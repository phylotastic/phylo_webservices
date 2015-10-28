import json
import time
import requests
import re
import ast


url = "http://128.123.177.21:5003/WSExecution/runWSFunctionWithWSDL_json"
ws_Wsdl_Url = "http://128.123.177.13/WSRegistry/sites/default/files/wsdl/"
headers = {'content-type': 'application/json'}


def execute_webservice(jsonPayload):
    response = requests.post(url, data=jsonPayload, headers=headers)
    null_response = {'Result': 'null'} 
    if response.status_code == requests.codes.ok:    
        res_json = json.loads(response.text)
    else:
        res_json = json.dumps(null_response)
    return res_json 
#--------------------------------------------------------

def create_json_payload(wsFunctionName, wsWsdlUrl, wsInputParams):
    payload_data = {}
    payload_data['ws_function_name'] = wsFunctionName
    payload_data['ws_wsdl_url'] = wsWsdlUrl
    payload_data['ws_input_params'] = wsInputParams
    json_payload = json.dumps(payload_data)
    
    return json_payload


#------------------------------------------------
def is_ascii(str_val):
    return bool(re.match(r'[\x00-\x7F]+$', str_val))

# ~~~~~~~~~~~~~~~~~~~~~ WebService1 ~~~~~~~~~~~~~~~~~~~~~~~~~
# WebService1: gnrd.wsdl
#inputs: WSDL function name to run (string), parameter of the function (string)  
#output: token in string

def run_webservice1(wsFuncName, wsFuncParam):
    Wsdl_Url = ws_Wsdl_Url + 'gnrd.wsdl'
    
    ws1ParamsList = [wsFuncParam]
    #create payload for webservice1
    JSONpayload1 = create_json_payload(wsFuncName, Wsdl_Url, ws1ParamsList)
    
    ws1_json_result = execute_webservice(JSONpayload1)
    
    #get the token value from token url
    token_url = ws1_json_result['token_url']
    tokenUrl2, token = token_url.split('=', 1)
    str_token = str(token);
    
    #wait for the token to be activated    
    print "Waiting for the token to be activated"    
    time.sleep(25)
        
    return str_token 


# ~~~~~~~~~~~~~~~~~~~~~ WebService2 ~~~~~~~~~~~~~~~~~~~~~~~~~
# WebService2: gnrdaux.wsdl
#input: token in string
#output: list of scientific names in string

def run_webservice2(token_val):
    Wsdl_Url = ws_Wsdl_Url + 'gnrdaux.wsdl'
    
    ws2ParamsList = [token_val]
    
    #create payload for webservice2
    JSONpayload2 = create_json_payload('getScientificNames', Wsdl_Url, ws2ParamsList)
    
    ws2_json_result = execute_webservice(JSONpayload2)

    ws2_json_names_list = ws2_json_result['names']
 
    scientificNamesList = []
    uclist = []    
    for element in ws2_json_names_list:
        #scName = element['scientificName'].replace(' ', '+')
        scName = element['scientificName']       
        if is_ascii(scName): #check if there is any string with unicode character
            scientificNamesList.append(str(scName))    
        else:         
            uclist.append(scName)
    
    return scientificNamesList; 

"""
#~~~~~~~~~~~~~~~~~~~~ WebService3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# WebService3: gnr.wsdl
def run_webservice3(scNamesList):
    Wsdl_Url = ws_Wsdl_Url + 'gnr.wsdl'
    
    #process list    
    ListSize = len(scNamesList)    
    ListSize = 20 #test    
    
    count = 0;
    TobeResolvedNames = ''
    
    for str_element in scNamesList:
        count += 1
        if(count != ListSize):
            str_element += '||' 
        TobeResolvedNames += str_element
    
    print "List size:"+ str(ListSize)    
    
    ws3ParamsList = [];
    ws3ParamsList.append(TobeResolvedNames);
    ws3ParamsList.append("true");
    
    #create payload for webservice2
    JSONpayload3 = create_json_payload('resolveScientificNames', Wsdl_Url, ws3ParamsList)
    
    print JSONpayload3
        
    ws3_json_result = execute_webservice(JSONpayload3)

    ws3_json_names_list = ws3_json_result['data']
     
    namesList = []
    
    for element in ws3_json_names_list:
        tempList = []
        tempList = element['results']
        for item in tempList:        
            namesList.append(item['name_string'])
    
    resolvedList = list(set(namesList))
    return resolvedList
    
#---------------------------------------------------------
"""

