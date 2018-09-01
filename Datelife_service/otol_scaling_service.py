import time
import datetime
import json
import requests
from ete3 import Tree
from ete3.parser.newick import NewickError
from ete3.coretype.tree import TreeError

import google_dns

#===================================
headers = {'content-type': 'application/json'}

#===============================================
#--------------------------------------------
def map_names_ottid(sc_names):
 	api_url = 'https://api.opentreeoflife.org/v2/tnrs/match_names'
   
 	payload = {
 		'names': sc_names,
 		'do_approximate_matching': False
 	}

 	jsonPayload = json.dumps(payload)

 	try:
 		response = requests.post(api_url, data=jsonPayload, headers=headers)
 	except requests.exceptions.ConnectionError:
 		alt_url = google_dns.alt_service_url(api_url)
 		response = requests.post(alt_url, data=jsonPayload, headers=headers, verify=False)        
 	#print response.text
 	
 	ott_ids_list = []

 	if response.status_code == requests.codes.ok:
 		data_json = json.loads(response.text)    
 		rsnames_list = data_json['results'] 
 		ott_ids_list = extract_ott_ids(rsnames_list)
        
 	return ott_ids_list

#--------------------------------------------
def extract_ott_ids(results):
 	ott_ids_list = []
 	
 	for element in results:
 		input_name = element['id']
 		match_list = element['matches']
 		ott_id = match_list[0]['ot:ottId']
 			
 		ott_ids_list.append(ott_id)

 	return ott_ids_list

#------------------------------------------------
def get_names_tree(newick_str):
 	parse_error = False
 	try:
 		tree = Tree(newick_str)
 	except NewickError:
 		try:
 			tree = Tree(newick_str, format=1)
 		except NewickError as e:
 			if 'quoted_node_names' in str(e):
 				tree = Tree(newick_str, format=1, quoted_node_names=True)
 			else:	 
 				parse_error = True
 	#print parse_error 
 	names_list = []
 	if not(parse_error):
 		names_list = []
 		for node in tree.traverse("postorder"):
 			if node.name == '':
 				continue
  		 	names_list.append(node.name.replace("_", " "))            
 
 	return names_list

#---------------------------------------------
'''
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
'''
#-----------------------------------------------
def get_dated_induced_tree_ottids(ott_id_list):	
 	#Ref: http://evoblackrim.com/opentree/2018/03/10/dating-open-tree.html
 	api_url = 'http://141.211.236.35:10999/induced_subtree'
   
 	payload = {
 		'ott_ids': ott_id_list
 	}

 	jsonPayload = json.dumps(payload)

 	try:
 		response = requests.post(api_url, data=jsonPayload, headers=headers)
 	except requests.exceptions.ConnectionError as e:
 		if 'BadStatusLine' in str(e):
 			#print "Error from OToL service API: Server retured nothing" 	
 			return None

 	#print response.text
 	#print response.status_code
 	dated_induced_tree_ottids = None

 	if response.status_code == 201:
 		data_json = json.loads(response.text)    
 		dated_induced_tree_ottids = data_json['newick'] 
        
 	return dated_induced_tree_ottids

#-----------------------------------------------
def get_dated_induced_tree(dated_tree_ottids):	
 	api_url = 'http://141.211.236.35:10999/rename_tree'
   
 	payload = {
 		'newick': dated_tree_ottids
 	}

 	jsonPayload = json.dumps(payload)

 	try:
 		response = requests.post(api_url, data=jsonPayload, headers=headers)
 	except requests.exceptions.ConnectionError as e:
 		if 'BadStatusLine' in str(e):
 			#print "Error from OToL service API: Server retured nothing" 	
 			return None

 	#print response.text 	
 	dated_induced_tree = None

 	if response.status_code == 201:
 		data_json = json.loads(response.text)    
 		dated_induced_tree = data_json['newick'] 
        
 	return dated_induced_tree

#-------------------------------------------
def prune_tree(newick_str, names_list):
 	tr = Tree(newick_str, format=1)
 	try:
 		tr.prune(names_list, True)
 		pruned_tree = tr.write()
 	except TreeError as e:
 		err_msg = str(e)
 		if "Ambiguous node name" in err_msg: 
 			amb_name = err_msg[err_msg.rfind(":")+1:].strip().replace("'","")
 			print amb_name
 			names_list.remove(amb_name)
 			tr.prune(names_list, True)
 			pruned_tree = tr.write()
 		else:
 			pruned_tree = None  

 	return pruned_tree

#----------------------------------------------
def scale_tree_api(tree_newick):
 	start_time = time.time()
 	
 	scaled_tree = None
 	taxon_names = get_names_tree(tree_newick)
 	#print taxon_names
 	if len(taxon_names) == 0:
 		return {'status_code': 400, "message": "No names found in the tree"}
 	else:
 		ott_ids = map_names_ottid(taxon_names)
 		
 		if len(ott_ids) == 0:
 			return {'status_code': 400, "message": "No ott_ids matched from the tree"}
 		else:
 			sc_tree_ids = get_dated_induced_tree_ottids(ott_ids)
 			#print sc_tree_ids
 			if sc_tree_ids is None:
 				return {'status_code': 400, "message": "No dated induced tree found from OToL API"}
 			else:
 				otol_scaled_tree = get_dated_induced_tree(sc_tree_ids)
 				if otol_scaled_tree is None:
 					return {'status_code': 500, "message": "Could not rename dated induced tree from OToL API"}
 				#print scaled_tree
 				taxon_names = [name.replace(" ", "_") for name in taxon_names]
 				try:
 					#prune the tree to remove internal nodes
 					scaled_tree = prune_tree(otol_scaled_tree, taxon_names).replace("_", " ")
 				except:
 					scaled_tree = otol_scaled_tree.replace("_", " ")
 
 	response = {}	
 	if scaled_tree is not None:
 		response['message'] = "Success"
 		response['status_code'] = 200	
		response['scaled_tree'] = scaled_tree
 	else: 
 		response['message'] = "Error retrieving scaled tree from OToL API"
 		response['status_code'] = 500
 		response['scaled_tree'] = ""		

	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	meta_data = {}
 	meta_data['creation_time'] = creation_time
 	meta_data['execution_time'] = float("{:4.2f}".format(execution_time))
 	meta_data['source_urls'] = ["http://141.211.236.35:10999/"]
	response['meta_data'] = meta_data
 	response['input_tree'] = tree_newick
	
	return response

#-----------------------------------------------

#if __name__ == "__main__":

	#tree_newick = "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);" 
	#tree_newick = "((((Homo sapiens,Macaca mulatta)Catarrhini,((Melursus ursinus,Canis lupus_pallipes)Caniformia,((Panthera pardus,Panthera tigris)Panthera,Herpestes fuscus))Carnivora)Boreoeutheria,Elephas maximus)Eutheria,Haliastur indus)Amniota;"
	#tree_newick = "(Aulacopone_relicta,(((Myrmecia_gulosa,(Aneuretus_simoni,Dolichoderus_mariae)),((Ectatomma_ruidum,Huberia_brounii),Formica_rufa)),Apomyrma_stygia),Martialis_heureka)Formicidae;"

#	sc_tree = scale_tree_api(tree_newick)
#	print sc_tree	
	
