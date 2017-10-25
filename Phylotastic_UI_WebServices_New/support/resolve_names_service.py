#resolver service: version 2.0
import json
import time
import requests
import re
import ast
import urllib
import datetime
import types

#-------------------------------------------------------------------
api_url = "http://resolver.globalnames.org/name_resolvers.json?"
headers = {'content-type': 'application/json'}
base_url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/"

#~~~~~~~~~~~~~~~~~~~~ (GlobalNamesResolver-TNRS)~~~~~~~~~~~~~~~~~~~~~~~~~~~
#resolve scientific names
def resolve_sn_gnr(scNames, do_fuzzy_match, multi_match):
    if do_fuzzy_match:
       best_match = 'false'
    else:
       best_match = 'true'

    payload = {
        'names': scNames,
        'best_match_only': best_match
    }
    
    #encoded_payload = urllib.urlencode(payload)
    #response = requests.get(api_url, params=encoded_payload, headers=headers) 
    response = requests.post(api_url, data=payload)     

    resolvedNamesList = [] 
    data_json = json.loads(response.text)

    if response.status_code == requests.codes.ok:        
        rsnames_list = data_json['data']
        parameters_list = data_json['parameters']   
        for element in rsnames_list:
            mult_matches_list = []
            input_name = element['supplied_name_string']
            
            match_list = element['results']
            for match in match_list:
                namesList = {}
                
                if float(match['score']) >= 0.75:
                   rsname = match['canonical_form']
       	           namesList['search_string'] = input_name
            	   namesList['matched_name'] =  rsname
            	   namesList['match_type'] = 'Exact' if match['match_type'] == 1 else 'Fuzzy'
                   namesList['data_source'] = match['data_source_title']      
            	   namesList['synonyms'] = []
                   namesList['match_score'] = match['score']  
            	   namesList['taxon_id'] = match['taxon_id']		
                   mult_matches_list.append(namesList)	
                if not(multi_match) and do_fuzzy_match: 
                   break

            if not do_fuzzy_match and match['match_type'] !=1:
               continue
            resolvedNamesList.append({'input_name': input_name, 'matched_results': mult_matches_list})
		
        statuscode = 200
        msg = "Success" 
    else:
        if 'message' in data_json:
           msg = "GNR Error: "+data_json['message']
        else:
           msg = "Error: Response error while resolving names with GNR"
        if 'status' in data_json:
           statuscode = data_json['status']
        
        statuscode = response.status_code   

    print resolvedNamesList
    return {'resolvedNames': resolvedNamesList, 'gnr_parameters': parameters_list, 'status_code': statuscode, 'message': msg}
        
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
                

#~~~~~~~~~~~~~~~~~~~~ (OpenTreeofLife-TNRS)~~~~~~~~~~~~~~~~~~~~~~~~~~~
def resolve_sn_ot(scNames, do_fuzzy_match, multi_match):
    opentree_api_url = 'https://api.opentreeoflife.org/v2/tnrs/match_names'
  
    payload = {
        'names': scNames,
 		'do_approximate_matching': do_fuzzy_match
    }
    jsonPayload = json.dumps(payload)
   
    response = requests.post(opentree_api_url, data=jsonPayload, headers=headers)
    
    data_json = json.loads(response.text)

    resolvedNamesList = []

    if response.status_code == requests.codes.ok:    
        rsnames_list = data_json['results'] 
        resolvedNamesList = get_resolved_names(rsnames_list, do_fuzzy_match, multi_match)
        statuscode = 200
        msg = "Success"
    else:
        if 'message' in data_json:
           msg = "OToL TNRS Error: "+data_json['message']
        else:
           msg = "Error: Response error while resolving names with OToL TNRS"
        if 'status' in data_json:
           statuscode = data_json['status']
        
        statuscode = response.status_code   
        
    return {'resolvedNames': resolvedNamesList, 'status_code': statuscode, 'message': msg}
 
