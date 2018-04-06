#GNRD wrapper: Find scientific names service: version 1.0
import json
import time
import requests
import re
import ast
import urllib
import datetime

#------------------------------------------------
api_url = "http://gnrd.globalnames.org/name_finder.json?"
headers = {'content-type': 'application/json'}
base_url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/"

#-------------------------------------------------
#get scientific names from URL
def get_sn_url(inputURL, sEngine=0):
    payload = {
        'url': inputURL,
        'engine': sEngine	
    }
    
    encoded_payload = urllib.urlencode(payload)
    response = requests.get(api_url, params=encoded_payload, headers=headers) 
    
    scientificNamesList = []
    try: 
       if response.status_code == requests.codes.ok:    
          data_json = json.loads(response.text)
       else:
          data_json = json.loads(response.text)
          if 'message' in data_json:
             msg = "GNRD Error: "+data_json['message']
          else:
             msg = "Error: Response error while extracting names using GNRD"
          if 'status' in data_json:
             statuscode = data_json['status']
          else:
             statuscode = 500

          return {'input_url': inputURL, 'scientificNames': scientificNamesList, 'status_code': statuscode, 'message': msg} 
    
    except ValueError:
          return {'input_url': inputURL, 'scientificNames': [], 'status_code': 500, 'message': "No JSON object could be decoded from GNRD response"}      

    token_result = get_token_result(data_json)
    
    if token_result['total'] == 0:
         return {'input_url': inputURL, 'scientificNames': scientificNamesList, 'status_code': 200, 'message': "No scientific names found"} 
    else:
         scientificNamesList = get_sn(token_result['names'])
         parametersList = token_result['parameters']        
         #scientificNamesList = uniquify(all_scientificNamesList) 
         return {'input_url': inputURL, 'gnrd_parameters': parametersList, 'scientificNames': scientificNamesList, 'status_code': 200, 'message': "Success"} 
     
#----------------------------------------------    
#get scientific names from final api-result
def get_sn(namesList):
    snlist = []
    uclist = []    
    for sn in namesList:
        #scName = element['scientificName'].replace(' ', '+')
        scName = sn['scientificName']       
        if is_ascii(scName): #check if there is any string with unicode character
            # Remove any parenthesis
            scName = re.sub(r'[()]', "", scName)
            if scName not in snlist: # Check for duplicate
               snlist.append(str(scName))    
        #else:         
        #    uclist.append(scName)
    
    return snlist; 

#------------------------------------------------
def is_ascii(str_val):
    return bool(re.match(r'[\x00-\x7F]+$', str_val))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#get the final-api result using the token
def get_token_result(response_json):
        
    #get the token value from token url
    token_url = response_json['token_url']
    tokenURL, token = token_url.split('=', 1)
    str_token = str(token);
        
    #print "Waiting for the token to be activated"    
    #time.sleep(20)
    
    payload = {
        'token': str_token,
    }
    
    encoded_payload = urllib.urlencode(payload)
    
    while True:
        token_result = requests.get(api_url, params=encoded_payload, headers=headers)
        result_json = json.loads(token_result.text)
        if token_result.status_code == result_json['status']:
           return result_json 

#---------------------------------------------------
#get scientific names from Text
def get_sn_text(inputTEXT, sEngine=0):
    payload = {
        'text': inputTEXT,
        'engine': sEngine
    }
    
    #encoded_payload = urllib.urlencode(payload)
    #response = requests.get(api_url, params=encoded_payload, headers=headers) 
    response = requests.post(api_url, data=payload) 

    scientificNamesList = []
    
    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
    else:
        data_json = json.loads(response.text) 
        if 'message' in data_json:
           msg = "GNRD Error: "+data_json['message']
        else:
           msg = "Error: Response error while extracting names using GNRD"
        if 'status' in data_json:
           statuscode = data_json['status']
        else:
           statuscode = 500

        #return {'input_text': inputTEXT, 'scientificNames': scientificNamesList, 'status_code': statuscode, 'message': msg} 
        return {'scientificNames': scientificNamesList, 'status_code': statuscode, 'message': msg} 
    
    token_result = get_token_result(data_json)
    
    if token_result['total'] == 0:
         return {'scientificNames': scientificNamesList, 'status_code': 200, 'message': "No scientific names found"} 
    else:
         scientificNamesList = get_sn(token_result['names'])
         parametersList = token_result['parameters']
         #scientificNamesList = uniquify(all_scientificNamesList) 
         return {'gnrd_parameters': parametersList, 'scientificNames': scientificNamesList, 'status_code': 200,'message': "Success"} 

#-----------------------------------------------------------
# removes duplicates from a list
'''
def uniquify(lst):
   # order preserving
   checked = []
   for item in lst:
       if item not in checked:
           checked.append(item)
   return checked
'''
#--------------------------------------
def extract_names_URL(inputURL, sEngine=0):
    #service execution time
    start_time = time.time()
    final_result = get_sn_url(inputURL, sEngine)
    
    if final_result['status_code'] != 200:
       return final_result
    
    end_time = time.time()
    execution_time = end_time-start_time

    if sEngine == 0:
       service_url = base_url + "names_url?url=" + inputURL
    else:
       service_url = base_url + "names_url?url=" + inputURL + "&engine=" + str(sEngine)

    service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-1"
    #service result creation time
    creation_time = datetime.datetime.now().isoformat()

    meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["http://gnrd.globalnames.org/"] }

   #'service_documentation': service_documentation} #'service_url': service_url
    final_result['meta_data'] = meta_data
 
    final_result['total_names'] = len(final_result['scientificNames'])

    return final_result  #return json.dumps(final_result)

