#service description: get scientific names for input common names using Tropicos plant database 
#service version: 0.1
import json
import requests
import time
import datetime 
import configparser

from bs4 import BeautifulSoup
from os.path import dirname, abspath

#----------------------------------------------
base_url = "http://services.tropicos.org/Name/"

#-----------------------------------------------------
def get_api_key():
	config = configparser.ConfigParser()
	current_dir = dirname(abspath(__file__))
	config.read(current_dir + "/"+ "service.cfg")
	
	tropicos_api_key = config.get('TROPICOS', 'api_key')

	return tropicos_api_key

#-----------------------------------------------------
def search_name(commonName, best_match):
	api_url = base_url + "Search?"
	Tropicos_API_Key = get_api_key()
	match_type = "exact" if best_match else "wildcard" 	

	response = {}    
	response['status_code'] = 200
	response['message'] = "Success"
	
	payload = {
		'commonname': commonName,
		'type': match_type,
		'apikey': Tropicos_API_Key,
		'format': "json"	
	}

	api_response = requests.get(api_url, params=payload) 
	
	match_name_info = {'searched_name': commonName}
	match_name_list = []

	if api_response.status_code == requests.codes.ok:
		#print api_response.text	 	
		match_name_list = extract_sc_names_info(api_response.text, not best_match) #best match true = don't want multiple results	
	else:
		response['status_code'] = 500
		response['message'] = "Error: Retrieving data from Tropicos API"

	match_name_info['matched_names'] = match_name_list
	response['result'] = match_name_info 

	return response

#----------------------------------------------
#get multiple results
def extract_sc_names_info(respText, multiple=False):
	sc_names_list = []
	json_resp = json.loads(respText)
	
	if 'Error' in json_resp[0]: #[{u'Error': u'No names were found'}]
		return sc_names_list

	for match in json_resp:
		sc_name_info = search_key(match['NameId'])
		if sc_name_info is not None:
			sc_names_list.append(sc_name_info)			
		if not multiple:
			break 
			
	return sc_names_list

#-------------------------------------------
def search_key(key):
	api_url = base_url+str(key)

	payload = {'apikey': get_api_key(), 'format': "json"}
	response = requests.get(api_url, params=payload) 
	
	name_info = {}
	if response.status_code == requests.codes.ok:
		json_resp = json.loads(response.text)
		name_info['scientific_name'] = json_resp['ScientificName']
		name_info['rank'] = json_resp['Rank']
		#name_info['common_name'] = extra_info['commonName']
		name_info['identifier'] = json_resp['NameId'] 
		name_info['source_info_url'] = json_resp['Source']
	else:
		name_info = None

	return name_info

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

	final_result['metadata'] = {'creation_time': creation_time, 'execution_time': "{:4.2f}".format(execution_time), 'source_urls': ["http://services.tropicos.org/"] }   	 
 	
	return final_result
#--------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#if __name__ == '__main__':

	#commonNameList = ["christmas fern", "castor bean", "indian sandalwood", "annual blue grass"]
	#commonNameList = ["corn", "rice", "wheat", "potato", "onion", "garlic", "cucumber", "tomato", "lettuce", "pea"]
	#commonNameList = ["christmas fern", "castor bean", "indian sandalwood", "annual blue grass"]
	#commonNameList = ["carrot"]
	
	#print (get_scientific_names(commonNameList))
 	
