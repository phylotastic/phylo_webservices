#get tree service: version 2

import json
import time
import requests
import re
import ast
import datetime
#----------------
from ete3 import Tree, TreeStyle
from ete3.parser.newick import NewickError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
api_url = "https://api.opentreeoflife.org/v2/tree_of_life/"
headers = {'content-type': 'application/json'}
    
#-----------------Induced Subtree of a set of nodes [OpenTree]---------------------
#input: list (comma separated) of ottids (long)   
#output: json object with inducedsubtree in newick key and status message in message key
def get_inducedSubtree(ottIdList):
    resource_url = api_url + "induced_subtree"    
    
    payload_data = {
     	'ott_ids': ottIdList
    }
    jsonPayload = json.dumps(payload_data)
    
    response = requests.post(resource_url, data=jsonPayload, headers=headers)
        
    newick_tree_str = ""
    inducedtree_info = {}

    if response.status_code == requests.codes.ok:
 		data_json = json.loads(response.text)
 		newick_tree_str = data_json['newick']		
 		inducedtree_info['message'] = "Success"
 		inducedtree_info['status_code'] = 200
    else:
        #print response.text
        try: 
         	error_json = json.loads(response.text)
         	error_msg = error_json['message']
         	if 'Not enough valid node or ott ids' in error_msg:
 				inducedtree_info['message'] = "Not enough valid node or ott ids provided to construct a subtree (there must be at least two)"
         	else:
 		 		inducedtree_info['message'] = error_msg
         	inducedtree_info['status_code'] = 204
     	except ValueError:
     		inducedtree_info['message'] =  "induced_subtree method: Decoding of JSON error message failed"
     		inducedtree_info['status_code'] = 500 	
    
    inducedtree_info['newick'] = newick_tree_str
 	
    return inducedtree_info

#-------------------------------------------------------
def subtree(ottidList):
    result = {}
    #single species
    if len(ottidList) < 2:
       result['newick'] = ""
       result['message'] = "Not enough valid nodes provided to construct a subtree (there must be at least two)"
       result['status_code'] = 204 
       return result
    
 	#multiple species
    induced_response = get_inducedSubtree(ottidList)
    result = induced_response

    return result 
#-----------------------------------------------------------
#get newick string for tree from OpenTree
#input: list of resolved scientific names
def get_tree_OT(resolvedNames, post=False):
 	start_time = time.time()
 	#service_url = 
 	service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-5"

 	ListSize = len(resolvedNames)
    
 	response = {}
 	if ListSize == 0:
 		response['newick'] = ""
 		response['message'] = "List of resolved names empty"
 		response['status_code'] = 204
 		response['service_documentation'] = service_documentation
 		if post:
 			return response;
 		else:		
 			return json.dumps(response)
    
 	rsnames = resolvedNames
 	#rsnames = resolvedNames['resolvedNames']
 	ottIdList = []
 	for rname in rsnames:
 		if rname['resolver_name'] == 'OT':
 			ottIdList.append(rname['taxon_id'])
 		else:
 			response['newick'] = ""
 			response['message'] = "Wrong TNRS. Need to resolve with OpenTree TNRS"
 			response['status_code'] = 204
 			response['service_documentation'] = service_documentation
 			if post:
 				return response;
 			else:		
 		 		return json.dumps(response)
 	     	     
    #get induced_subtree
 	final_result = subtree(ottIdList)
 	newick_str = final_result['newick']
 
 	if final_result['newick'] != "":
 		synth_tree_version = get_tree_version()		
 		tree_metadata = get_metadata()
 		tree_metadata['inference_method'] = tree_metadata['inference_method'] + " from synthetic tree with ID "+ synth_tree_version
 		final_result['tree_metadata'] = tree_metadata
 		final_result['tree_metadata']['synthetic_tree_id'] = synth_tree_version
 		num_tips = get_num_tips(newick_str)
 		if num_tips != -1:
 			final_result['tree_metadata']['num_tips'] = num_tips
 		study_list = get_supporting_studies(ottIdList) 	
 		final_result['tree_metadata']['supporting_studies'] = study_list['studies']
 		 
 	end_time = time.time()
 	execution_time = end_time-start_time
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	final_result['creation_time'] = creation_time
 	final_result['execution_time'] = "{:4.2f}".format(execution_time)
 	final_result['service_documentation'] = service_documentation

 	if post: 	    
 		return final_result
 	else:
 		return json.dumps(final_result) 

