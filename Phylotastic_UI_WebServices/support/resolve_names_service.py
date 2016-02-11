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
'''
#get the final-api result using the token
def get_token_result(response_json):
        
    #get the token value from token url
    token_url = response_json['token_url']
    tokenURL, token = token_url.split('=', 1)
    str_token = str(token);
    
    #wait for the token to be activated    
    #print "Waiting for the token to be activated"    
    #time.sleep(20)
    
    payload = {
        'token': str_token,
    }
    #print str_token
    
    encoded_payload = urllib.urlencode(payload)
    
    while True:
        token_result = requests.get(api_url, params=encoded_payload, headers=headers) 
        result_json = json.loads(token_result.text)
        if token_result.status_code == result_json['status']:
           return result_json 
'''

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
def resolve_sn_ot(scNames, post):
    opentree_api_url = 'https://api.opentreeoflife.org/v2/tnrs/match_names'
    
    payload = {
        'names': scNames
    }
    jsonPayload = json.dumps(payload)
   
    response = requests.post(opentree_api_url, data=jsonPayload, headers=headers)
    
    resolvedNamesList = []

    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
        rsnames_list = data_json['results'] 
        for element in rsnames_list:
            rsname_json = element['matches'][0]
            rsname = rsname_json['matched_name']
 	    namesList = {}
 	    namesList['matched_name'] = rsname_json['matched_name']
 	    namesList['search_string'] = rsname_json['search_string']	 
            namesList['match_type'] = 'Exact' if rsname_json['is_approximate_match'] else 'Fuzzy'
            namesList['synonyms'] = rsname_json['synonyms']
 	    namesList['taxon_id'] = rsname_json['ot:ottId']
 	    namesList['resolver_name'] = 'OT'	
 	    resolvedNamesList.append(namesList)
 	            
    if post: 	    
     	return {'resolvedNames': resolvedNamesList}
    else: 
        return json.dumps({'resolvedNames': resolvedNamesList}) 

#--------------------------------------------
def resolve_names_OT(inputNamesList, post=False): 

    final_result = resolve_sn_ot(inputNamesList, post)    
    
    return final_result

#-----------------------------------------------------------
def resolve_names_GNR(inputNamesList, post=False): 
    
    api_friendly_list = make_api_friendly_list(inputNamesList)	
    final_result = resolve_sn_gnr(api_friendly_list, post)    
    
    return final_result
        
#-------------------------------------------------
if __name__ == '__main__':

    inputList = ["Formica aquilonia", "Formica dirksi", "Formica exsectoides", "Formica pacifica", "Formica sanguinea", "Formicidae"]
    #inputList = ["Setophaga plambea", "Setophaga angilae", "Setophaga magnolia", "Setophaga strieta", "Setophaga virens"]
    result = resolve_names_GNR(inputList)    
    print result
    result = resolve_names_OT(inputList)
    print result
    
       
