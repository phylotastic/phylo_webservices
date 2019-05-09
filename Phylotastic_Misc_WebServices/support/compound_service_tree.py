#compound service to get trees: version 1.0
import json
import time
import requests
import datetime

#===================================
headers = {'content-type': 'application/json'}
phylotastic_base_url = "https://phylo.cs.nmsu.edu/phylotastic_ws/"

#~~~~~~~~~~~~~~~(Get Tree from Open-Tree_of_Life)~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_tree(taxa_list):
    phylo_service_url = phylotastic_base_url + "gt/ot/tree"
    
    payload = {
        'taxa': taxa_list	
    }
    
    jsonPayload = json.dumps(payload)
    
    #----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool--------------
    try: 
       response = requests.post(phylo_service_url, data=jsonPayload, headers=headers)
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

#----------------------------------------------------------
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
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':
 	#sc_list = ["Setophaga striata","Setophaga magnolia","Setophaga angelae","Setophaga plumbea","Setophaga virens"]
	#print get_tree_sc_names(sc_list)
