#species to EOL url service: version 1.0
import json
import requests
import time
import datetime 
import configparser

from os.path import dirname, abspath

#----------------------------------------------
headers = {'content-type': 'application/json'}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#------------------------------------------
def get_api_key():
	config = configparser.ConfigParser()
	current_dir = dirname(abspath(__file__))
	config.read(current_dir + "/"+ "service.cfg")
	
	eol_api_key = config.get('EOL', 'api_key')

	return eol_api_key

#----------------------------------------------
def match_species(speciesName):
 	EOL_API_Key = get_api_key()
 	search_url = "http://eol.org/api/search/1.0.json"    
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
 	#encoded_payload = urllib.urlencode(payload)
 	response = requests.get(search_url, params=payload, headers=headers) 

 	numResults = 0    
 	data_json = {}
 	if response.status_code == requests.codes.ok:    
 		data_json = json.loads(response.text) 
 		numResults = data_json['totalResults']
 		data_json['status_code'] = response.status_code
 	else:
 		data_json['status_code'] = response.status_code
 		data_json['message'] = "Error: Reponse error from EOL search api"
  	
 	if numResults == 0:
 		return None 
 	else: 
 		return data_json

#---------------------------------------------------
def get_eolurls_species(inputSpeciesList, post=False):
 	start_time = time.time()
 	response = {}	
 	outputSpeciesList = []

 	for inputSpecies in inputSpeciesList:
 		species_obj = {}
 		url_species = []	 	
 		match_species_json = match_species(inputSpecies)
 		species_obj['searched_name'] = inputSpecies	 	
 		if match_species_json is None:		 	
 			species_obj['matched_name'] = ""
 		elif match_species_json is not None and match_species_json['status_code'] == 200:
 			species_info_link = match_species_json['results'][0]['link']
 			species_obj['matched_name'] = match_species_json['results'][0]['title']
 			species_obj['eol_id'] = match_species_json['results'][0]['id']			
 			species_obj['species_info_link'] = species_info_link 
 		else: 
 			return match_species_json	
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
 	response['species'] = outputSpeciesList
 	
 	#response['service_url'] = service_url
 	response['input_species'] = inputSpeciesList

 	return response

#--------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':

#	inputSpecies = ["Panthera leo", "Panthera onca"]
 	#inputTaxon = 'Felidae'
	
 	#start_time = time.time()    
 	#print get_eolurls_species(inputSpecies)
 	#end_time = time.time()
 	#print end_time-start_time
