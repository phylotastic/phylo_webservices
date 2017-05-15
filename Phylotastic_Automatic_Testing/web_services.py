import urllib2
import urllib
import datetime
import json
import requests
import os
import sys
import subprocess
from newick import loads

#Define Resources URI for Testing Web Service
#https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
WS_1_RESOURCES_URI = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url";
WS_1_HEADER = {'content-type':'application/json'};

WS_2_RESOURCES_URI = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_text";
WS_2_HEADER = {'content-type':'application/json'};

WS_3_RESOURCES_URL_GET = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve"
WS_3_HEADER = {'content-type':'application/json'}
WS_3_RESOURCES_URL_POST = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/names"

WS_4_RESOURCES_URL_GET = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/gnr/resolve"
WS_4_HEADER = {'content-type':'application/json'}
WS_4_RESOURCES_URL_POST = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/gnr/names"

WS_5_RESOURCES_URL_GET = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/get_tree"
WS_5_HEADER = {'content-type':'application/json'}
WS_5_RESOURCES_URL_POST = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/tree"

WS_6_RESOURCES_URL_GET = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/all_species"
WS_6_HEADER = {'content-type':'application/json'}

WS_7_RESOURCES_URL_GET = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/country_species"
WS_7_HEADER = {'content-type':'application/json'}

WS_8_RESOURCES_URL_GET = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/get_images"
WS_8_HEADER = {'content-type':'application/json'}
WS_8_RESOURCES_URL_POST = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/images"

WS_9_RESOURCES_URL_GET = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi/genome_species"
WS_9_HEADER = {'content-type':'application/json'}
WS_9_RESOURCES_URL_POST = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi/genome_species"

TV_RESOURCES_URL = "http://phylo.cs.nmsu.edu:8989/status"
TV_HEADER = {'content-type': "text/html"}
#-------------------------------------------------------------------------------
#Each function is testing tool for each Web Service in document
#https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
def isJSON(string):
    try:
       json_object = json.loads(string)
    except ValueError, e:
       return False
    return True
def isNewick(string):
    try:
        newick_data = loads(string)
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
       list_result = []
       for index, item in enumerate(json_object["resolvedNames"]):
           list_result.append(json_object["resolvedNames"][index]["matched_name"])

       set_result = set(list_result)
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
    list_result = []
    for index, item in enumerate(json_object["resolvedNames"]):
        list_result.append(json_object["resolvedNames"][index]["matched_name"])

    set_result = set(list_result)
    if (not set_expected_ouput.issubset(set_result)):
        print("Error : Web Service's result could be in-correct");
        exit(1)
    print("Pass : Returned data contains expected output")
    return True
def testService_ResolveScientificNamesGNR_TNRS_WS_4_GET(param_names,expected_output):
    param_structure = {
    	'names' : param_names
    }
    encoded_param_structure = urllib.urlencode(param_structure)
    response = requests.get(WS_4_RESOURCES_URL_GET, params=encoded_param_structure, headers=WS_4_HEADER)
    if (response.status_code == requests.codes.ok):
       ws4_json_result = response.text
       if (isJSON(str(ws4_json_result)) == False):
           print("Error : Web Service 4's result is not JSON Format")
           exit(1)
       print("Pass : Returned data is JSON format")
       json_object = json.loads(str(ws4_json_result))
       if (type(json_object["resolvedNames"]) is not list):
           print("Error : JSON format is not correct")
           exit(1)
       print("Pass : Returned data contains object 'resolvedNames'")
       #Check correct output data
       set_expected_ouput = set(expected_output)
       list_result = []
       for index, item in enumerate(json_object["resolvedNames"]):
           list_result.append(json_object["resolvedNames"][index]["matched_name"])
       set_result = set(list_result)
       if (not set_expected_ouput.issubset(set_result)):
           print("Error : Web Service's result could be in-correct");
           exit(1)
       print("Pass : Returned data contains expected output")
       return True
    else:
       print("Error : Exit 4")
       return False
       exit(1)
def testService_ResolveScientificNamesGNR_TNRS_WS_4_POST(json_param_names,expected_output):
    data = json_param_names
    url = WS_4_RESOURCES_URL_POST
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    result_cmd = ""
    for x in f:
        result_cmd = str(x)
        break
    f.close()

    if (isJSON(str(result_cmd)) == False):
        print("Error : Web Service 4's result is not JSON Format")
        exit(1)
    print("\nPass : Returned data is JSON format")
    json_object = json.loads(str(result_cmd))
    if (type(json_object["resolvedNames"]) is not list):
        print("Error : JSON format is not correct")
        exit(1)
    print("Pass : Returned data contains object 'resolvedNames'")
    #Check correct output data
    set_expected_ouput = set(expected_output)
    list_result = []
    for index, item in enumerate(json_object["resolvedNames"]):
        list_result.append(json_object["resolvedNames"][index]["matched_name"])

    set_result = set(list_result)
    if (not set_expected_ouput.issubset(set_result)):
        print("Error : Web Service's result could be in-correct");
        exit(1)
    print("Pass : Returned data contains expected output")
    return True
