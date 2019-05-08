#service description: find common names for the tips of a tree 
#service version: 0.1
import json
import requests
import re
import time
import datetime 

from ete3 import Tree
from ete3.parser.newick import NewickError

import scientific_to_common_name_NCBI
import scientific_to_common_name_EOL
import scientific_to_common_name_GNR

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

	if source == "NCBI":
		common_names_result = scientific_to_common_name_NCBI.get_sci_to_comm_names(tips)    
	elif source == "GNR":
		common_names_result = scientific_to_common_name_GNR.get_sci_to_comm_names(tips)    
	else: #default EOL source
		common_names_result = scientific_to_common_name_EOL.get_sci_to_comm_names(tips)
	
	for result in common_names_result['result']:
		if len(result['matched_results']) != 0:
			#GNR source returns result from multiple databases
			if source != "GNR":
				tip_mapping = {"scientific_name": result['searched_name'], "common_names": result['matched_results'][0]['common_names']}
			else: 
				#first check GBIF; if no name found then check CoL and others
				tip_mapping = check_mapping(result, 'GBIF') 
				if tip_mapping is None:
					tip_mapping = check_mapping(result, 'Catalogue') 
					if tip_mapping is None:
						tip_mapping = check_mapping(result, None)
		else:
			tip_mapping = {"scientific_name": result['searched_name'], "common_names": []}

		tip_list.append(tip_mapping)

	#print common_names_result
	common_names_mapping['tip_list'] = tip_list

	return common_names_mapping

#----------------------------------
def preprocess_newick(nwk_str):
	# Delete ott_ids from tip_labels
	nw_str = nwk_str
 	nw_str = re.sub('_ott\d+', "", nw_str)
 	newick_str = nw_str.replace('_', " ")

	return newick_str

#--------------------------------------
def remove_duplicate_names(comm_names):
	processed_names_list = [com_name.lower() for com_name in comm_names]
	unique_list = []
	for name in processed_names_list: 
		if name not in unique_list: 
			unique_list.append(name) 

	return unique_list

#-----------------------------------
def check_mapping(result, db=None):
	mapping = None
	for match in result['matched_results']:
		if db is not None and db in match['data_source'] and len(match['common_names']) != 0:
			mapping = {"scientific_name": result['searched_name'], "common_names": match['common_names']}	
			break
		elif db is None and len(match['common_names']) != 0: 
			mapping = {"scientific_name": result['searched_name'], "common_names": match['common_names']}	
			break

	return mapping

#----------------------------------------
def get_common_name_tree(newick_str, multiple=False, source="GNR"):
	start_time = time.time()
	response = {}
	
	newick_str_c = preprocess_newick(newick_str)
	#print newick_str_c
	name_mapping = []

	tip_lst = get_tips_list(newick_str_c)
	if tip_lst is None:
		status_code = 500
		message = "Error: Newick parsing error occured in ETE"
	else:
		mapping = get_common_names(tip_lst, source)
		#replace tips with their common names
		for tip in mapping['tip_list']:
			sc_name = tip['scientific_name']
			com_names = tip['common_names']
			unq_com_names = remove_duplicate_names(com_names)
			name_mapping.append({'scientific_name': sc_name, 'common_names': unq_com_names})
			
			for common_name in com_names: 
				com_name = common_name.capitalize()
				newick_str_c = newick_str_c.replace(sc_name, sc_name+"_"+com_name)
				if not(multiple):
					break

		response['mapping'] = name_mapping
 
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
	response['input_tree'] = newick_str
 	response['source'] = source
	response['result_tree'] = newick_str_c	

	return response

#-------------------------------------
#if __name__ == '__main__':

	#input_tree = "(((Rangifer tarandus, Cervus elaphus)Cervidae, (Bos taurus, Ovis orientalis)Bovidae), (Suricata suricatta, (Cistophora cristata,Mephitis mephitis))Carnivora);"
	#input_tree = "((((Mustela altaica,Lutra lutra),Taxidea taxus)Mustelidae,Canis lupus)Caniformia,Panthera pardus)Carnivora;"
	#input_tree = "(Setophaga_magnolia_ott532751,Setophaga_striata_ott60236,Setophaga_plumbea_ott45750,Setophaga_angelae_ott381849,Setophaga_virens_ott1014098)Setophaga_ott285198;"
	#input_tree = "((((((Tipularia discolor)Tipularia)Calypsoinae)Epidendreae)mrcaott334ott908,(((((Spiranthes infernalis)Spiranthes)Spiranthinae,((Ponthieva racemosa)Ponthieva)Cranichidinae)Cranichideae,(((Platanthera praeclara)Platanthera)Orchidinae)Orchideae)Orchidoideae)mrcaott335ott27841)mrcaott334ott335,(((Vanilla inodora)Vanilla)Vanilleae)Vanilloideae)Orchidaceae;"
	#print get_common_name_tree(input_tree, False, "GNR")
	#tips = get_tips_list(input_tree)
	#print get_common_names(tips, "EOL")
