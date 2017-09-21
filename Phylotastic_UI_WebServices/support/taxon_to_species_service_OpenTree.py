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
base_url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/"
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
 			break
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
    for place in res_json:
        countryList.append(place['name'].lower())
    country = country.lower()
    #commonList = list(set(countries).intersection(set(countryList)))
    
    if (country in countryList):
        return True
    else:
        return False

#---------------------------------------------------
def get_all_species(inputTaxon):
 	start_time = time.time()

 	service_url = base_url + "all_species?taxon=" + inputTaxon
 	service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-6"

 	cache_exists = False
 	ott_id = match_taxon(inputTaxon)
 	if ott_id == -1:
 		final_result = {'taxon': inputTaxon,'species': [], 'message': 'No Taxon matched with %s' %(inputTaxon), 'status_code': 204}
 		len_splist = 0	
 	else: #taxon name matched	
 		species_list = []
 		conn = connect_mongodb()
 		cache_result = find_taxon_cache(conn, inputTaxon) 		
 		if cache_result['cache_found']:
 			final_result = {'taxon': inputTaxon,'species': cache_result['result'], 'message': 'Success', 'status_code': 200}
 			print "Cache found"
 			cache_exists = True
 			len_splist = len(cache_result['result'])	 
 		else:
 			data_json = get_children(ott_id)
 			if data_json['rank'] == 'species' or data_json['rank'] == 'subspecies':
 				species_list.append(data_json['ot:ottTaxonName'])		
 			elif data_json['rank'] == 'genus':
 				species_list = get_species_from_genus(data_json['children'])
 			else:
 				species_list = get_species_from_highrank(data_json['children'], conn)
 			len_splist = len(species_list)
	
 		#print species_list
 		#species_list.sort()
 	 	
 	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()

 	if len_splist > 0 and not(cache_exists):
 	 	final_result = {'taxon': inputTaxon,'species': species_list, 'message': 'Success', 'status_code': 200}
 	 	insert_taxon_cache(conn, inputTaxon, species_list)
 	elif len_splist == 0 and not(cache_exists) and ott_id != -1:	
 	 	final_result = {'taxon': inputTaxon,'species': species_list, 'message': 'No species found', 'status_code': 204}

 	final_result['creation_time'] = creation_time
 	final_result['execution_time'] = "{:4.2f}".format(execution_time)
 	final_result['total_names'] = len_splist
 	#final_result['source_urls'] = ["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-Taxonomy"]
 	#final_result['source_version'] = "ott2.9draft12"
 	final_result['service_url'] = service_url
 	final_result['service_documentation'] = service_documentation

 	return final_result #return json.dumps(final_result)

#--------------------------------------------------
def get_country_species(inputTaxon, country):
 	start_time = time.time()

 	service_url = base_url + "country_species?taxon=" + inputTaxon + "&country=" + country 
 	service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-7"

 	cache_exists = False
 	ott_id = match_taxon(inputTaxon)
 	if ott_id == -1:
 		final_result = {'taxon': inputTaxon,'species': [], 'message': 'No Taxon matched with %s' %(inputTaxon), 'status_code': 204}
 		len_splist = 0
 	else: #taxon name matched and ott_id found
 		conn = connect_mongodb()
 		cache_result = find_taxon_cache(conn, inputTaxon, False, country)
 		if cache_result['cache_found']:
 			species_list = cache_result['result']
 			len_splist = len(species_list)
 			if len_splist != 0:
 				final_result = {'taxon': inputTaxon,'species': species_list, 'message': 'Success', 'status_code': 200}
 			else:
 				final_result = {'taxon': inputTaxon,'species': species_list, 'message': 'No species found on this country', 'status_code': 204}  	
 			#print "Cache found"
 			cache_exists = True	
 		else:
 			conn.close()
 			all_species_result = get_all_species(inputTaxon)  
  			all_species_json = json.loads(all_species_result)
 			status_code = all_species_json['status_code']
  			species_list = all_species_json['species']
 			message = all_species_json['message']	
 			#print all_species_result
 			#species_list.sort()
    		#countries = ['Bhutan', 'Nepal', 'Canada']

 			if status_code == 204:  #no taxon found or no species found
  				return all_species_json
 			elif status_code == 200:
 		 		species_lst = []
 		 		for species in species_list:
 					if check_species_by_country(species, country):
 						species_lst.append(species)
 				len_splist = len(species_lst)
  	
 	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()

 	if  len_splist != 0 and not(cache_exists):
 	 	final_result = {'taxon': inputTaxon,'species': species_lst, 'message': 'Success', 'status_code': 200}
   	elif len_splist == 0 and not(cache_exists) and ott_id != -1:
 		final_result = {'taxon': inputTaxon,'species': species_lst, 'message': 'No species found on this country', 'status_code': 206}

 	if not(cache_exists):
 		insert_taxon_cache(conn, inputTaxon, species_lst, False, country) 

 	final_result['creation_time'] = creation_time
 	final_result['execution_time'] = "{:4.2f}".format(execution_time)
 	final_result['total_names'] = len_splist
 	#final_result['source_urls'] = ["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-Taxonomy", "https://www.inaturalist.org"]
 	#final_result['source_version'] = "ott2.9draft12"
 	final_result['service_url'] = service_url
 	final_result['service_documentation'] = service_documentation	
 	final_result['country'] = country

 	return final_result #return json.dumps(final_result)
 	
#--------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':

	#inputTaxon = 'Vulpes' #genus
 	#inputTaxon = 'Felidae'
	#inputTaxon = 'Canidae' #family
 	#inputTaxon = 'Carnivora' #order
 	#inputTaxon = 'Tremarctos'
	#inputTaxon = 'Panthera onca mesembrina' 
 	#inputTaxon = 'Panthera onca'  
 	#country = 'Bangladesh'
 	#country = 'United States'
 	#country = 'Nepal'
 	#print match_taxon(inputTaxon) 
 	#print get_all_species(inputTaxon)
 	#get_children(735488)
 	#print check_species_by_country(inputTaxon, country)	
 	#print get_country_species(inputTaxon, country)
 	
