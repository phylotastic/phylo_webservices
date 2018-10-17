#service description: find common names for the tips of a tree 
#service version: 0.1
import json
import requests
import time
import datetime 
import urllib
from ete3 import Tree
from ete3.parser.newick import NewickError

import scientific_to_common_name_NCBI
import scientific_to_common_name_EOL

#==============================================
#find the tips in the tree
def get_tips_list(newick_str):
 	parse_error = False
 	try:
 		tree = Tree(newick_str)
 	except NewickError:
 		try:
 			tree = Tree(newick_str, format=1)
 		except NewickError as e:
 			#print str(e) 
 			if 'quoted_node_names' in str(e):
 				try:
 					tree = Tree(newick_str, format=1, quoted_node_names=True)
 				except NewickError as e:
 					parse_error = True	
 			else:
 				parse_error = True

 	if not(parse_error):
 		tips_list = [leaf.name for leaf in tree.iter_leaves()]            
 	else:
 		tips_list = None

 	return tips_list

#---------------------------------------

#get the common names of tips
def get_common_names(tips, source):
	common_names_mapping = {}
	tip_list = []

	if source == "EOL":
		common_names_result = scientific_to_common_name_EOL.get_sci_to_comm_names(tips)    
	else: #default NCBI source
		common_names_result = scientific_to_common_name_NCBI.get_sci_to_comm_names(tips)
	
	for result in common_names_result['result']:
		if len(result['common_names']) != 0:
			tip_mapping = {"scientific_name": result['searched_name'], "common_names": result['common_names']}
		tip_list.append(tip_mapping)

	#print common_names_result
	common_names_mapping['tip_list'] = tip_list

	return common_names_mapping

#----------------------------------------
def get_common_names_mapping(newick_str, source="NCBI"):
	start_time = time.time()
	response = {}
	tip_lst = get_tips_list(newick_str)
	if tip_lst is None:
		status_code = 500
		message = "Error: Newick parsing error occured in ETE"
	else:
		mapping = get_common_names(tip_lst, source)
		status_code = 200
		message = "Success"

	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	
 	meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time))}
 	response['meta_data'] = meta_data
 	
 	response['message'] = message
 	response['status_code'] = status_code
 	response['result'] = mapping	

	return response
#-------------------------------------
#if __name__ == '__main__':

	#input_tree = "(((Rangifer tarandus, Cervus elaphus)Cervidae, (Bos taurus, Ovis orientalis)Bovidae), (Suricata suricatta, (Cistophora cristata,Mephitis mephitis))Carnivora);"
	#tips = get_tips_list(input_tree)
	#print get_common_names(tips)