#-----------------------------------------------------
def extract_names_TEXT(inputTEXT, sEngine=0):
    start_time = time.time()
    final_result = get_sn_text(inputTEXT, sEngine)    
    end_time = time.time()
    execution_time = end_time-start_time
    
    if final_result['status_code'] != 200:
       return final_result
    
    if sEngine == 0:
       service_url = base_url + "names_text?text=" + inputTEXT
    else:
       service_url = base_url + "names_text?text=" + inputTEXT + "&engine=" + str(sEngine)
     
    service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-2"
    
    #service result creation time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["http://gnrd.globalnames.org/"] }
#'service_documentation': service_documentation} #'service_url': service_url
    final_result['meta_data'] = meta_data

    final_result['total_names'] = len(final_result['scientificNames'])
    
    return final_result #return json.dumps(final_result)	    
   

#----------------------TaxonFinder(http://taxonfinder.org/api)------------------------------------
#get scientific names from URL using TaxonFinder 
def get_tf_sn_url(inputURL):
    payload = {
        'url': inputURL	
    }
    
    taxon_finder_api = "http://taxonfinder.org/api/find?"
    #encoded_payload = urllib.urlencode(payload)
    response = requests.get(taxon_finder_api, params=payload) 
    #print response.text
     
    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
    else:
        data_json = json.loads(response.text)
        if 'message' in data_json:
           msg = "TaxonFinder Error: "+data_json['message']
        else:
           msg = "Error: Response error while extracting names using TaxonFinder"
        if 'status' in data_json:
           statuscode = data_json['status']
        else:
           statuscode = 500

        return {'input_url': inputURL, 'scientificNames': scientificNamesList, 'status_code': statuscode, 'message': msg} 
    
    scientificNamesList = get_tf_names(data_json)
    
    if len(scientificNamesList) == 0:
         return {'input_url': inputURL, 'scientificNames': scientificNamesList, 'status_code': 200, 'message': "No scientific names found"} 
    else:
         return {'input_url': inputURL, 'scientificNames': scientificNamesList, 'status_code': 200, 'message': "Success"} 

#-------------------------------------------
#get scientific names from TEXT using TaxonFinder
def get_tf_sn_text(inputTEXT):
    payload = {
        'text': inputTEXT	
    }
    
    taxon_finder_api = "http://taxonfinder.org/api/find?"
    #encoded_payload = urllib.urlencode(payload)
    response = requests.post(taxon_finder_api, data=payload) 
         
    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
    else:
        data_json = json.loads(response.text)
        if 'message' in data_json:
           msg = "TaxonFinder Error: "+data_json['message']
        else:
           msg = "Error: Response error while extracting names using TaxonFinder"
        if 'status' in data_json:
           statuscode = data_json['status']
        else:
           statuscode = 500

        return {'scientificNames': scientificNamesList, 'status_code': statuscode, 'message': msg} 
    
    scientificNamesList = get_tf_names(data_json)
    
    if len(scientificNamesList) == 0:
         return {'scientificNames': scientificNamesList, 'status_code': 200, 'message': "No scientific names found"} 
    else:
         return {'scientificNames': scientificNamesList, 'status_code': 200, 'message': "Success"} 
     
#--------------------------------------------
def get_tf_names(data_json):
    snlist = []
    for element in data_json:
        scName = element['name']
        #print scName
        # Remove any parenthesis
        scName = re.sub(r'[()]', "", scName)
        if scName not in snlist: # Check for duplicate
           snlist.append(str(scName))   
    
    return snlist

#----------------------------------------------
def extract_names_taxonfinder(tf_input, input_type=None):
    start_time = time.time()
    if input_type == 'url':
       final_result = get_tf_sn_url(tf_input)  
    elif input_type == 'text':
       final_result = get_tf_sn_text(tf_input)
    else:
       final_result = {'status_code': 400, 'message': 'Input type parameter missing'}
    
    end_time = time.time()
    execution_time = end_time-start_time
    
    if final_result['status_code'] != 200:
       return final_result
    
    #service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-2"
    
    #service result creation time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["http://taxonfinder.org/"] }
    #'service_documentation': service_documentation} #'service_url': service_url
    final_result['meta_data'] = meta_data

    final_result['total_names'] = len(final_result['scientificNames'])
    
    return final_result	    
      
#--------------------------------------------

#if __name__ == '__main__':
    #inputURL = 'http://en.wikipedia.org/wiki/Sharks'    
    #inputURL = 'https://en.wikipedia.org/wiki/Setophaga'
    #inputURL = 'https://species.wikimedia.org/wiki/Morganucodontidae'
    #inputURL = 'https://en.wikipedia.org/wiki/Ant'
    #inputTEXT = 'The Crabronidae are a large paraphyletic group of wasps. Ophiocordyceps, Cordyceps are genus of fungi. The Megalyroidea are a small hymenopteran superfamily that includes a single family, Megalyridae. The Apidae is the largest family within the Apoidea, with at least 5700 species of bees. Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries.'	
    #inputTEXT = "Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries."
    #result = extract_names_URL(inputURL, 0)
    #result = extract_names_TEXT(inputTEXT, 0)    
    #result = extract_names_taxonfinder(inputTEXT, 'text')
    #print result
    
