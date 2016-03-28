#taxon to species service: version 2.0
import json
import requests
import time
import pymongo
import datetime 

#------------------------------------
dbName = "TaxonSpecies"
dataCollectionName ="taxonSpecieslist"
#-------------------------------------
#Open Tree of Life API
api_url = "https://api.opentreeoflife.org/v2/"
headers = {'content-type': 'application/json'}
#--------------------------------------

#connection to Mongo DB
def connect_mongodb(host='localhost', port=27017):
 	try:
 		conn=pymongo.MongoClient(host, port)
 		print "Connected successfully!!!"
 	except pymongo.errors.ConnectionFailure, e:
 		print "Could not connect to MongoDB: %s" % e 

 	return conn

#------------------------------------------
#check cache database 
def find_taxon_cache(conn, taxonName, findAll=True, country=None):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	
 	documents = data_collection.find({"taxon":{"$eq":taxonName}, "is_all":{"$eq":findAll}, "country":{"$eq":country}},{"_id":0})
 	
 	response = {}
 	if documents.count() == 0:
 		response['result'] = ""
  		response['cache_found'] = False	
 	else:
 		for doc in documents:
  	 		taxon_species = doc['species'] 				
 			break;
 		data_collection.update({ "taxon":{"$eq":taxonName}, "is_all":{"$eq":findAll}, "country":{"$eq":country} },{ "$currentDate": {"last_accessed": True} }) #update the last accessed value		
 		response['result'] = taxon_species
  		response['cache_found'] = True
 	
 	return response

#------------------------------------------
#insert cache into database 
def insert_taxon_cache(conn, taxonName, species_lst, find_all=True, country=None):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	
 	insert_status = None
 	
 	query_result = data_collection.find({"taxon": taxonName,"is_all": find_all,"country": country})
 	if query_result.count() == 0:
 		document = {"taxon": taxonName, "country": country, "is_all": find_all, "species": species_lst, "last_accessed": datetime.datetime.now()}
 		insert_status = data_collection.insert(document)
 		
 	response = {}

 	if insert_status != None:
 		response['status'] = "Inserted"	
 	else:
 		response['status'] = "Not inserted"
 	
 	return response

#----------------------------------------------
def match_taxon(taxonName):
    resource_url = api_url + "tnrs/match_names"    
    payload = {
        'names': [taxonName], 
        'do_approximate_matching': 'false'
    }
    response = requests.post(resource_url, data=json.dumps(payload), headers=headers)
     
    data_json = json.loads(response.text)
    length = len(data_json['results']) 
    
    if length == 0:
        return -1 
    else: 
        return data_json['results'][0]['matches'][0]['ot:ottId']

#-------------------------------------------
def get_children(ottId):
    resource_url = api_url + "taxonomy/taxon"    
    payload = {
        'ott_id': ottId,
        'include_children': 'true'    
    }
    response = requests.post(resource_url, data=json.dumps(payload), headers=headers)
     
    #print response.text 
    return json.loads(response.text)

#----------------------------------------    
def get_species_from_highrank(highrankChildren, conn):
    species_list = [] 
    #get all children of each higherankedChildren    
    for child in highrankChildren:
 		cache_result = find_taxon_cache(conn, child['ot:ottTaxonName'])
 		if cache_result['cache_found']:
 			species_list.extend(cache_result['result'])
 			#print "cache found for child" 
 			continue 
 		species_lst = []  #temp species list
 		res_json = get_children(child['ot:ottId'])
 		children_lst = res_json['children']
 		if child['rank'] == 'genus':
 		 	#get all species from genus
 			if len(children_lst) == 0:
 				continue
 			species_lst = get_species_from_genus(children_lst)
 			#extend the species list with the species of this genus
 			species_list.extend(species_lst)
 		else:
 			highrankChildren.extend(children_lst) 
                                   
    return species_list

#-------------------------------------------
def get_species_from_genus(genusChildren):
    species_list = []
    #get all species of a genus 
    for child in genusChildren:
 		if child['rank'] == 'species':
 			species_list.append(child['ot:ottTaxonName'])            
        
    return species_list

