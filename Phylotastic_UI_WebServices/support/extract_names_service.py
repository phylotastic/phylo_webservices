#find names service: version 1.0
import json
import time
import requests
import re
import ast
import urllib
import datetime

api_url = "http://gnrd.globalnames.org/name_finder.json?"
headers = {'content-type': 'application/json'}
base_url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/"

#get scientific names from URL
def get_sn_url(inputURL, sEngine=0):
    payload = {
        'url': inputURL,
        'engine': sEngine	
    }
    
    encoded_payload = urllib.urlencode(payload)
    response = requests.get(api_url, params=encoded_payload, headers=headers) 
    
    scientificNamesList = []

    if sEngine == 0:
       service_url = base_url + "names_url?url=" + inputURL
    else:
       service_url = base_url + "names_url?url=" + inputURL + "&engine=" + sEngine
     
    service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-1"

    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
    else:
        return {'input_url': inputURL, 'scientificNames': scientificNamesList,'status_code': 500,
                'service_url': service_url, "service_url_doc": service_documentation, 'message': "Error extracting names using GNRD"} 
    
    token_result = get_token_result(data_json)
    
    if token_result['total'] == 0:
         return {'input_url': inputURL, 'scientificNames': scientificNamesList, 'status_code': 204, 
                 'service_url': service_url, "service_url_doc": service_documentation, 'message': "No scientific names found"} 
    else:
         scientificNamesList = get_sn(token_result['names'])
         parametersList = token_result['parameters']        
         #scientificNamesList = uniquify(all_scientificNamesList) 
         return {'input_url': inputURL, 'parameters': parametersList, 'scientificNames': scientificNamesList, 'status_code': 200, 
                 'service_url': service_url, "service_url_doc": service_documentation, 'message': "Success"} 
     
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
    
    encoded_payload = urllib.urlencode(payload)
    response = requests.get(api_url, params=encoded_payload, headers=headers) 
 
    scientificNamesList = []
    
    if sEngine == 0:
       service_url = base_url + "names_text?text=" + inputTEXT
    else:
       service_url = base_url + "names_text?text=" + inputTEXT + "&engine=" + sEngine
     
    service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-2"    

    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
    else:
        return {'input_text': inputTEXT, 'scientificNames': scientificNamesList, 'status_code': 500, 
                'service_url': service_url, "service_url_doc": service_documentation, 'message': "Error extracting names using GNRD"} 
    
    token_result = get_token_result(data_json)
    
    if token_result['total'] == 0:
         return {'input_text': inputTEXT, 'scientificNames': scientificNamesList, 'status_code': 204, 
                 'service_url': service_url, "service_url_doc": service_documentation, 'message': "No scientific names found"} 
    else:
         scientificNamesList = get_sn(token_result['names'])
         parametersList = token_result['parameters']
         #scientificNamesList = uniquify(all_scientificNamesList) 
         return {'input_text': inputTEXT, 'parameters': parametersList, 'scientificNames': scientificNamesList, 'status_code': 200, 
                 'service_url': service_url, "service_url_doc": service_documentation, 'message': "Success"} 

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
def extract_names_URL(inputURL, sEngine):
    #service execution time
    start_time = time.time()
    final_result = get_sn_url(inputURL, sEngine)    
    end_time = time.time()
    execution_time = end_time-start_time

    #service result creation time
    creation_time = datetime.datetime.now().isoformat()

    final_result['creation_time'] = creation_time
    final_result['execution_time'] = "{:4.2f}".format(execution_time) 
    final_result['total_names'] = len(final_result['scientificNames'])

    return json.dumps(final_result)

def extract_names_TEXT(inputTEXT, sEngine):
    start_time = time.time()
    final_result = get_sn_text(inputTEXT, sEngine)    
    end_time = time.time()
    execution_time = end_time-start_time
    
    #service result creation time
    creation_time = datetime.datetime.now().isoformat()
    final_result['creation_time'] = creation_time
    final_result['execution_time'] = "{:4.2f}".format(execution_time)
    final_result['total_names'] = len(final_result['scientificNames'])
    
    return json.dumps(final_result)	    
   
#--------------------------------------------

#if __name__ == '__main__':
    #inputURL = 'https://en.wikipedia.org/wiki/Aster'    
    #inputURL = 'https://en.wikipedia.org/wiki/Setophaga'
    #inputURL = 'https://species.wikimedia.org/wiki/Morganucodontidae'
    #inputURL = 'https://en.wikipedia.org/wiki/Ant'
    #inputTEXT = 'The Crabronidae are a large paraphyletic group of wasps. Ophiocordyceps, Cordyceps are genus of fungi. The Megalyroidea are a small hymenopteran superfamily that includes a single family, Megalyridae. The Apidae is the largest family within the Apoidea, with at least 5700 species of bees. Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries.'	
    #inputTEXT = "Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries."
    #result = extract_names_URL(inputURL, 0)
    #result = extract_names_TEXT(inputTEXT, 0)    
    #print result
    