#-------------------------------------------
#get supporting studies of the tree from OpenTree
def get_supporting_studies(ottIdList):
 	resource_url = "http://phylo.cs.nmsu.edu:5006/phylotastic_ws/md/studies"    
    
 	payload_data = {
 		'list': ottIdList,
 		'list_type': "ottids"		
    }
 	jsonPayload = json.dumps(payload_data)
    
 	response = requests.post(resource_url, data=jsonPayload, headers=headers)
        
 	studies_info = {}

 	if response.status_code == requests.codes.ok:
 		data_json = json.loads(response.text)
 		studies_info['studies'] = data_json['studies']		
 		studies_info['message'] = data_json['message']
 		studies_info['status_code'] = data_json['status_code']
 	else:
 		studies_info['studies'] = []		
 		studies_info['message'] = "Error: getting study info from OpenTree"
 		studies_info['status_code'] = 500

 	return studies_info

#--------------------------------------------
#find the number of tips in the tree
def get_num_tips(newick_str):
 	parse_error = False
 	try:
 		tree = Tree(newick_str)
 	except NewickError:
 		try:
 			tree = Tree(newick_str, format=1)
 		except NewickError as e:
 			parse_error = True

 	if not(parse_error):
 		tips_list = [leaf for leaf in tree.iter_leaves()]            
 		tips_num = len(tips_list)
 	else:
 		tips_num = -1

 	return tips_num

#-------------------------------------------
def get_tree_version():
 	resource_url = "https://api.opentreeoflife.org/v2/tree_of_life/about"    
    
 	payload_data = {
 		'study_list': False
 	}
 	jsonPayload = json.dumps(payload_data)
    
 	response = requests.post(resource_url, data=jsonPayload, headers=headers)
        
 	metadata = {}
 	if response.status_code == requests.codes.ok:
 		data_json = json.loads(response.text)
 		return data_json['tree_id']
 	else:
 		return "Error: getting synth tree version"  

#---------------------------------------------
def get_metadata():
 	tree_metadata = {}
 	tree_metadata['topology_id'] = "NA"
 	tree_metadata['gene_or_species'] = "species"
 	tree_metadata['rooted'] = True
 	tree_metadata['anastomosing'] = False
 	tree_metadata['consensus_type'] = "NA"
 	tree_metadata['branch_lengths_type'] = None
 	tree_metadata['branch_support_type'] = None
 	tree_metadata['character_matrix'] = "NA"
 	tree_metadata['alignment_method'] = "NA"
 	tree_metadata['inference_method'] = "induced_subtree"

 	return tree_metadata	
#---------------------------------------------
#if __name__ == '__main__':

    #ott_idlist = [3597195, 3597205, 3597191, 3597209, 60236]
    #inputNames = {"resolvedNames": [{"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga striata", "search_string": "setophaga strieta", "synonyms": ["Dendroica striata", "Setophaga striata"], "taxon_id": 60236}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Setophaga magnolia", "search_string": "setophaga magnolia", "synonyms": ["Dendroica magnolia", "Setophaga magnolia"], "taxon_id": 3597209}, {"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga angelae", "search_string": "setophaga angilae", "synonyms": ["Dendroica angelae", "Setophaga angelae"], "taxon_id": 3597191}, {"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga plumbea", "search_string": "setophaga plambea", "synonyms": ["Dendroica plumbea", "Setophaga plumbea"], "taxon_id": 3597205}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Setophaga virens", "search_string": "setophaga virens", "synonyms": ["Dendroica virens", "Setophaga virens"], "taxon_id": 3597195}]}

    #result = get_inducedSubtree(ott_idlist)
    #result = get_tree_OT(inputNames)
    #print result
    
       
