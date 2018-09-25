#taxon to species service: version 2.0
import json
import requests
import time
import pymongo
import datetime 

import google_dns

#------------------------------------
dbName = "TaxonSpecies"
dataCollectionName ="taxonSpecieslist"
#-------------------------------------
#Open Tree of Life API
base_url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/"
api_url = "https://api.opentreeoflife.org/v3/"
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
    jsonPayload = json.dumps(payload)
    #response = requests.post(resource_url, data=json.dumps(payload), headers=headers)
    #+++++++++++Solution 2++++++++++++++++
    try: 
       response = requests.post(resource_url, data=jsonPayload, headers=headers)
    except requests.exceptions.ConnectionError:
       alt_url = google_dns.alt_service_url(resource_url)
       response = requests.post(alt_url, data=jsonPayload, headers=headers, verify=False)        
    #----------------------------------------------
    
    if response.status_code == requests.codes.ok: 
       data_json = json.loads(response.text)
       length = len(data_json['results'])
       message = "Success"
       status_code = 200 
    else:    
       data_json = json.loads(response.text)
       if 'message' in data_json:
          message = "OToL TNRS Error: "+data_json['message']
       else:
          message = "Error: Response error from Open Tree of Life TNRS"
       if 'status' in data_json:
          status_code = data_json['status']
       else:
          status_code = response.status_code

    if length == 0 and status_code == 200:
        ott_id = -1 
    else: 
        ott_id = data_json['results'][0]['matches'][0]['taxon']['ott_id']

    return {'message': message, 'status_code': status_code, 'ott_id': ott_id}

#-------------------------------------------
def get_children(ottId):
    resource_url = api_url + "taxonomy/taxon_info"    
    payload = {
        'ott_id': ottId,
        'include_children': 'true'    
    }

    jsonPayload = json.dumps(payload)
    #response = requests.post(resource_url, data=json.dumps(payload), headers=headers)
    #+++++++++++Solution 2++++++++++++++++
    try: 
       response = requests.post(resource_url, data=jsonPayload, headers=headers)
    except requests.exceptions.ConnectionError:
       alt_url = google_dns.alt_service_url(resource_url)
       response = requests.post(alt_url, data=jsonPayload, headers=headers, verify=False)        
    #----------------------------------------------
         
    data_json = json.loads(response.text)
    if response.status_code == requests.codes.ok:    
       message = "Success"
       status_code = 200 
    else:    
       if 'message' in data_json:
          message = "OToL Taxonomy API Error: "+data_json['message']
       else:
          message = "Error: Response error from Open Tree of Life Taxonomy API"
       if 'status' in data_json:
          status_code = data_json['status']
       else:
          status_code = response.status_code

    return {'message': message, 'status_code': status_code, 'response': response.text}
#----------------------------------------    
def get_species_from_highrank(highrankChildren, conn):
 	species_list = []
 	
    #get all children of each higherankedChildren    
 	for child in highrankChildren:
 		cache_result = find_taxon_cache(conn, child['name'])
 		if cache_result['cache_found']:
 			species_list.extend(cache_result['result'])
 			#print "cache found for child" 
 			continue       
 		species_lst = []  #temp species list
 		result = get_children(child['ott_id'])
 		if result['status_code'] != 200:
 			return result
 		res_json = json.loads(result['response'])
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
                                   
 	return {'species':species_list} 

#-------------------------------------------
def get_species_from_genus(genusChildren):
	species_list = []
    #get all species of a genus 
	for child in genusChildren:
		if child['rank'] == 'species':
			species_list.append(child['name'])            
        
	return species_list

