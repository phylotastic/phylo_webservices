#resolver service: version 2.0
import json
import time
import requests
import re
import ast
import urllib
import datetime
import types

import google_dns

#-------------------------------------------------------------------
api_url = "https://resolver.globalnames.org/name_resolvers.json?"
headers = {'content-type': 'application/json'}
#base_url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/"

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
            #print element
            if 'results' not in element:
               continue
            match_list = element['results']
            for match in match_list:
                if match is None:
                   continue
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

    #print resolvedNamesList
    return {'resolvedNames': resolvedNamesList, 'gnr_parameters': parameters_list, 'status_code': statuscode, 'message': msg}
        
#----------------------------------------------    

#Process Scientific Names List for GNR
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
                
#-----------------------------------------------------
#Process Scientific Names List for iPlant
def make_iplant_api_friendly_list(scNamesList):
    #process list for iPlant api    
    ListSize = len(scNamesList)    
    
    count = 0;
    TobeResolvedNames = ''
    
    for str_element in scNamesList:
        count += 1
        if(count != ListSize):
            str_element += ',' 
        TobeResolvedNames += str_element
    
    #print "List size:"+ str(ListSize)    
    return TobeResolvedNames


#~~~~~~~~~~~~~~~~~~~~ (iplantcollaborative-TNRS)~~~~~~~~~~~~~~~~~~~~~~~~~~~
#resolve scientific names using iplantcollaborative
def resolve_sn_iplant(scNames, do_fuzzy_match, multi_match):
    """
    Source: http://tnrs.iplantcollaborative.org/api.html
    """
    iplant_api_url = "http://tnrs.iplantc.org/tnrsm-svc/matchNames"

    if do_fuzzy_match:
       match_type = 'all'  #'all' retrieves all matches
    else:
       match_type = 'best' #'best' retrieves only the single best match for each name submitted

    payload = {
        'names': scNames,
        'retrieve': match_type
    }
    
    encoded_payload = urllib.urlencode(payload)
    response = requests.get(iplant_api_url, params=encoded_payload) 
    #print response.text
    
    resolvedNamesList = [] 
    data_json = json.loads(response.text)

    if response.status_code == requests.codes.ok:  
        rsnames_list = data_json['items']
        
        #get the group numbers
        group_list = []
        for element in rsnames_list:
            if int(element['group']) not in group_list: 
               group_list.append(int(element['group']))

        #find the multiple matches of the same item 
        for group in group_list:
            match_list = []
            for rsn in rsnames_list:
                if int(rsn['group']) == group:
                   match_list.append(rsn)
                
            mult_matches_list = []
            for matched_element in match_list:
                namesList = {} 
                input_name = matched_element['nameSubmitted']
                match_score = float(matched_element['scientificScore'])
                taxon_url = matched_element['url']
                if match_score >= 0.5:
                   rs_name = matched_element['nameScientific']
       	           namesList['search_string'] = input_name
                   namesList['matched_name'] =  rs_name
                   namesList['match_type'] = 'Exact' if match_score == 1 else 'Fuzzy'
                   namesList['data_source'] = "Tropicos - Missouri Botanical Garden"      
                   namesList['synonyms'] = []
                   namesList['match_score'] = match_score  
                   namesList['taxon_id'] = taxon_url[taxon_url.rfind("/")+1:len(taxon_url)]		
                   mult_matches_list.append(namesList)	
               
                if not(multi_match) and do_fuzzy_match:
                   break
               
                if not(do_fuzzy_match) and match_score != 1:
                   continue
 
            resolvedNamesList.append({'input_name': input_name, 'matched_results': mult_matches_list})		

        statuscode = 200
        msg = "Success" 
    else:
        if 'message' in data_json:
           msg = "iPlantcollaborative Error: "+data_json['message']

        else:
           msg = "Error: Response error while resolving names with iPlantcollaborative"
        if 'status' in data_json:
           statuscode = data_json['status']
        
        statuscode = response.status_code   

    return {'resolvedNames': resolvedNamesList, 'status_code': statuscode, 'message': msg}
        
#----------------------------------------------    

#~~~~~~~~~~~~~~~~~~~~ (OpenTreeofLife-TNRS)~~~~~~~~~~~~~~~~~~~~~~~~~~~
def resolve_sn_ot(scNames, do_fuzzy_match, multi_match):
    opentree_api_url = 'https://api.opentreeoflife.org/v3/tnrs/match_names'
  
    payload = {
        'names': scNames,
 		'do_approximate_matching': do_fuzzy_match
    }
    jsonPayload = json.dumps(payload)

    #----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool due to DNS resolver problem--------------
    #+++++++++++Solution 1++++++++++++++++
    #max_tries = 20
    #remaining_tries = max_tries
    #while remaining_tries > 0:
    #    try:
    #        response = requests.post(opentree_api_url, data=jsonPayload, headers=headers)
    #        break
    #    except requests.exceptions.ConnectionError:
    #        time.sleep(20)
    #    remaining_tries = remaining_tries - 1   
    #++++++++++++++++++++++++++++++++++++++
    #+++++++++++Solution 2++++++++++++++++
    try: 
       response = requests.post(opentree_api_url, data=jsonPayload, headers=headers)
    except requests.exceptions.ConnectionError:
       alt_url = google_dns.alt_service_url(opentree_api_url)
       response = requests.post(alt_url, data=jsonPayload, headers=headers, verify=False)        
    #----------------------------------------------
    #response = requests.post(opentree_api_url, data=jsonPayload, headers=headers)
    
    data_json = json.loads(response.text)

    resolvedNamesList = []

    if response.status_code == requests.codes.ok:    
        rsnames_list = data_json['results'] 
        resolvedNamesList = get_resolved_names(rsnames_list, do_fuzzy_match, multi_match)
        statuscode = 200
        msg = "Success"
    else:
        if 'message' in data_json:
           msg = "OToL TNRS API Error: "+data_json['message']
        else:
           msg = "OToL API Error: Response error while resolving names with OToL TNRS"
        if 'status' in data_json:
           statuscode = data_json['status']
        
        statuscode = response.status_code   
        
    return {'resolvedNames': resolvedNamesList, 'status_code': statuscode, 'message': msg}
 
