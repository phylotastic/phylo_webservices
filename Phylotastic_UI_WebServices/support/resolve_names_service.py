#resolver service: version 2
import json
import time
import requests
import re
import ast
import urllib


api_url = "http://resolver.globalnames.org/name_resolvers.json?"
headers = {'content-type': 'application/json'}

#~~~~~~~~~~~~~~~~~~~~ (GlobalNamesResolver-TNRS)~~~~~~~~~~~~~~~~~~~~~~~~~~~
#resolve scientific names
def resolve_sn_gnr(scNames, post):
    payload = {
        'names': scNames,
        'best_match_only': 'true'
    }
    
    encoded_payload = urllib.urlencode(payload)
    response = requests.get(api_url, params=encoded_payload, headers=headers) 
    
    resolvedNamesList = [] 
    
    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
        rsnames_list = data_json['data']
        for element in rsnames_list:
            rsname = element['results'][0]['canonical_form']       
 	    namesList = {}
 	    namesList['matched_name'] =  rsname
            namesList['search_string'] = element['supplied_name_string']
 	    namesList['match_type'] = 'Exact' if element['results'][0]['match_type'] == 1 else 'Fuzzy'
 	    namesList['synonyms'] = []
 	    namesList['taxon_id'] = element['results'][0]['taxon_id']	
            namesList['resolver_name'] = 'GNR'
 	    resolvedNamesList.append(namesList)
    
    if post: 	    
        return {'resolvedNames': resolvedNamesList}
    else:
        return json.dumps({'resolvedNames': resolvedNamesList}) 
        
#----------------------------------------------    

#~~~~~~~~~~~~~~~~~~~~ Process Scientific Names List ~~~~~~~~~~~~~~~~~~~~~~~~~~~
def make_api_friendly_list(scNamesList):
    #process list    
    ListSize = len(scNamesList)    
    
    count = 0;
    TobeResolvedNames = ''
    
    for str_element in scNamesList:
        count += 1
        if(count != ListSize):
            str_element += '||' 
        TobeResolvedNames += str_element
    
    #print "List size:"+ str(ListSize)    
    return TobeResolvedNames
                

#~~~~~~~~~~~~~~~~~~~~ (OpenTree-TNRS)~~~~~~~~~~~~~~~~~~~~~~~~~~~
def resolve_sn_ot(scNames, do_fuzzy_match, multi_match, post):
    opentree_api_url = 'https://api.opentreeoflife.org/v2/tnrs/match_names'
    
    payload = {
        'names': scNames,
 		'do_approximate_matching': do_fuzzy_match
    }
    jsonPayload = json.dumps(payload)
   
    response = requests.post(opentree_api_url, data=jsonPayload, headers=headers)
    
    resolvedNamesList = []

    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
        rsnames_list = data_json['results'] 
        resolvedNamesList = get_resolved_names(rsnames_list, do_fuzzy_match, multi_match)
        #write_result(resolvedNamesList)
    
    if post: 	    
     	return {'resolvedNames': resolvedNamesList}
    else: 
        return json.dumps({'resolvedNames': resolvedNamesList}) 

#-------------------------------------------
def get_resolved_names(results, do_fuzzy_match, multi_match):
 	resolvedNameslist = []
 	
 	for element in results:
 		match_list = element['matches']
 		
 		for match_result in match_list:
 			namesList = {}
 			search_str = match_result['search_string']
 			match_str = match_result['matched_name']
 			match_type = match_result['is_approximate_match']
 			match_score = match_result['score']
 			ott_id = match_result['ot:ottId']
 			synonyms = match_result['synonyms']
 			if float(match_score) > 0.5:	     	
 				namesList['matched_name'] = match_str
 				namesList['search_string'] = search_str	 
 				namesList['match_type'] = 'Exact' if not(match_type) else 'Fuzzy'
 				namesList['synonyms'] = synonyms
 				namesList['taxon_id'] = ott_id
 				namesList['resolver_name'] = 'OT'	
 				resolvedNameslist.append(namesList)
 				if not(multi_match) and do_fuzzy_match:
 					break;
 	#print len(resolvedNameslist)
 	return resolvedNameslist

#--------------------------------------------
def resolve_names_OT(inputNamesList, do_fuzzy_match=True, multi_match=False, post=False): 

    final_result = resolve_sn_ot(inputNamesList, do_fuzzy_match, multi_match, post)    
    
    return final_result

#-----------------------------------------------------------
def resolve_names_GNR(inputNamesList, post=False): 
    
    api_friendly_list = make_api_friendly_list(inputNamesList)	
    final_result = resolve_sn_gnr(api_friendly_list, post)    
    
    return final_result

#------------------------------------------------------
def write_result(final_result):
    result_file = open('tnrs_response.txt', 'w')
    result_file.write(str(final_result))
    result_file.close()

#---------------------------------------        
def read_input():
 	with open('tnrs_input.txt', 'r') as f:
 		read_data = f.read()
 	return read_data
#-------------------------------------------------
#if __name__ == '__main__':

    #inputList = ["Astar"]
    #inputList = ["Setophaga plambea", "Setophaga angilae", "Setophaga magnolia", "Setophaga strieta", "Setophaga virens"] 
    #print result
    #st_time = time.time()
    #result = resolve_names_OT(inputList, True, True)
    #en_time = time.time()
    #print en_time-st_time
    
       
