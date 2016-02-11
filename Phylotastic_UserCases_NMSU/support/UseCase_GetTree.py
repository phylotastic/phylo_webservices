import json
import time
import requests
import re
import ast
import urllib

headers = {'content-type': 'application/json'}

# ~~~~~~~~~~~~~~~~~~~~~ WebService1 ~~~~~~~~~~~~~~~~~~~~~~~~~
# WebService1: findnames.wsdl
#inputs: text to be extracted for scientific names   
#output: list of scientific names in string

def run_webservice1(ws1_input, funcName):

    service_Url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/"
    service_func = 'names_'+funcName
    resource_url = service_Url + service_func
    service_param = funcName
    
    payload = {
    	funcName : ws1_input
    }
    
    encoded_payload = urllib.urlencode(payload)
    
    response = requests.get(resource_url, params=encoded_payload, headers=headers)
    
    ws1_json_result = response.text
    
    return ws1_json_result

# ~~~~~~~~~~~~~~~~~~~~~ WebService2 ~~~~~~~~~~~~~~~~~~~~~~~~~
# WebService2: opentree_tnrs.wsdl
#input: list of scientific names in string
#output: list of resolved scientific names in string

def run_webservice2(ws2_input):
    resource_url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/names"
    #print ws2_input
    response = requests.post(resource_url, data=ws2_input, headers=headers)
    
    if response.status_code == requests.codes.ok:    
    	return response.text
    else:
        return 'error:' + response.status_code
    
    
#~~~~~~~~~~~~~~~~~~~~ WebService3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# WebService3: opentree_tree.wsdl
#input: list of resolved scientific names in string
#output: newick string of the tree

def run_webservice3(ws3_input):
    resource_url = 'http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/tree'
    
    response = requests.post(resource_url, data=ws3_input, headers=headers)
    
    if response.status_code == requests.codes.ok:    
    	return response.text
    else:
        return 'error:' + response.status_code


#-----------------------------------------------------------

def run_UseCase(usecase_input, ucaseno):
    
    if ucaseno == 1:    
       funcname = 'text'
    else:
       funcname = 'url'
    
    #print "Executing webservice1"
    ws1_result = run_webservice1(usecase_input, funcname)
    
    #print "Executing webservice2"
    ws2_result = run_webservice2(ws1_result)    
    
    #print "Executing webservice3"
    ws3_result = run_webservice3(ws2_result)
    
    ws3_json_result = json.loads(ws3_result) 
    
    if ws3_json_result['newick'] == '':
 	final_result = ws3_json_result['message']
    else:
        final_result = ws3_json_result['newick'] 
    
    return final_result

#--------------------------------------------
if __name__ == '__main__':

    #usercase_Input = 'https://en.wikipedia.org/wiki/Plain_pigeon'
    #usercase_Input = 'https://en.wikipedia.org/wiki/Lemon_dove'
    #usercase_Input = 'https://en.wikipedia.org/wiki/Aster'
    #usercase_Input = 'https://species.wikimedia.org/wiki/Morganucodontidae'
    #usercase_Input = 'The Crabronidae are a large paraphyletic group of wasps. Ophiocordyceps, Cordyceps are genus of fungi. The Megalyroidea are a small hymenopteran superfamily that includes a single family, Megalyridae. The Apidae is the largest family within the Apoidea, with at least 5700 species of bees. Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries.'
    usercase_Input = 'Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries.'
    #1 = text  2= url
    usecase_result = run_UseCase(usercase_Input, 1)    
    
    print usecase_result
    
       