#-------------------------------------------------    
def check_species_by_country(species, country):
    INaturalistApi_url = 'https://www.inaturalist.org/places.json'

    payload = {
        'taxon': species,
        'place_type': 'Country',
    }    
    
    response = requests.get(INaturalistApi_url, params=payload)
    res_json = json.loads(response.text) 
    
    if response.status_code == requests.codes.ok:    
       message = "Success"
       status_code = 200 
    else:    
       if 'message' in res_json:
          message = "INaturalist API Error: "+res_json['message']
       else:
          message = "Error: Response error from INaturalist API"
       if 'status' in res_json:
          status_code = res_json['status']
       else:
          status_code = response.status_code
  
    countryList = []
    for place in res_json:
        countryList.append(place['name'].lower())
    country = country.lower()
    #commonList = list(set(countries).intersection(set(countryList)))
    
    if (country in countryList):
        exists = True
    else:
        exists = False

    return {'message': message, 'status_code': status_code, 'exists': exists}

#---------------------------------------------------
def get_all_species(inputTaxon, ottid=None):
 	start_time = time.time()

 	#service_url = base_url + "all_species?taxon=" + inputTaxon
 	#service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-6"

 	large_result = False
 	high_rank = None
 	cache_exists = False
 	if ottid is None:
 		ot_tnrs_resp = match_taxon(inputTaxon)
 		if ot_tnrs_resp['status_code'] != 200:
 			return ot_tnrs_resp
 		ott_id = ot_tnrs_resp['ott_id']
 	else:
 		ott_id = ottid
 	
 	if ott_id == -1:
 		final_result = {'input_taxon': inputTaxon,'species': [], 'message': 'No Taxon matched with %s' %(inputTaxon), 'status_code': 200}
 		len_splist = 0	
 	else: #taxon name matched	
 		species_list = []
 		conn = connect_mongodb()
 		cache_result = find_taxon_cache(conn, inputTaxon)		
 		if cache_result['cache_found']:
 			final_result = {'input_taxon': inputTaxon,'species': cache_result['result'], 'message': 'Success', 'status_code': 200}
 			#print "Cache found"
 			cache_exists = True
 			len_splist = len(cache_result['result'])	 
 		else:
 			data_result = get_children(ott_id)
 
 			if data_result['status_code'] != 200:
 				return data_result
 			data_json = json.loads(data_result['response'])
 			#print data_json
 			if data_json['rank'] == 'species' or data_json['rank'] == 'subspecies':
 				species_list.append(data_json['name'])		
 			elif data_json['rank'] == 'genus':
 				species_list = get_species_from_genus(data_json['children'])
 			elif data_json['rank'] in['superorder','order','suborder','infraorder','parvorder','class','superclass','subclass','infraclass','parvclass','phylum','kingdom','domain', 'no rank']:
 				large_result = True
 				high_rank = data_json['rank']
 			else:
 				result = get_species_from_highrank(data_json['children'], conn)
 				if 'status_code' in species_list: #error occured in source web service
 					return result
 				species_list = result['species']
 			len_splist = len(species_list)
	
 		#print species_list
 		#species_list.sort()
 	 	
 	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()

 	if len_splist > 0 and not(cache_exists):
 	 	final_result = {'input_taxon': inputTaxon,'species': species_list, 'message': 'Success', 'status_code': 200}
 	 	insert_taxon_cache(conn, inputTaxon, species_list)
 		conn.close()
 	elif len_splist == 0 and not(cache_exists) and ott_id != -1 and not large_result:	
 	 	final_result = {'input_taxon': inputTaxon,'species': species_list, 'message': 'No species found', 'status_code': 200}
 	elif len_splist == 0 and not(cache_exists) and ott_id != -1 and large_result:	
 	 	final_result = {'input_taxon': inputTaxon, 'species': [], 'message': "Currently input taxon with '%s' rank is not supported"%high_rank, 'status_code': 403}

 	meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-Taxonomy"]} #,'service_documentation': service_documentation} #'service_url': service_url,
 	final_result['meta_data'] = meta_data
 	final_result['total_names'] = len_splist
 	final_result['input_taxon'] = inputTaxon
 	 	
 	return final_result 