#-------------------------------------------
def get_resolved_names(results, do_fuzzy_match, multi_match):
 	resolvedNameslist = []
 	
 	for element in results:
 		input_name = element['name']
 		match_list = element['matches']
 		mult_matches_list = []
 		for match_result in match_list:
 			namesList = {}
 			search_str = match_result['search_string']
 			match_str = match_result['matched_name']
 			match_type = match_result['is_approximate_match']
 			match_score = match_result['score']
 			ott_id = match_result['taxon']['ott_id']
 			synonyms = match_result['taxon']['synonyms']
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
    list_size = 1000
    final_result = []

    start_time = time.time()
    
    status_code = 200
    message = "Success"

    if len(inputNamesList) > list_size:
    	sublists = create_sublists(inputNamesList, list_size)
        print "Number of sublists: %d"%len(sublists)
    	for sublst in sublists:
    		resolvedResult = resolve_sn_ot(sublst, do_fuzzy_match, multi_match)
    		resolvedNameslst = resolvedResult['resolvedNames']
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

    #return {'resolvedNames': final_result, 'total_names': result_len, 'status_code': status_code, 'input_names': inputNamesList , 'message': message, 'meta_data': meta_data}
    return {'resolvedNames': final_result, 'total_names': result_len, 'status_code': status_code, 'message': message, 'meta_data': meta_data}

#-----------------------------------------------------------
def resolve_names_GNR(inputNamesList, do_fuzzy_match, multi_match): 
    list_size = 3000
    resolver_result = []

    status_code = 200
    message = "Success"
    final_result = {}
    start_time = time.time()

    if len(inputNamesList) > list_size:
 		sublists = create_sublists(inputNamesList, list_size)
 		#print "Number of sublists: %d"%len(sublists)
 		for sublst in sublists:
 			api_friendly_list = make_api_friendly_list(inputNamesList)
 			resolvedResult = resolve_sn_gnr(api_friendly_list, do_fuzzy_match, multi_match)
 			resolvedNameslst = resolvedResult['resolvedNames']
    		 
    		if resolvedResult['status_code'] != 200:
    			return {'status_code': resolvedResult['status_code'], 'message': resolvedResult['message']}
    		resolver_result.extend(resolvedNameslst)  
    else:
        api_friendly_list = make_api_friendly_list(inputNamesList)	
        resolvedResult = resolve_sn_gnr(api_friendly_list, do_fuzzy_match, multi_match)
    	resolver_result = resolvedResult['resolvedNames']
    	status_code = resolvedResult['status_code']
    	message = resolvedResult['message']
     
    result_len = len(resolver_result)
    if result_len <= 0 and status_code == 200:
        final_result['message'] = "Could not resolve any name"

    end_time = time.time()
    execution_time = end_time-start_time

    #service result creation time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["https://resolver.globalnames.org/"] }
#"service_documentation": service_documentation}
    final_result['resolvedNames'] = resolver_result 
    final_result['meta_data'] = meta_data
    final_result['total_names'] = result_len
    final_result['status_code'] = status_code
    final_result['message'] = message
    
    return final_result

#-------------------------------------------------
def resolve_names_iPlant(inputNamesList, do_fuzzy_match, multi_match): 
    
    start_time = time.time()
    api_friendly_list = make_iplant_api_friendly_list(inputNamesList)	
    final_result = resolve_sn_iplant(api_friendly_list, do_fuzzy_match, multi_match)    
    end_time = time.time()
    execution_time = end_time-start_time

    result_len = len(final_result['resolvedNames'])
    if result_len <= 0 and final_result['status_code'] == 200:
        final_result['message'] = "Could not resolve any name"

    #service_documentation = ""
    #service result creation time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["http://tnrs.iplantcollaborative.org"] }
#"service_documentation": service_documentation}
    final_result['meta_data'] = meta_data
    final_result['total_names'] = result_len
    #final_result['input_names'] = inputNamesList
    
    return final_result
    
#-------------------------------------------------
if __name__ == '__main__':

    #inputList = ["Formica polyctena", "Tetramorium caespitum","Carebara diversa", "Formicinae"]
    #inputList = ["Setophaga plambea", "Setophaga angilae", "Setophaga magnolia", "Setophaga strieta", "Setophaga virens"]
    inputList = ["Dionaea muscipula", "Sarracenia", "Darlingtonia californica", "Drosera", "Pinguicula", "Utricularia", "Roridulaceae"]
    #inputList = ["Ran Temporaria"]
    #result = resolve_names_GNR(inputList, True, True)    
    #print result
    
    result = resolve_names_OT(inputList, True, True)
    print result
    
       
