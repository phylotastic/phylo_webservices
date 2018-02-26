import dendropy
import requests
import os
import time
import datetime

import treebase_tree_download
import tree_selection

#======================================
output_path = "./data/output/"
#-------------------------------------------
def get_treebase_trees(taxa):
	
	tree_list = treebase_tree_download.get_trees(taxa)
		
	if len(tree_list) == 0:
		return {'code': 422, 'msg': "No tree found for the input list of species", 'trees': [] } 
	selected_trees = tree_selection.select_trees(tree_list, taxa)
	if len(selected_trees) == 0:
		return {'code': 422, 'msg': "No tree matched selection criteria", 'trees': [] }	

	return {'code': 200, 'msg': "Success", 'trees': selected_trees }    

#--------------------------------------------
def build_tree(taxa_list, list_id):
	r_api_url = "http://localhost:8000/treebase_tree"

	#prepare taxa string for phylor_API 
	taxa_str = "|".join(taxa_list)
	taxa = taxa_str.replace(" ", "_")

	payload = {
 		'list_id': list_id,
 		'taxa': taxa,       
	}
 	
	response = requests.post(r_api_url, data=payload) 
	#print response.text  	
	if "200" in response.text:
		return 200
	else:
		return 500
	#if response.status_code == requests.codes.ok:
	
	
#--------------------------------------------
def read_tree_file(file_id):
	if os.path.isfile(output_path + file_id):
		tree_obj = dendropy.Tree.get(path=output_path+file_id, schema="newick")        
		tree_str = tree_obj.as_string(schema="newick")
		tree_str = tree_str.replace('\n', '')
	else:
		tree_str = ""

	return tree_str

#-------------------------------------------
def get_tree(taxa_list):
	start_time = time.time()
	final_result = {}

	taxa_set = frozenset(taxa_list)
	list_id = hash(taxa_set)
	file_id = "tree_" + str(list_id)+"_pr.tre"
	
	if not os.path.isfile(output_path + file_id):
		#print "Building supertree from source trees"
		treebase_dict = get_treebase_trees(taxa_list)
		if treebase_dict['code'] == 200: 
			selected_trees = treebase_dict['trees']
			tree_selection.combine_trees(selected_trees, list_id)
			r_api_resp = build_tree(taxa_list, list_id)
			if r_api_resp != 200:
				return {'status_code': r_api_resp, 'message': "Error from phylor:treebase API" }
		else:
			return {'status_code': treebase_dict['code'], 'message': treebase_dict['msg'] }
	
	tree_str = read_tree_file(file_id)
	end_time = time.time()

	creation_time = datetime.datetime.now().isoformat()
	execution_time = end_time-start_time

	meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["https://github.com/TreeBASE/treebase/wiki/API"] }

	if tree_str != "":
		final_result['status_code'] = 200
		final_result['message'] = "Success"
		final_result['meta_data'] = meta_data
	else:
		final_result['status_code'] = 500
		final_result['message'] = "Error reading output newick file"
	
	final_result['newick'] = tree_str

	return final_result

#----------------------------------------------
#if __name__ == "__main__":
	#taxa = ["Bos taurus", "Cervidae", "Hippopotamus amphibius", "Sus scrofa", "Tayassuidae", "Camelus", "Orcinus orca"]
	#taxa = ["Platanthera praeclara", "Vanilla inodora", "Spiranthes infernalis", "Ponthieva racemosa", "Tipularia discolor", "Cranichus muscosa"]
	#print get_tree(taxa)