#-------------------------------------------------    
def check_species_by_country(species, country):
    INaturalistApi_url = 'https://www.inaturalist.org/places.json'

    payload = {
        'taxon': species,
        'place_type': 'Country',
    }    
    
    matched_result = requests.get(INaturalistApi_url, params=payload)
    res_json = json.loads(matched_result.text) 
    
    countryList = []
    for country in res_json:
        countryList.append(country['name'])
    
    #commonList = list(set(countries).intersection(set(countryList)))
    
    if (country in countryList):
        return True
    else:
        return False

#---------------------------------------------------
def get_all_species(inputTaxon):
 	
 	ott_id = match_taxon(inputTaxon)
 	if ott_id == -1:
 		final_result = create_json_msg(inputTaxon,[], 'No Taxon matched with %s' %(inputTaxon), 404)
 		return final_result
 	
 	species_list = []
 	conn = connect_mongodb()
 	cache_result = find_taxon_cache(conn, inputTaxon)
 	if cache_result['cache_found']:
 		final_result = create_json_msg(inputTaxon, cache_result['result'], 'Success', 200) 
 		print "Cache found"
 		return final_result 
 	else:
 		data_json = get_children(ott_id)
 		if data_json['rank'] == 'genus':
 			species_list = get_species_from_genus(data_json['children'])
 		else:
 			species_list = get_species_from_highrank(data_json['children'], conn)
 	
 	#species_list.sort()
 	len_splist = len(species_list)
 	
 	if len_splist != 0:
 	 	final_result = create_json_msg(inputTaxon, species_list, 'Success', 200)
 	 	insert_taxon_cache(conn, inputTaxon, species_list)
 	else:	
 	 	final_result = create_json_msg(inputTaxon, species_list, 'No species found', 204)

 	return final_result

#--------------------------------------------------
def get_country_species(inputTaxon, country):

 	ott_id = match_taxon(inputTaxon)
 	if ott_id == -1:
 		final_result = create_json_msg(inputTaxon, [], 'No Taxon found', 404)
 		return final_result
 	
 	conn = connect_mongodb()
 	cache_result = find_taxon_cache(conn, inputTaxon, False, country)
 	if cache_result['cache_found']:
 		species_list = cache_result['result']
 		if len(species_list) != 0:
 			final_result = create_json_msg(inputTaxon, species_list, 'Success', 200)
 		else:
 			final_result = create_json_msg(inputTaxon, species_list, 'No species found on this country', 206) 
 		print "Cache found"
 		return final_result	
 	else:
 		conn.close()
 		all_species_result = get_all_species(inputTaxon)  
  		all_species_json = json.loads(all_species_result)
 		status_code = all_species_json['statuscode']
  		species_list = all_species_json['species']
 		message = all_species_json['message']	
 	
 		#species_list.sort()
    	#countries = ['Bhutan', 'Nepal', 'Canada']

 		if status_code == 404 or status_code == 204:  #no taxon found or no species found
  			return all_species_json
 		elif status_code == 200:
 		 	species_lst = []
 		 	for species in species_list:
 				if check_species_by_country(species, country):
 					species_lst.append(species)
  	
 	if len(species_lst) != 0:
 	 	final_result = create_json_msg(inputTaxon, species_lst, 'Success', 200)
   	else:
 		final_result = create_json_msg(inputTaxon, species_lst, 'No species found on this country', 206)

 	insert_taxon_cache(conn, inputTaxon, species_lst, False, country) 	

 	return final_result
 	
#--------------------------------------------

def create_json_msg(input_taxon, species_lst, msg, code):
 	
 	return json.dumps({'taxon': input_taxon,'species': species_lst, 'message': msg, 'statuscode': code})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':

	#inputTaxon = 'Vulpes' #genus
 	#inputTaxon = 'Felidae'
	#inputTaxon = 'Canidae' #family
 	#inputTaxon = 'Carnivora' #order
 	#inputTaxon = 'Tremarctos'
	#inputTaxon = 'Mustelidae' 
 	#inputTaxon = 'Ursi'  
 	#country = 'Bangladesh'
 	#country = 'Brazil'
 	#country = 'USA'
 	#start_time = time.time()    
 	
 	#print get_all_species(inputTaxon)
 	#print get_country_species(inputTaxon, country)
 	#end_time = time.time()
 	
 	#print end_time-start_time
