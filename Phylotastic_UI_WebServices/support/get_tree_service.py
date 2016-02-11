import json
import time
import requests
import re
import ast

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
api_url = "https://api.opentreeoflife.org/v2/tree_of_life/"
headers = {'content-type': 'application/json'}
    
#--------------Most Recent Common Ancestor(MRCA) of a set of nodes [OpenTree]--------------
def get_MRCA_id(ottidList):
    resource_url = api_url + "mrca"    
    
    payload_data = {
     	'ott_ids': ottidList
    }
    jsonPayload = json.dumps(payload_data)
    
    response = requests.post(resource_url, data=jsonPayload, headers=headers)
    
    mrca_list = []
    
    if response.status_code == requests.codes.ok:    
        data_json = json.loads(response.text)
  	mrca_info = {}
 	mrca_info['ott_name'] = data_json['nearest_taxon_mrca_name']       
 	mrca_info['ott_id'] = data_json['nearest_taxon_mrca_ott_id']
        mrca_list.append(mrca_info)
    
    return mrca_list 
    
#-------------------Subtree of a node [OpenTree]------------------------
#input: ottid(long) of one node
#output: subtree in newick format (string)
def get_Subtree(ottId):
    resource_url = api_url + "subtree"    
    
    payload_data = {
     	'ott_id': ottId
    }
    jsonPayload = json.dumps(payload_data)
    
    response = requests.post(resource_url, data=jsonPayload, headers=headers)
        
    newick_tree_str = ''

    if response.status_code == requests.codes.ok:
    	data_json = json.loads(response.text)
     	newick_tree_str = data_json['newick']
    
    return newick_tree_str

#-----------------Induced Subtree of a set of nodes [OpenTree]---------------------
#input: list (comma separated) of ottids (long)   
#output: subtree in newick format (string)
def get_inducedSubtree(ottIdList):
    resource_url = api_url + "induced_subtree"    
    
    payload_data = {
     	'ott_ids': ottIdList
    }
    jsonPayload = json.dumps(payload_data)
    
    response = requests.post(resource_url, data=jsonPayload, headers=headers)
        
    newick_tree_str = ''

    if response.status_code == requests.codes.ok:
    	data_json = json.loads(response.text)
     	newick_tree_str = data_json['newick']
    
    return newick_tree_str

#-------------------------------------------------------
def subtree(ottidList):
    #single species
    if len(ottidList) == 1:
       ottid = ottidList[0]
       return get_Subtree(ottid)
    #multiple species
    mrca_info = get_MRCA_id(ottidList)
    if len(mrca_info) == 0:
    	return ''
    mrca_ottid = mrca_info[0]['ott_id']
    newick_str = get_Subtree(mrca_ottid) 

    return newick_str

#-----------------------------------------------------------
#get newick string for tree from OpenTree
#input: list of resolved scientific names
def get_tree_OT(resolvedNames, post=False):
    ListSize = len(resolvedNames)
    if ListSize == 0:
  	return create_json_msg('','List of resolved names empty')
    
    rsnames = resolvedNames
    #rsnames = resolvedNames['resolvedNames']
    ottIdList = []
    for rname in rsnames:
        if rname['resolver_name'] == 'OT':
    	   ottIdList.append(rname['taxon_id']) 	
 	else:     
 	   return create_json_msg('', 'Wrong TNRS. Need to resolve with OpenTree TNRS')
     
    final_result = create_json_msg('', 'No Tree found')

    #first try to get subtree
    final_tree = subtree(ottIdList)

    if len(final_tree) == 0:
	#subtree method failed, try inducedsubtree
        final_tree = get_inducedSubtree(ottIdList)
        if len(final_tree) == 0:
           final_result = create_json_msg(final_tree, 'No Tree found')     
 	else:
           final_result = create_json_msg(final_tree, 'Induced subtree method used')
    else:
 	final_result = create_json_msg(final_tree, 'Subtree method used')
    
    if post: 	    
        return final_result
    else:
        return json.dumps(final_result) 

#-----------------------------------------------------
def create_json_msg(newick, status):
    result = {}
    result['newick'] = newick
    result['message'] = status

    return result       	

