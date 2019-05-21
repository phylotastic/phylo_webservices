#compound service to get trees: version 1.0
import json
import re
import time
import requests
import datetime

#===================================
headers = {'content-type': 'application/json'}
phylotastic_base_url = "https://phylo.cs.nmsu.edu/phylotastic_ws/"

#~~~~~~~~~~~~~~~(Get Tree from Open-Tree_of_Life)~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_tree(taxa_list):
    phylo_service_url = phylotastic_base_url + "gt/ot/tree"
    print taxa_list
    payload = {
        'taxa': taxa_list	
    }
    
    jsonPayload = json.dumps(payload)
    
    #----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool--------------
    try: 
       response = requests.post(phylo_service_url, data=jsonPayload, headers=headers)
       print response.text
    except requests.exceptions.ConnectionError:
       return {'message': "Error: HTTP connection error from phylotastic. Please try again later.", 'status_code': 500}        
    #---------------------------------------------- 
       
    tree_result = {}

    result_data_json = json.loads(response.text)

    if response.status_code == requests.codes.ok:    
       tree_result['newick_tree'] = result_data_json['newick']
       msg =  "Success"
       statuscode = 200
    else:
       msg = result_data_json['message'] if 'message' in result_data_json else "Error from phylotastic service" 
       statuscode = result_data_json['status_code'] if 'status_code' in result_data_json else response.status_code 

    tree_result['message'] =  msg
    tree_result['status_code'] = statuscode

    return tree_result


#-------------------(Get newick tree with common names)-----------------------------
def get_tree_common(newick_str, source, multiple):
    phylo_service_url = phylotastic_base_url + "tc/common_names"
    
    payload = {
        'newick_tree': newick_str,
        'source': source,
        'multiple': multiple
    }
    
    jsonPayload = json.dumps(payload)
    
    #----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool--------------
    try: 
       response = requests.post(phylo_service_url, data=jsonPayload, headers=headers)
    except requests.exceptions.ConnectionError:
       return {'message': "Error: HTTP connection error from phylotastic. Please try again later.", 'status_code': 500}        
    #-----------------------------------------------
    tree_result = {}

    result_data_json = json.loads(response.text)
    print result_data_json
    if response.status_code == requests.codes.ok:    
       tree_result['newick_tree'] = result_data_json['result_tree']
       tree_result['mapping'] = result_data_json['mapping'] 
       msg =  "Success"
       statuscode = 200
    else:
       msg = result_data_json['message'] if 'message' in result_data_json else "Error from phylotastic service" 
       statuscode = result_data_json['status_code'] if 'status_code' in result_data_json else response.status_code 

    tree_result['message'] =  msg
    tree_result['status_code'] = statuscode

    return tree_result

#-------------------------------------------------------
#-------------------(Get scientific names from common names)------------------
def get_scientific_names(name_list, source, multiple=False):
    if source == "NCBI":
        src = "ncbi"
    elif source == "ITIS":
        src = "itis"
    elif source == "EBI":
        src = "ebi"
    else:
        src = "tpcs"

    phylo_service_url = phylotastic_base_url + "cs/"+src+"/scientific_names"
    
    payload = {
        'commonnames': name_list,
        'multiple': multiple
    }
    
    jsonPayload = json.dumps(payload)
    
    #----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool--------------
    try: 
       response = requests.post(phylo_service_url, data=jsonPayload, headers=headers)
    except requests.exceptions.ConnectionError:
       return {'message': "Error: HTTP connection error from phylotastic. Please try again later.", 'status_code': 500}        
    #-----------------------------------------------
    name_map_result = {}

    result_data_json = json.loads(response.text)
    
    if response.status_code == requests.codes.ok:    
       name_map_result['matched_result'] = result_data_json['result']
       msg =  "Success"
       statuscode = 200
    else:
       msg = result_data_json['message'] if 'message' in result_data_json else "Error from phylotastic service" 
       statuscode = result_data_json['status_code'] if 'status_code' in result_data_json else response.status_code 

    name_map_result['message'] =  msg
    name_map_result['status_code'] = statuscode

    return name_map_result

#----------------------------------------------------------
#get tree from scientific names
def get_tree_sc_names(taxa_list, source="GNR", multiple=False):
    start_time = time.time()

    tree_result_json = get_tree(taxa_list)
    response = {}

    if tree_result_json['status_code'] != 200:    
        return tree_result_json   
    else:
        tree_mod_json = get_tree_common(tree_result_json['newick_tree'], source, multiple)
        if tree_mod_json['status_code'] == 200:
           response['newick'] = tree_mod_json['newick_tree']
           response['mapping'] = tree_mod_json['mapping']
        else:
           return tree_mod_json
        
    end_time = time.time()
    execution_time = end_time-start_time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float('{:4.2f}'.format(execution_time)), 'source_urls':["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs"] }

    response['input_list'] = taxa_list
    response['source'] = source
    response['meta_data'] = meta_data
    response['message'] = "Success"
    response['status_code'] = 200

    return response

#--------------------------------------------
def comm_to_sci_names(map_result):
	scientific_names = {}
	for result in map_result:
		bi_scientific_name = None
		sc_name = None
		for match in result['matched_names']:
			sc_name = match['scientific_name']
			sc_name_lst = sc_name.split(" ")
			if len(sc_name_lst) == 2:
				bi_scientific_name = sc_name
				break
			else:
				bi_scientific_name = None
				
		if bi_scientific_name is not None:
			scientific_names[result['searched_name']] = bi_scientific_name 
		else:
			scientific_names[result['searched_name']] = sc_name

	return scientific_names

#----------------------------------------------------------
#get tree from common names
def get_tree_com_names(taxa_list, source="NCBI", multiple=False):
    start_time = time.time()

    name_map_result = get_scientific_names(taxa_list, source, multiple)
    response = {}

    if name_map_result['status_code'] != 200:    
        return name_map_result   
    else:
        com_sc_name_mapping = comm_to_sci_names(name_map_result['matched_result'])
        sc_name_list = list(com_sc_name_mapping.values())
        newick_tree_result = get_tree(sc_name_list)
        # Delete ott_ids from tip_labels
        if 'newick_tree' not in newick_tree_result:
            return {"message": "Error: No tree found.", "status_code": 400} 
        nw_str = newick_tree_result['newick_tree']
        newick_str = re.sub('_ott\d+', "", nw_str)
        newick_tree = newick_str.replace('_', " ")
        #replace all scientific names with common names
        for com_taxa in taxa_list:
            sc_name = com_sc_name_mapping[com_taxa] 
            newick_tree = newick_tree.replace(sc_name, sc_name+"_"+com_taxa)    

        response['newick'] = newick_tree
        response['mapping'] = com_sc_name_mapping
        
    end_time = time.time()
    execution_time = end_time-start_time
    creation_time = datetime.datetime.now().isoformat()
    meta_data = {'creation_time': creation_time, 'execution_time': float('{:4.2f}'.format(execution_time)), 'source_urls':["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs"] }

    response['input_list'] = taxa_list
    response['source'] = source
    response['meta_data'] = meta_data
    response['message'] = "Success"
    response['status_code'] = 200

    return response
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':
 	#sc_list = ["Setophaga striata","Setophaga magnolia","Setophaga angelae","Setophaga plumbea","Setophaga virens"]
	#com_list = ["cattle", "cat", "goat", "pig", "sheep", "duck", "chicken", "horse", "domestic dog"]
    #print get_tree_sc_names(sc_list)
	#print get_tree_com_names(com_list)
