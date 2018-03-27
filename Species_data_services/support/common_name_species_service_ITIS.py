#service description: get species for an input common name using ITIS service API 
#service version: 0.1
import json
import re
import requests
import time
import datetime 
import urllib

#-----------------------------------------------------------
base_url = "https://www.itis.gov/ITISWebService/jsonservice/ITISService/"
source_info_base = "https://www.itis.gov/ITISWebService/jsonservice/ITISService/getFullRecordFromTSN?tsn="
#-----------------------------------------------------------
def search_name(commonName, best_match):
	api_url = base_url + "searchByCommonName?"

	itis_response = {}    
	itis_response['status_code'] = 200
 	itis_response['message'] = "Success"
	
	payload = {'srchKey': commonName}
	encoded_payload = urllib.urlencode(payload)
	response = requests.get(api_url, params=encoded_payload) 
	
	match_name_info = {'searched_name': commonName}
	match_name_list = []
	
	if response.status_code == requests.codes.ok:
		#print response.text
		cm_name_key_list = extract_name_info(response.text)
		#empty list means: No common name matched
		sc_name_info = {}
		if len(cm_name_key_list) != 0:
			if best_match:  #best match result
				best_matched_key, cm_name = find_best_match_key(commonName, cm_name_key_list)
				if best_matched_key is None:
					sc_name_info['scientific_name'] = search_key(cm_name_key_list[0][1])
					sc_name_info['common_name'] = cm_name_key_list[0][0]
					sc_name_info['identifier'] = cm_name_key_list[0][1]
					sc_name_info['source_info_url'] = source_info_base + str(cm_name_key_list[0][1])
				else:
					sc_name_info['scientific_name'] = search_key(best_matched_key)
					sc_name_info['common_name'] = cm_name
					sc_name_info['identifier'] = best_matched_key
					sc_name_info['source_info_url'] = source_info_base + str(best_matched_key)

				match_name_list.append(sc_name_info)
			else: #multiple results
				match_name_list = extract_sc_names(cm_name_key_list) 		
	else:
		itis_response['status_code'] = 500
		itis_response['message'] = "ITIS response Error: Could not retrieve data"

	match_name_info['matched_names'] = match_name_list
	itis_response['result'] = match_name_info 

	return itis_response

#---------------------------------------------------
def extract_sc_names(cm_name_list):
	matched_results = []
	
	for indx, (cm_name, cm_key) in enumerate(cm_name_list):
		sc_name_info = {}	
		sc_name_info['scientific_name'] = search_key(cm_key)
		sc_name_info['common_name'] = cm_name
		sc_name_info['identifier'] = cm_key
		sc_name_info['source_info_url'] = source_info_base + str(cm_key)
		matched_results.append(sc_name_info)

	return matched_results

#----------------------------------------------------
def extract_name_info(ITIS_json_resp):
	found_common_names = []
	json_content = json.loads(ITIS_json_resp)
	
	if len(json_content['commonNames']) == 1 and json_content['commonNames'][0] is None:
		return found_common_names

	for cm_nm_obj in json_content['commonNames']:			
		cm_name = cm_nm_obj['commonName']
		cm_lang = cm_nm_obj['language'] 
		cm_tsn = cm_nm_obj['tsn']
		#print ("%s, %s")%(cm_name, cm_tsn)
		if cm_lang == "English": #get only english common names
			found_common_names.append( (cm_name, cm_tsn) )
	 
	return found_common_names

#-----------------------------------------------------
def find_best_match_key(input_name, cm_name_key_list):
	best_match_key = second_best_match_key = None
	best_match_cm_name = second_best_match_cm_name = None
	for indx, (cm_name, cm_tsn) in enumerate(cm_name_key_list):
		cleaned_input_name = re.sub(r"\s+"," ", input_name.strip())
		cm_name_lower = cm_name.lower()
		#print ("%s, %s, %s")%(input_name, cm_name_lower, cm_tsn)
		if best_match_key is None and cleaned_input_name.lower() == cm_name_lower:
			best_match_key = cm_tsn
			best_match_cm_name = cm_name
		elif second_best_match_key is None and cleaned_input_name.lower() in cm_name_lower:
			second_best_match_key = cm_tsn
			second_best_match_cm_name = cm_name	

	#print ("%s, %s, %s, %s")%(best_match_key, best_match_cm_name, second_best_match_key, second_best_match_cm_name)
	if best_match_key is not None:
		return best_match_key, best_match_cm_name 
	else:
		return second_best_match_key, second_best_match_cm_name

#--------------------------------------------------------
def search_key(key):
	api_url = base_url+"searchForAnyMatch?"

	payload = {'srchKey': key}
	encoded_payload = urllib.urlencode(payload)
	response = requests.get(api_url, params=encoded_payload) 
	
	if response.status_code == requests.codes.ok:
		json_resp = json.loads(response.text)
		name_info = json_resp['anyMatchList'][0]['sciName']
	else:
		name_info = None

	return name_info

#-------------------------------------------------------
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

	final_result['metadata'] = {'creation_time': creation_time, 'execution_time': "{:4.2f}".format(execution_time), 'source_urls': ["https://www.itis.gov/ws_description.html"] }   	 
 	
 	return final_result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':

	#commonName = "domestic dog"
	#commonName = "black bear"
	#commonName = "domestic cattle"  
	#commonName = "tiger" 
	#commonName = "blue whale"
	#commonName = "lion"
	#commonName = "horse"
	#commonName = "button mangrove"
	#input_names = ["domestic dog", "black bear", "domestic cattle", "blue whale"]
	#input_names = ["blue whale", "swordfish", "killer whale"]
	#input_names = ["Christmas fern", "cutleaf coneflower", "Castor bean"]
	#input_names = ["Flowering dogwood", "White oak", "Oregon pine", "Button mangrove", "Yellow mombin"]	

	#print search_name(commonName, True)
	#print get_scientific_names(input_names)
 	
 	
