import urllib2
import urllib
import datetime
import json
import requests
#Define Resources URI for Testing Web Service
#https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
WS_1_RESOURCES_URI = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url";
WS_1_HEADER = {'content-type':'application/json'};

WS_2_RESOURCES_URI = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_text";
WS_2_HEADER = {'content-type':'application/json'};
#-------------------------------------------------------------------------------
#Each function is testing tool for each Web Service in document
#https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
def isJSON(string):
    try:
       json_object = json.loads(string)
    except ValueError, e:
       return False
    return True
def testService_FindScientificNamesOnWebPages_WS_1(param_url,expected_output):
    param_structure = {
    	'url' : param_url
    }
    encoded_param_structure = urllib.urlencode(param_structure)
    response = requests.get(WS_1_RESOURCES_URI, params=encoded_param_structure, headers=WS_1_HEADER)
    if (response.status_code == requests.codes.ok):
       ws1_json_result = response.text
       #print "Web Service 1 : FindScientificNames Result : %s " %(str(ws1_json_result))
       #Check output data of web service is correct and consistent : JSON format, code == 200,existed JSON object scientificNames
       if (isJSON(str(ws1_json_result)) == False):
           print("Error : Web Service 1's result is not JSON Format")
           exit(1)
       print("Pass : Returned data is JSON format")
       json_object = json.loads(str(ws1_json_result))
       if (type(json_object["scientificNames"]) is not list):
           print("Error : JSON format is not correct")
           exit(1)
       print("Pass : Returned data contains object 'scientificNames'")
       #Check correct output data
       set_expected_ouput = set(expected_output)
       set_result = set(json_object["scientificNames"])
       if (not set_expected_ouput.issubset(set_result)):
           print("Error : Web Service's result could be in-correct");
           exit(1)
       print("Pass : Returned data contains expected output")
       return True
    else:
       print("Error : Exit 1")
       return False
       exit(1)
def testService_FindScientificNamesOnText_WS_2(param_text,expected_output):
    param_structure = {
    	'text' : param_text
    }
    encoded_param_structure = urllib.urlencode(param_structure)
    response = requests.get(WS_2_RESOURCES_URI, params=encoded_param_structure, headers=WS_1_HEADER)
    if (response.status_code == requests.codes.ok):
       ws2_json_result = response.text
       #print "Web Service 1 : FindScientificNames Result : %s " %(str(ws1_json_result))
       #Check output data of web service is correct and consistent : JSON format, code == 200,existed JSON object scientificNames
       if (isJSON(str(ws2_json_result)) == False):
           print("Error : Web Service 2's result is not JSON Format")
           exit(1)
       print("Pass : Returned data is JSON format")
       json_object = json.loads(str(ws2_json_result))
       if (type(json_object["scientificNames"]) is not list):
           print("Error : JSON format is not correct")
           exit(1)
       print("Pass : Returned data contains object 'scientificNames'")
       #Check correct output data
       set_expected_ouput = set(expected_output)
       set_result = set(json_object["scientificNames"])
       if (not set_expected_ouput.issubset(set_result)):
           print("Error : Web Service's result could be in-correct");
           exit(1)
       print("Pass : Returned data contains expected output")
       return True
    else:
       print("Error : Exit 1")
       return False
       exit(1)