#-------------------------------------------
def get_resolved_names(results, do_fuzzy_match, multi_match):
 	resolvedNameslist = []
 	
 	for element in results:
 		input_name = element['id']
 		match_list = element['matches']
 		mult_matches_list = []
 		for match_result in match_list:
 			namesList = {}
 			search_str = match_result['search_string']
 			match_str = match_result['matched_name']
 			match_type = match_result['is_approximate_match']
 			match_score = match_result['score']
 			ott_id = match_result['ot:ottId']
 			synonyms = match_result['synonyms']
 			if float(match_score) >= 0.75:	     	
 				namesList['matched_name'] = match_str
 				namesList['search_string'] = search_str	 
 				namesList['match_type'] = 'Exact' if not(match_type) else 'Fuzzy'
 				namesList['match_score'] = match_score          
 				namesList['synonyms'] = synonyms
 				namesList['taxon_id'] = ott_id
 				namesList['data_source'] = "Open Tree of Life Reference Taxonomy"
 				mult_matches_list.append(namesList)	
 			if not(multi_match) and do_fuzzy_match: 
 				break

 		resolvedNameslist.append({'input_name': input_name, 'matched_results': mult_matches_list})

 	#print len(resolvedNameslist)
 	return resolvedNameslist

#---------------------------------
def create_sublists(lst, size=200):
	return [lst[i:i+size] for i in xrange(0, len(lst), size)]

#--------------------------------------------
def resolve_names_OT(inputNamesList, do_fuzzy_match, multi_match): 
    list_size = 250
    final_result = []

    start_time = time.time()
    
    status_code = 200
    message = "Success"

    if len(inputNamesList) > list_size:
    	sublists = create_sublists(inputNamesList, list_size)
    	for sublst in sublists:
    		resolvedResult = resolve_sn_ot(sublst, do_fuzzy_match, multi_match)
    		resolvedNameslst = resolvedResult['results']
    		if resolvedResult['status_code'] != 200:
    			return {'status_code': resolvedResult['status_code'], 'message': resolvedResult['message']}
    		final_result.extend(resolvedNameslst)  
    else:
    	resolvedResult = resolve_sn_ot(inputNamesList, do_fuzzy_match, multi_match)
    	final_result = resolvedResult['resolvedNames']
    	status_code = resolvedResult['status_code']
    	message = resolvedResult['message']

    result_len = len(final_result)

    if result_len <= 0 and status_code == 200:
        message = "Could not resolve any name" 

    end_time = time.time()
    
    #service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-3"
    execution_time = float("{:4.2f}".format(end_time-start_time))
    #service result creation time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': execution_time, 'source_urls':["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tnrs"] }
#"service_documentation": service_documentation}

    return {'resolvedNames': final_result, 'total_names': result_len, 'status_code': status_code, 'input_names': inputNamesList , 'message': message, 'meta_data': meta_data}


#-----------------------------------------------------------
def resolve_names_GNR(inputNamesList, do_fuzzy_match, multi_match): 
    
    start_time = time.time()
    api_friendly_list = make_api_friendly_list(inputNamesList)	
    final_result = resolve_sn_gnr(api_friendly_list, do_fuzzy_match, multi_match)    
    end_time = time.time()
    execution_time = end_time-start_time

    result_len = len(final_result['resolvedNames'])
    if result_len <= 0 and final_result['status_code'] == 200:
        final_result['message'] = "Could not resolve any name"

    #service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-4"
    #service result creation time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["http://resolver.globalnames.org/"] }
#"service_documentation": service_documentation}
    final_result['meta_data'] = meta_data
    final_result['total_names'] = result_len
    final_result['input_names'] = inputNamesList
    
 
    return final_result
    
#-------------------------------------------------
#if __name__ == '__main__':

    #inputList = ["Formica polyctena", "Tetramorium caespitum","Carebara diversa", "Formicinae"]
    #inputList = ["Setophaga plambea", "Setophaga angilae", "Setophaga magnolia", "Setophaga strieta", "Setophaga virens"]
    #inputList = ["Ran Temporaria"]
    #result = resolve_names_GNR(inputList, True, True)    
    #print result
    
    #result = resolve_names_OT(inputList, True, True)
    #print result
    
       