def testService_GetPhylogeneticTreeFrom_OpenTree_5_GET(param_taxa,expected_output):
    param_structure = {
    	'taxa' : param_taxa
    }
    encoded_param_structure = urllib.urlencode(param_structure)
    response = requests.get(WS_5_RESOURCES_URL_GET, params=encoded_param_structure, headers=WS_5_HEADER)
    if (response.status_code == requests.codes.ok):
       ws5_json_result = response.text
       if (isJSON(str(ws5_json_result)) == False):
           print("Error : Web Service 5's result is not JSON Format")
           exit(1)
       print("Pass : Returned data is JSON format")
       json_object = json.loads(str(ws5_json_result))
       if ((json_object["message"] != "Success") and (json_object["newick"] is None or json_object["newick"] == "")):
           print("Error : JSON format is not correct")
           exit(1)
       print("Pass : Returned data contains object 'message' and 'newick'")
       #Check correct output data
       tree_data = json_object["newick"]
       if (not isNewick(tree_data)):
           print("Error : Web Service's result is NOT a Newick tree");
           exit(1)
       print("Pass : Returned data is Newick tree")
       if (str(tree_data).strip().upper() == str(expected_output).strip().upper()):
           print("Pass : Returned data contains expected output")
           return True
       else:
           print("Error : Web Service's result could be in-correct")
           return False
    else:
       print("Error : Exit 4")
       return False
       exit(1)
def testService_GetPhylogeneticTreeFrom_OpenTree_5_POST(json_param_taxa,expected_output):
    data = json_param_taxa
    url = WS_5_RESOURCES_URL_POST
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    result_cmd = ""
    for x in f:
        result_cmd = str(x)
        break
    f.close()

    ws5_json_result = result_cmd
    if (isJSON(str(ws5_json_result)) == False):
        print("Error : Web Service 5's result is not JSON Format")
        exit(1)
    print("Pass : Returned data is JSON format")
    json_object = json.loads(str(ws5_json_result))
    if ((json_object["message"] != "Success") and (json_object["newick"] is None or json_object["newick"] == "")):
        print("Error : JSON format is not correct")
        exit(1)
    print("Pass : Returned data contains object 'message' and 'newick'")
    #Check correct output data
    tree_data = json_object["newick"]
    if (not isNewick(tree_data)):
        print("Error : Web Service's result is NOT a Newick tree");
        exit(1)
    print("Pass : Returned data is Newick tree")
    if (str(tree_data).strip().upper() == str(expected_output).strip().upper()):
        print("Pass : Returned data contains expected output")
        return True
    else:
        print("Error : Web Service's result could be in-correct")
        return False
def testService_GetAllSpeciesFromATaxon_WS_6(param_taxon,expected_output):
    param_structure = {
    	'taxon' : param_taxon
    }
    encoded_param_structure = urllib.urlencode(param_structure)
    response = requests.get(WS_6_RESOURCES_URL_GET, params=encoded_param_structure, headers=WS_6_HEADER)
    if (response.status_code == requests.codes.ok):
       ws6_json_result = response.text
       if (isJSON(str(ws6_json_result)) == False):
           print("Error : Web Service 6's result is not JSON Format")
           exit(1)
       print("Pass : Returned data is JSON format")
       json_object = json.loads(str(ws6_json_result))
       if (type(json_object["species"]) is not list):
           print("Error : JSON format is not correct")
           exit(1)
       print("Pass : Returned data contains object 'species'")
       #Check correct output data
       set_expected_ouput = set(expected_output)
       set_result = set(json_object["species"])
       if (not set_expected_ouput.issubset(set_result)):
           print("Error : Web Service's result could be in-correct");
           exit(1)
       print("Pass : Returned data contains expected output")
       return True
    else:
       print("Error : Exit 1")
       return False
       exit(1)
def testService_GetAllSpeciesFromATaxonFilteredByCountry_WS_7(param_taxon,param_country,expected_output):
    param_structure = {
    	'taxon' : param_taxon,
        'country' : param_country
    }
    encoded_param_structure = urllib.urlencode(param_structure)
    response = requests.get(WS_7_RESOURCES_URL_GET, params=encoded_param_structure, headers=WS_7_HEADER)
    if (response.status_code == requests.codes.ok):
       ws7_json_result = response.text
       if (isJSON(str(ws7_json_result)) == False):
           print("Error : Web Service 7's result is not JSON Format")
           exit(1)
       print("Pass : Returned data is JSON format")
       json_object = json.loads(str(ws7_json_result))
       if (type(json_object["species"]) is not list):
           print("Error : JSON format is not correct")
           exit(1)
       print("Pass : Returned data contains object 'species'")
       #Check correct output data
       set_expected_ouput = set(expected_output)
       print set_expected_ouput
       set_result = set(json_object["species"])
       print set_result
       if (not set_expected_ouput.issubset(set_result)):
           print("Error : Web Service's result could be in-correct");
           exit(1)
       print("Pass : Returned data contains expected output")
       return True
    else:
       print("Error : Exit 1")
       return False
       exit(1)