#~~~~~~~~~~~~~~~~~~~~ WebService3 (OpenTreeTNRS)~~~~~~~~~~~~~~~~~~~~~~~~~~~
# WebService3: wsdl_2_restHTTP_OpenTree.wsdl
#input: list of scientific names (string)
#output: list of ottids (string) of resolved names

def run_webservice3(scNamesList):
    Wsdl_Url = ws_Wsdl_Url + 'wsdl_2_restHTTP_OpenTree.wsdl'
     
    ws3ParamsList = scNamesList
    if len(scNamesList) == 0:
        print "No Scientific Names found"
        return []
    
    print 'Matching from Open Tree TNRS....'
    
    #create payload for webservice3
    JSONpayload3 = create_json_payload('TNRS_GetMatchNames_By_names', Wsdl_Url, ws3ParamsList)
        
    ws3_json_result = execute_webservice(JSONpayload3)
    
    #print "Matched names result using OpenTreeTNRS"    
    #print json.dumps(ws3_json_result)
    
    ws3_json_names_list = ws3_json_result['results']
         
    namesList = []
    ottidList = []
    
    for element in ws3_json_names_list:
        tempList = []
        tempList = element['matches']
        for item in tempList:        
            namesList.append(item['matched_name'])
            ottidList.append(str(item['ot:ottId']))
        #resolvedList = list(set(namesList))
    print "Number of names matched:" + str(len(ottidList)) 
    
    return ottidList    

    
#--------------Most Recent Common Ancestor(MRCA) of a set of nodes--------------

def get_MRCA(ottidList):
    Wsdl_Url = ws_Wsdl_Url + 'wsdl_2_restHTTP_OpenTree.wsdl'
    #print 'OTTIDs:'    
    #print ottidList
        
    JSONpayload32 = create_json_payload('OpenTree_GetMRCA_By_ott_ids', Wsdl_Url, ottidList)
    ws32_json_result = execute_webservice(JSONpayload32)
    
    ott_id = ws32_json_result['nearest_taxon_mrca_ott_id']
    
    print "MRCA ottid:" + str(ott_id)
    
    return ott_id 

"""       
#-----------------------Subtree----------------------------------
#input: ottid(long) of one node
#output: subtree in newick format (string)

def get_Subtree(ottId):
    Wsdl_Url = ws_Wsdl_Url + 'wsdl_2_restHTTP_OpenTree.wsdl'    
    print "Get the subtree"
    str_ott_id = str(ott_id)
        
    ws33ParamsList = [str_ott_id]       
    
    JSONpayload33 = create_json_payload('OpenTree_GetSubTree_By_ott_id', Wsdl_Url, ws33ParamsList)
            
    ws33_json_result = execute_webservice(JSONpayload33)
    
    return ws33_json_result

"""
#----------------------Induced Subtree---------------------------------
#input: list of ottids in string
#output: subtree in newick format (string)

def get_inducedSubtree(ottIdList):
    Wsdl_Url = ws_Wsdl_Url + 'wsdl_2_restHTTP_OpenTree.wsdl'    
    
    if(len(ottIdList)==0):
        print "No tree found"
        return "empty tree"
    print "Get the induced subtree"     
    
    str_ottids = ''
    ListSize = len(ottIdList)
    count = 0
    print str(ListSize) 
    
    for ottid in ottIdList:        
        count +=1        
        str_ottids += ottid             
        if(count != ListSize):
            str_ottids += ','
            
    ws34ParamsList = [str_ottids]
    print ws34ParamsList
    JSONpayload34 = create_json_payload('OpenTree_GetInducedSubTree_By_ott_ids', Wsdl_Url, ws34ParamsList)
                
    ws34_json_result = execute_webservice(JSONpayload34)    
    
    result_tree = str(ws34_json_result['newick'])
    
    return result_tree

#-----------------------------------------------------------

def run_usecase2(inputURL):
    print "Executing webservice1"
    ws1_result = run_webservice1('findScientificNamesWithURL', inputURL)
    
    print "Executing webservice2"
    ws2_result = run_webservice2(ws1_result)    
    
    print "Executing webservice3"
    ws3_result = run_webservice3(ws2_result)
    
    final_result = get_inducedSubtree(ws3_result)    
    
    return final_result

#--------------------------------------------
#if __name__ == '__main__':

    #inputURL = 'https://species.wikimedia.org/wiki/Vulpes_vulpes_vulpes'    
#    inputURL = 'https://en.wikipedia.org/wiki/Setophaga'
    #inputURL = 'https://species.wikimedia.org/wiki/Morganucodontidae'
#    usecase2_result = run_usecase2(inputURL)
#    print "Result:"    
#    print usecase2_result
    
       