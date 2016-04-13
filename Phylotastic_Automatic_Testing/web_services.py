import urllib2
import urllib
import datetime
import json
import requests
import os
import sys
import subprocess
#Define Resources URI for Testing Web Service
#https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
WS_1_RESOURCES_URI = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url";
WS_1_HEADER = {'content-type':'application/json'};

WS_2_RESOURCES_URI = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_text";
WS_2_HEADER = {'content-type':'application/json'};

WS_3_RESOURCES_URL_GET = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve"
WS_3_HEADER = {'content-type':'application/json'}

WS_3_RESOURCES_URL_POST = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/names"
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
    response = requests.get(WS_2_RESOURCES_URI, params=encoded_param_structure, headers=WS_2_HEADER)
    if (response.status_code == requests.codes.ok):
       ws2_json_result = response.text
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
       print("Error : Exit 2")
       return False
       exit(1)
def testService_ResolveScientificNamesOpenTreeWS_WS_3_GET(param_names,expected_output):
    param_structure = {
    	'names' : param_names
    }
    encoded_param_structure = urllib.urlencode(param_structure)
    response = requests.get(WS_3_RESOURCES_URL_GET, params=encoded_param_structure, headers=WS_3_HEADER)
    if (response.status_code == requests.codes.ok):
       ws3_json_result = response.text
       if (isJSON(str(ws3_json_result)) == False):
           print("Error : Web Service 3's result is not JSON Format")
           exit(1)
       print("Pass : Returned data is JSON format")
       json_object = json.loads(str(ws3_json_result))
       if (type(json_object["resolvedNames"]) is not list):
           print("Error : JSON format is not correct")
           exit(1)
       print("Pass : Returned data contains object 'resolvedNames'")
       #Check correct output data
       set_expected_ouput = set(expected_output)
       set_result = set(json_object["resolvedNames"][0]["synonyms"])
       if (not set_expected_ouput.issubset(set_result)):
           print("Error : Web Service's result could be in-correct");
           exit(1)
       print("Pass : Returned data contains expected output")
       return True
    else:
       print("Error : Exit 3")
       return False
       exit(1)
def testService_ResolveScientificNamesOpenTreeWS_WS_3_POST(json_param_names,expected_output):
    data = json_param_names
    url = WS_3_RESOURCES_URL_POST
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    result_cmd = ""
    for x in f:
        result_cmd = str(x)
        break
    f.close()

    if (isJSON(str(result_cmd)) == False):
        print("Error : Web Service 3's result is not JSON Format")
        exit(1)
    print("\nPass : Returned data is JSON format")
    json_object = json.loads(str(result_cmd))
    if (type(json_object["resolvedNames"]) is not list):
        print("Error : JSON format is not correct")
        exit(1)
    print("Pass : Returned data contains object 'resolvedNames'")
    #Check correct output data
    set_expected_ouput = set(expected_output)
    set_result = set(json_object["resolvedNames"][0]["synonyms"])
    if (not set_expected_ouput.issubset(set_result)):
        print("Error : Web Service's result could be in-correct");
        exit(1)
    print("Pass : Returned data contains expected output")
    return True