#-------------------------------------------

if __name__ == '__main__':

    #inputOttIds = [3597195, 3597205, 3597191, 3597209, 60236]
    #inputNames = {"resolvedNames": [{"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga striata", "search_string": "setophaga strieta", "synonyms": ["Dendroica striata", "Setophaga striata"], "taxon_id": 60236}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Setophaga magnolia", "search_string": "setophaga magnolia", "synonyms": ["Dendroica magnolia", "Setophaga magnolia"], "taxon_id": 3597209}, {"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga angelae", "search_string": "setophaga angilae", "synonyms": ["Dendroica angelae", "Setophaga angelae"], "taxon_id": 3597191}, {"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga plumbea", "search_string": "setophaga plambea", "synonyms": ["Dendroica plumbea", "Setophaga plumbea"], "taxon_id": 3597205}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Setophaga virens", "search_string": "setophaga virens", "synonyms": ["Dendroica virens", "Setophaga virens"], "taxon_id": 3597195}]}

    #inputNames = {"resolvedNames": [{"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Formicidae", "search_string": "formicidae", "synonyms": ["Formicidae", "ants", "Formicoidea"], "taxon_id": 215086}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Formica dirksi", "search_string": "formica dirksi", "synonyms": ["Formica dirksi"], "taxon_id": 3261229}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Formica aquilonia", "search_string": "formica aquilonia", "synonyms": ["Formica aquilonia"], "taxon_id": 62158}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Formica sanguinea", "search_string": "formica sanguinea", "synonyms": ["Formica sanguinea"], "taxon_id": 704977}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Formica exsectoides", "search_string": "formica exsectoides", "synonyms": ["Formica exsectoides"], "taxon_id": 3261265}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Formica pacifica", "search_string": "formica pacifica", "synonyms": ["Formica pacifica"], "taxon_id": 3261024}]}
    
    #inputNames = {"resolvedNames": [{"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Crabronidae", "search_string": "crabronidae", "synonyms": ["Crabronidae"], "taxon_id": 372234}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Tetramorium caespitum", "search_string": "tetramorium caespitum", "synonyms": ["Tetramorium caespitum"], "taxon_id": 214421}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Ophiocordyceps", "search_string": "ophiocordyceps", "synonyms": ["Ophiocordyceps"], "taxon_id": 843906}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Megalyridae", "search_string": "megalyridae", "synonyms": ["Megalyridae"], "taxon_id": 840287}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Apidae", "search_string": "apidae", "synonyms": ["Apidae"], "taxon_id": 52848}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Formica polyctena", "search_string": "formica polyctena", "synonyms": ["Formica polyctenum", "Formica polyctena"], "taxon_id": 815730}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Carebara diversa", "search_string": "carebara diversa", "synonyms": ["Pheidologeton diversus", "Carebara diversus", "Carebara diversa"], "taxon_id": 842045}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Cordyceps", "search_string": "cordyceps", "synonyms": ["Akrophyton", "Racemella", "Campylothecium", "Phytocordyceps", "Tettigorhyza", "Hypoxylum", "Torrubia", "Cordyliceps", "Polistophthora", "Mitrasphaera", "Cordyceps", "Corynesphaera", "Cordylia"], "taxon_id": 64408}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Adetomyrma venatrix", "search_string": "adetomyrma venatrix", "synonyms": ["Adetomyrma venatrix"], "taxon_id": 4538021}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Pseudomyrmex", "search_string": "pseudomyrmex", "synonyms": ["Pseudomyrmex"], "taxon_id": 412943}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Apoidea", "search_string": "apoidea", "synonyms": ["bees", "Apoidea", "bee"], "taxon_id": 419526}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Formicinae", "search_string": "formicinae", "synonyms": ["Formicinae"], "taxon_id": 614614}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Megalyroidea", "search_string": "megalyroidea", "synonyms": ["Megalyroidea"], "taxon_id": 365543}]}
    
    inputNames = {"resolvedNames": [{"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Crabronidae", "search_string": "crabronidae", "synonyms": ["Crabronidae"], "taxon_id": 372234}]} 

    result = get_tree_OT(inputNames) 
    print result
    
       