#--------------------------------------------------
def get_country_species(inputTaxon, country):
 	start_time = time.time()

 	#service_url = base_url + "country_species?taxon=" + inputTaxon + "&country=" + country 
 	#service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-7"

 	no_species_found = False
 	cache_exists = False

 	ot_tnrs_resp = match_taxon(inputTaxon)
 	if ot_tnrs_resp['status_code'] != 200:
 		return ot_tnrs_resp
 	ott_id = ot_tnrs_resp['ott_id']
 	 
 	if ott_id == -1:
 		final_result = {'input_taxon': inputTaxon,'species': [], 'message': 'No Taxon matched with %s' %(inputTaxon), 'status_code': 200}
 		len_splist = 0
 	else: #taxon name matched and ott_id found
 		conn = connect_mongodb()
 		cache_result = find_taxon_cache(conn, inputTaxon, False, country)
 		if cache_result['cache_found']:
 			species_list = cache_result['result']
 			len_splist = len(species_list)
 			if len_splist != 0:
 				final_result = {'input_taxon': inputTaxon,'species': species_list, 'message': 'Success', 'status_code': 200}
 			else:
 				final_result = {'input_taxon': inputTaxon,'species': species_list, 'message': 'No species found on this country', 'status_code': 200}  	
 			#print "Cache found"
 			cache_exists = True	
 		else:
 			all_species_result = get_all_species(inputTaxon, ott_id)
 			all_species_json = all_species_result
 			#all_species_json = json.loads(all_species_result)
 			status_code = all_species_json['status_code']
  			species_list = all_species_json['species']
 			message = all_species_json['message']	
 			#print all_species_result
 			
 			species_lst = []
 			if status_code == 200 and len(species_list) == 0:  #no species found
  				final_result = all_species_result
 				no_species_found = True
 				len_splist = len(species_list)
 				species_lst = species_list
 			elif status_code == 200 and len(species_list) > 0:
 		 		for species in species_list:
 					check_result = check_species_by_country(species, country)
 					if check_result['status_code'] != 200:
 						return check_result
 					exists = check_result['exists']
 					if exists:
 						species_lst.append(species)
 				len_splist = len(species_lst)
 			else:
  				return all_species_result
 
 	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()

 	if  len_splist != 0 and not(cache_exists):
 	 	final_result = {'input_taxon': inputTaxon,'species': species_lst, 'message': 'Success', 'status_code': 200}
 	elif len_splist == 0 and not(cache_exists) and ott_id != -1 and not no_species_found:
 		final_result = {'input_taxon': inputTaxon,'species': species_lst, 'message': 'No species found on this country', 'status_code': 200}

 	if (not cache_exists and len_splist > 0) or (not cache_exists and no_species_found):
 		conn = connect_mongodb()
 		insert_taxon_cache(conn, inputTaxon, species_lst, False, country) 

 	meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-Taxonomy", "https://www.inaturalist.org"]} #, 'service_url': service_url, 'service_documentation': service_documentation}	
 	final_result['meta_data'] = meta_data
 	final_result['total_names'] = len_splist
 	final_result['input_country'] = country
 	#final_result['input_taxon'] = inputTaxon

 	return final_result 
 	
#--------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':

	#To remove the warning: "the InsecurePlatformWarning: A true SSLContext object is not available"
 	#requests.packages.urllib3.disable_warnings()

 	#inputTaxon = "Hydropotes"
	#inputTaxon = 'Vulpes' #genus
 	#inputTaxon = 'Felidae'
	#inputTaxon = 'Canidae' #family
 	#inputTaxon = 'Carnivora' #order
 	#inputTaxon = 'Tremarctos'
	#inputTaxon = 'Panthera onca mesembrina' 
 	#inputTaxon = 'Panthera onca'
 	#inputTaxon = "Aramidae"  
 	#countries = ['Bhutan', 'Nepal', 'Canada']
 	#country = 'Bangladesh'
 	#country = 'United States'
 	#country = 'Nepal'
 	#print match_taxon(inputTaxon) 
 	#print get_all_species(inputTaxon)
 	#get_children(735488)
 	#print check_species_by_country(inputTaxon, country)	
 	#print get_country_species(inputTaxon, country)
 	