def testService_GetImagesURLListOfSpecies_WS_8_GET(param_species,expected_output):
    param_structure = {
    	'species' : param_species
    }
    encoded_param_structure = urllib.urlencode(param_structure)
    response = requests.get(WS_8_RESOURCES_URL_GET, params=encoded_param_structure, headers=WS_8_HEADER)
    if (response.status_code == requests.codes.ok):
       ws8_json_result = response.text
       if (isJSON(str(ws8_json_result)) == False):
           print("Error : Web Service 8's result is not JSON Format")
           exit(1)
       print("Pass : Returned data is JSON format")
       json_object = json.loads(str(ws8_json_result))
       if (type(json_object["species"][0]["images"]) is not list):
           print("Error : JSON format is not correct")
           exit(1)
       if ((json_object["status_code"] is None) or (json_object["status_code"] == "")):
           print("Error : JSON format is not correct")
           exit(1)
       print("Pass : Returned data contains object 'species' 'images'")
       #Check correct output data
       set_expected_ouput = set(expected_output)
       #print set_expected_ouput
       img_objs = []
       for imgs in json_object["species"]:
            for img in imgs["images"]: 
                img_objs.append(str(img["eolMediaURL"]))
       #set_result = set(json_object["species"][0]["images"])
       set_result = set(img_objs)
       #print set_result
       if (not set_expected_ouput.issubset(set_result)):
            print("Error : Web Service's result could be in-correct")
            exit(1)
       #if (json_object["species"][0]["images"][0]["eolMediaURL"] != expected_output):
       #    print("Error : Web Service's result could be in-correct");
       #    exit(1)
       print("Pass : Returned data contains expected output")
       return True
    else:
       print("Error : Exit 1")
       return False
       exit(1)
def testService_GetImagesURLListOfSpecies_WS_8_POST(json_param_species,expected_output):
    data = json_param_species
    url = WS_8_RESOURCES_URL_POST
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    result_cmd = ""
    for x in f:
        result_cmd = str(x)
        break
    f.close()

    ws8_json_result = result_cmd
    if (isJSON(str(ws8_json_result)) == False):
        print("Error : Web Service 8's result is not JSON Format")
        exit(1)
    print("Pass : Returned data is JSON format")
    json_object = json.loads(str(ws8_json_result))
    if ((json_object["message"] != "Success") or (type(json_object["species"][0]["images"]) is not list)):
        print("Error : JSON format is not correct")
        exit(1)
    print("Pass : Returned data contains object 'species' 'images'")
    #Check correct output data
    if (json_object["species"][0]["images"][0]["eolMediaURL"] != expected_output):
        print("Error : Web Service's result could be in-correct");
        exit(1)
    print("Pass : Returned data contains expected output")
    return True
def testService_GetSpeciesNCBI_WS_9_GET(param_taxon,expected_output):
    param_structure = {
    	'taxon' : param_taxon
    }
    encoded_param_structure = urllib.urlencode(param_structure)
    response = requests.get(WS_9_RESOURCES_URL_GET, params=encoded_param_structure, headers=WS_9_HEADER)
    if (response.status_code == requests.codes.ok):
       ws9_json_result = response.text
       if (isJSON(str(ws9_json_result)) == False):
           print("Error : Web Service 9's result is not JSON Format")
           exit(1)
       print("Pass : Returned data is JSON format")
       json_object = json.loads(str(ws9_json_result))
       if (type(json_object["species"]) is not list):
           print("Error : JSON format is not correct")
           exit(1)
       if ((json_object["status_code"] is None) or (json_object["status_code"] == "")):
           print("Error : JSON format is not correct")
           exit(1)
       print("Pass : Returned data contains object 'species'")
       #Check correct output data
       set_expected_ouput = set(expected_output)
       set_result = set(json_object["species"])
       if (not set_expected_ouput.issubset(set_result)):
          print("Error : Web Service's result could be in-correct");
          exit(1)

       print("Pass : Returned data contains expected output")
       return True
    else:
       print("Error : Exit 1")
       return False
       exit(1)
#---------------------------------------------------------------
def testService_TreeViewer_Alive():
    response = requests.get(TV_RESOURCES_URL, headers=TV_HEADER)
    if (response.status_code == requests.codes.ok):
       tv_result = response.text
       
       #Check correct output data
       if (tv_result != "alive"):
          print("Error : the Tree viewer web Service is not alive");
          return False
          exit(1)

       print("Pass : TreeViewer webservice is alive")
       return True
    else:
       print("Error : Exit 1")
       return False
       exit(1)
