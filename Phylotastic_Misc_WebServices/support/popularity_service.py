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
        'names': [taxon]	
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

    msg =  "Success"
    statuscode = 200

    result_data_json = json.loads(response.text)

    if response.status_code == requests.codes.ok:
        if len(result_data_json['results'])!= 0:    
            ott_id = result_data_json['results'][0]['matches'][0]['ot:ottId']
            taxon_match_result['ott_id'] = ott_id
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
   
    if taxon == "biota":
       ott_id = 93302  	#"all life"
    else:
       match_taxon_result = get_ott_id(taxon)
       if match_taxon_result['status_code'] != 200:
          return match_taxon_result
       else:
          ott_id = match_taxon_result['ott_id']
          #print ott_id

    onezoom_result = onezoom_single_taxon_api(ott_id, num_taxa)
    
    final_result = {}
    if onezoom_result['status_code'] != 200:    
        final_result = onezoom_result   
    else:
        final_result['popular_species'] = onezoom_result['popular_species']
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
#if __name__ == '__main__':
	#print get_popular_species("no taxon",10)
