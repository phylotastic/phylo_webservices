#scientific names to common names service: version 1.0
import json
import requests
import time
import datetime 
import urllib
import ConfigParser
from os.path import dirname, abspath

#----------------------------------------------
headers = {'content-type': 'application/json'}

#---------------------------------------
def get_api_key():
	config = ConfigParser.ConfigParser()
	current_dir = dirname(abspath(__file__))
	config.read(current_dir + "/"+ "habitat_service.cfg")
	
	eol_api_key = config.get('EOL', 'api_key')

	return eol_api_key

#----------------------------------------------
def match_species(speciesName):
 	search_url = "http://eol.org/api/search/1.0.json"
 	EOL_API_Key = get_api_key()
    
 	payload = {
 		'key': EOL_API_Key,
 		'q': speciesName,
 		'page': 1,
 		'exact': True,
 		'filter_by_taxon_concept_id': "",
 		'filter_by_hierarchy_entry_id': "",
 		'filter_by_string': "", 
 		'cache_ttl': ""
    }
 	encoded_payload = urllib.urlencode(payload)
 	response = requests.get(search_url, params=encoded_payload, headers=headers) 
    
 	numResults = 0
 	eol_response = {}
 	if response.status_code == requests.codes.ok:    
 		data_json = json.loads(response.text)
 		#length = len(data_json['results']) 
 		numResults = data_json['totalResults']
 		eol_response['status_code'] = 200
 		eol_response['message'] = "Success"    
 	else:
 		eol_response['status_code'] = response.status_code
 		eol_response['message'] = "Error: Response error from EOL while matching species name."

 	if numResults == 0:
 		eol_response['eol_id'] = -1 
 	else: 
 		eol_response['eol_id'] = data_json['results'][0]['id']

 	return eol_response

#--------------------------------------------   
def get_species_info(speciesId):
 	page_url = "http://eol.org/api/pages/1.0.json" 
 	EOL_API_Key = get_api_key()   
 	payload = {
 		'key': EOL_API_Key,
 		'batch' : False,
 		'id': speciesId,
 		'images_per_page': 5,
 		'images_page': 1,
 		'videos_per_page': 0,
 		'videos_page': 0,
 		'sounds_per_page': 0,
 		'sounds_page': 0,
 		'maps_per_page': 0,
 		'maps_page': 0,
 		'texts_per_page': 0,
 		'texts_page': 0,
 		'iucn': True, #include the IUCN Red List status object
 		'subjects': "overview",  #'overview' to return the overview text (if exists)
 		'licenses': "all",
 		'details': True, #include all metadata for data objects
 		'common_names': True,
 		'synonyms': False,
 		'references': False,
 		'taxonomy': True,
 		'vetted': 2, # only trusted and unreviewed content will be returned (untrusted content will not be returned)
 		'cache_ttl': "", 
 		'language': "en"
    }
 	encoded_payload = urllib.urlencode(payload)
 	response = requests.get(page_url, params=encoded_payload, headers=headers) 
    
 	if response.status_code == requests.codes.ok:    
 		species_info_json = json.loads(response.text)
 		return species_info_json
 	else:
 		return None
 		
#--------------------------------------------
def get_vernacular_names(vernacularInfo):
	#print vernacularInfo
 	species_comm_name_list = []
 	for info in vernacularInfo:
 		if 'eol_preferred' in info and info['eol_preferred'] and info["language"] == "en":
 			species_comm_name_list.append(info['vernacularName'])

 	return species_comm_name_list


#---------------------------------------------------
def get_sci_to_comm_names(inputSpeciesList):
 	start_time = time.time()
 	response = {}	
 	outputSpeciesList = []

 	for inputSpecies in inputSpeciesList:
 		species_obj = {}
 		images_species = []	 	
 		eol_response = match_species(inputSpecies)
 		if eol_response['status_code'] != 200:
 			return eol_response
 		species_id = eol_response['eol_id'] 
 		species_obj['searched_name'] = inputSpecies	 	
 		if species_id == -1:		 	
 			species_obj['matched_name'] = ""
 			species_obj['total_names'] = 0
 		else: 	
 		 	species_info_json = get_species_info(species_id)
 			if 'status_code' in species_info_json and species_info_json['status_code'] != 200:
 				return species_info_json
 			else:
 				species_obj['matched_name'] = species_info_json['scientificName']
 				species_obj['identifier'] = species_id #'eol_id'			
 				common_name_lst = species_info_json['vernacularNames'] 
 				length = len(common_name_lst)		
 				if length != 0:
 					comm__name_species = get_vernacular_names(common_name_lst)
 					#species_obj['total_names'] = len(comm__name_species)
 				else:
 					comm__name_species = []

 		species_obj['common_names'] = comm__name_species
 		outputSpeciesList.append(species_obj)
	
 	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	
 	meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["http://eol.org"]}
 #, 'service_documentation': service_documentation }
 	response['meta_data'] = meta_data
 	
 	response['message'] = "Success"
 	response['status_code'] = 200
 	response['result'] = outputSpeciesList
 	#response['input_species'] = inputSpeciesList
 
 	return response
 	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':

	#inputSpecies = ["Rangifer tarandus", "Cervus elaphus", "Bos taurus"]#, "Ovis orientalis", "Suricata suricatta", "Cistophora cristata", "Mephitis mephitis"]
   
 	#inputTaxon = 'Felidae'
	#inputTaxon = 'Canidae' #family
 	
 	#start_time = time.time()    
 	
 	#print get_sci_to_comm_names(inputSpecies)
 	
 	#end_time = time.time()
 	
 	#print end_time-start_time
