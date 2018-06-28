#popularity service: version 1.0
import json
import time
import requests
import datetime

import google_dns
#===================================

#~~~~~~~~~~~~~~~~~~~~ (OpenTreeofLife-TNRS)~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_ott_id(taxon):
    opentree_url = "https://api.opentreeoflife.org/v2/tnrs/match_names"
    
    payload = {
        'names': [taxon],
        'do_approximate_matching': False	
    }
    
    jsonPayload = json.dumps(payload)
    
    #response = requests.post(opentree_url, data=jsonPayload, headers={'content-type': 'application/json'})
    #----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool--------------
    try: 
       response = requests.post(opentree_url, data=jsonPayload, headers={'content-type': 'application/json'})
    except requests.exceptions.ConnectionError:
       alt_url = google_dns.alt_service_url(opentree_url)
       response = requests.post(alt_url, data=jsonPayload, headers={'content-type': 'application/json'}, verify=False)        
    #----------------------------------------------     

    taxon_match_result = {}
    match_results = []

    msg =  "Success"
    statuscode = 200

    result_data_json = json.loads(response.text)

    if response.status_code == requests.codes.ok:
        if len(result_data_json['results'])!= 0:    
            matches = result_data_json['results'][0]['matches']
            for match in matches:
               taxon_match = {}
               taxon_match['unique_name'] = match['unique_name']
               taxon_match['ott_id'] = match['ot:ottId']
               match_results.append(taxon_match)
            taxon_match_result['match_result'] = match_results
        else:
            statuscode = 400
            msg = "No taxon matched with name '%s'"%taxon   
    else:
        if 'message' in result_data_json:
           msg = "OpenTree Error: "+result_data_json['message']
        else:
           msg = "Error: Response error while matching taxons using OpenTreeofLife API"
        
        statuscode = response.status_code
         
    taxon_match_result['message'] =  msg
    taxon_match_result['status_code'] = statuscode

    return taxon_match_result

#---------------------------------------------------------
def onezoom_single_taxon_api(taxon_ott_id, max_taxa):
    onezoom_url = "http://beta.onezoom.org/popularity/list"

    payload = {
       'expand_taxa': 1,
       'key': 0, 
       'max': max_taxa,
       'names': 1,
       'otts': taxon_ott_id	
    }
    
    response = requests.get(onezoom_url, params=payload)
    #print response.text

    popular_species_list = []

    result_data_json = json.loads(response.text)
    msg =  "Success"
    statuscode = 200

    if response.status_code == requests.codes.ok:
        if len(result_data_json['data'])!= 0:    
           popular_species_list = extract_species(result_data_json['data'])
    else:
        msg = "Error: Response error while retrieving popular species using OneZoom API"
        statuscode = response.status_code

    return {'popular_species': popular_species_list, 'message': msg, 'status_code': statuscode}

#---------------------------------------------
def extract_species(result_data):
    popular_species = []    	
    for item in result_data:
        species_obj = {}
        species_obj['name'] = item[3]
        species_obj['rank'] = item[2]
        species_obj['score'] = item[1] #float('{:10.2f}'.format(item[1]))
        species_obj['ott_id'] = item[0]
        popular_species.append(species_obj)

    return popular_species

#----------------------------------------------------------
def get_popular_species(taxon="biota", num_taxa=20):
    start_time = time.time()
    final_result = {}
    results = []
    if taxon == "biota":
       ott_id = 93302  	#"all life"
       onezoom_result = onezoom_single_taxon_api(ott_id, num_taxa)
       results.append({'matched_taxon': "cellular organisms", 'ott_id': ott_id, 'popular_species': onezoom_result['popular_species']})
    else:
       match_taxon_result = get_ott_id(taxon)
       if match_taxon_result['status_code'] != 200:
          return match_taxon_result
       else:
          taxon_matches = match_taxon_result['match_result']
          for match in taxon_matches:
             ott_id = match['ott_id']
             onezoom_result = onezoom_single_taxon_api(ott_id, num_taxa)
             if onezoom_result['status_code'] == 200:
                #if len(onezoom_result['popular_species']) != 0:    
                results.append({'matched_taxon': match['unique_name'], 'ott_id': ott_id, 'popular_species': onezoom_result['popular_species']}) 
             else:
                return onezoom_result          

    final_result['result'] = results
    final_result['message'] = "Success"     
    final_result['status_code'] = 200

    end_time = time.time()
    execution_time = end_time-start_time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float('{:4.2f}'.format(execution_time)), 'source_urls':["http://beta.onezoom.org"] }

    final_result['meta_data'] = meta_data
    final_result['input_taxon'] = taxon

    return final_result
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
	print get_popular_species("Anura",10)
