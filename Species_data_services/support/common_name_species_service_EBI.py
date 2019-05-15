#service description: get scientific names for input common names using European Bioinformatics Institute Taxonomy database 
#service version: 0.1
#source: https://www.ebi.ac.uk/ena/browse/taxonomy-service
import json
import requests
import time
import datetime 
import urllib

#----------------------------------------------
base_url = "http://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/"
#-----------------------------------------------------

def search_name(commonName, best_match):

	api_url = base_url + "any-name/" if best_match else base_url + "suggest-for-search/"	
	rest_api = api_url + commonName

	response = {}    
	response['status_code'] = 200
 	response['message'] = "Success"
	
	api_response = requests.get(rest_api) 
	
	match_name_info = {'searched_name': commonName}
	match_name_list = []

	if api_response.status_code == requests.codes.ok:
		#print api_response.text	 	
		match_name_list = extract_sc_names_info(api_response.text, not best_match) #best match true = don't want multiple results	
	else:
		response['status_code'] = 500
		response['message'] = "Error: Retrieving data from EBI API"

	match_name_info['matched_names'] = match_name_list
	response['result'] = match_name_info 

	return response

#----------------------------------------------
def extract_sc_names_info(response_result, multiple_match=False):
	matched_names = []
	json_result = json.loads(response_result)
	for indx, result in enumerate(json_result):
		match_name_obj = {}
		match_name_obj['scientific_name'] = result['scientificName']
		match_name_obj['common_name'] = result['commonName']  
		match_name_obj['identifier'] = int(result['taxId'])
		matched_names.append(match_name_obj)
		if not(multiple_match):
			break
		if indx == 20:
			break

	return matched_names

#---------------------------------------------------
def get_scientific_names(inputNameList, best_match=True):	
 	start_time = time.time()
	
	final_result = {'status_code': 200, 'message': "Success" }

	results = []
	for inputName in inputNameList:
		match_result = search_name(inputName, best_match)
		if match_result['status_code'] == 200:
			results.append(match_result['result'])

	final_result['result'] = results

	end_time = time.time()
 	execution_time = end_time-start_time    
    
	#service result creation time
 	creation_time = datetime.datetime.now().isoformat()

	final_result['metadata'] = {'creation_time': creation_time, 'execution_time': "{:4.2f}".format(execution_time), 'source_urls': ["https://www.ebi.ac.uk"] }   	 
 	
 	return final_result
#--------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#if __name__ == '__main__':

	#commonNameList = ["christmas fern", "castor bean", "indian sandalwood", "annual blue grass"]
	#commonNameList = ["corn", "rice", "wheat", "potato", "onion", "garlic", "cucumber", "tomato", "lettuce", "pea"]
	#commonNameList = ["christmas fern", "castor bean", "indian sandalwood", "annual blue grass"]
	#commonNameList = ["cow", "cat", "horse"]
	
	#print get_scientific_names(commonNameList)
 	
