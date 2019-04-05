# -*- coding: utf-8 -*-
#Open Tree of Life tree service: version 1.2
import json
import time
import requests
import types
import re
import ast
import datetime

import r_helper
import google_dns
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#Suppress warning for using a version of Requests which vendors urllib3 inside
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#------------------------
from ete3 import Tree, TreeStyle
from ete3.parser.newick import NewickError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
api_url = "https://api.opentreeoflife.org/v3/tree_of_life/"
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
    
    #----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool due to DNS resolver problem--------
    #+++++++++++Solution 1++++++++++++++++
    #max_tries = 20
    #remaining_tries = max_tries
    #while remaining_tries > 0:
    #    try:
    #        response = requests.post(resource_url, data=jsonPayload, headers=headers)
    #        break
    #    except requests.exceptions.ConnectionError:
    #        time.sleep(20)
    #    remaining_tries = remaining_tries - 1
    #+++++++++++++++++++++++++++++++++++++++
    
    #+++++++++++Solution 2++++++++++++++++
    try: 
       response = requests.post(resource_url, data=jsonPayload, headers=headers)
    except requests.exceptions.ConnectionError:
       alt_url = google_dns.alt_service_url(resource_url)
       response = requests.post(alt_url, data=jsonPayload, headers=headers, verify=False)        
    #----------------------------------------------

    newick_tree_str = ""
    studies = ""
    inducedtree_info = {}

    if response.status_code == requests.codes.ok:
 		data_json = json.loads(response.text)
 		newick_tree_str = data_json['newick']
 		studies = data_json['supporting_studies']		
 		inducedtree_info['message'] = "Success"
 		inducedtree_info['status_code'] = 200
    else:
 		try: 
 			error_msg = str(response.text)
 			if 'node_id' in error_msg:
 				st_indx = error_msg.find("node_id")  #"[/v3/tree_of_life/induced_subtree] Error: node_id 'ott4284156' was not found!"
 				en_indx = error_msg.find("was")
 				missing_node_id_str = error_msg[st_indx+9: en_indx-2]
 				missing_ott_id = int(missing_node_id_str.replace("ott", ""))
 				ottIdList.remove(missing_ott_id)
 				return ottIdList
 			else:
 				error_json = json.loads(error_msg)
 				error_msg = error_json['message']
 		 		inducedtree_info['message'] = "OpenTreeofLife API Error: " + error_msg
         	
 		except Exception as e:
 			inducedtree_info['message'] =  "OpenTreeofLife API Error: " + str(e)
     		 	
    inducedtree_info['status_code'] = response.status_code

    inducedtree_info['newick'] = newick_tree_str
    inducedtree_info['studies'] = studies
 	
    return inducedtree_info

#-------------------------------------------------------
def subtree(ottidList):   
 	induced_response = get_inducedSubtree(ottidList)
 	while type(induced_response) == types.ListType: 
 		induced_response = get_inducedSubtree(induced_response)    
 
 	return induced_response 
#-----------------------------------------------------------
#get newick string for tree from OpenTree
#input: list of resolved scientific names
def get_tree_OT(resolvedNames, include_metadata=False, include_ottid=True):
 	start_time = time.time() 
 	ListSize = len(resolvedNames)
    
 	response = {}
 	if ListSize == 0:
 		response['newick'] = ""
 		response['message'] = "Error: List of resolved names empty"
 		response['status_code'] = 500
 		
 		return response
 		
 	rsnames = resolvedNames
 	#rsnames = resolvedNames['resolvedNames']
 	ottIdList = []
 	for rname in rsnames:
 		if 'matched_results' in rname:
 			for match_result in rname['matched_results']:
 				if 'Open Tree of Life' in match_result['data_source']:
 					ottIdList.append(match_result['taxon_id'])
 					break 			
 		else:
 			if rname['resolver_name'] == 'OT':
 				ottIdList.append(rname['taxon_id'])
 			else:
 				response['newick'] = ""
 				response['message'] = "Error: wrong TNRS. Need to resolve with OpenTreeofLife TNRS"
 				response['status_code'] = 500
 			 	return response
 			     
    #get induced_subtree
 	final_result = {} 
 	opentree_result = subtree(ottIdList)
 	newick_str = opentree_result['newick']
 	if newick_str.find(";") == -1:
 		newick_str = newick_str + ";"
 
 	if not(include_ottid):
 		# Delete ott_ids from tip_labels
 		nw_str = newick_str
 		nw_str = re.sub('_ott\d+', "", nw_str)
 		newick_str = nw_str
 		#newick_str = nw_str.replace('_', " ")

 	#remove singleton nodes from tree
 	final_nwk_str = r_helper.remove_singleton(newick_str)
 	if final_nwk_str is None: #R function did not work
 		final_nwk_str = newick_str
 	
 	final_result['newick'] = final_nwk_str #newick_str.encode('ascii', 'ignore').decode('ascii')
 	if opentree_result['status_code'] != 200:	
 		return opentree_result 
 
 	if opentree_result['newick'] != "":
 		final_result['message'] = "Success"
 		final_result['status_code'] = 200
 		if include_metadata:
 			synth_tree_version = get_tree_version()		
 			tree_metadata = get_metadata()
 			tree_metadata['inference_method'] = tree_metadata['inference_method'] + " from synthetic tree with ID "+ synth_tree_version
 			final_result['tree_metadata'] = tree_metadata
 			final_result['tree_metadata']['synthetic_tree_id'] = synth_tree_version
 			#https://wiki.python.org/moin/UnicodeDecodeError
 			newick_str = newick_str.encode('utf-8', 'ignore')
 			num_tips = get_num_tips(newick_str)
 			if num_tips != -1:
 				final_result['tree_metadata']['num_tips'] = num_tips

 			study_ids = opentree_result['studies']
 			study_list = get_supporting_studies(study_ids) 	
 			final_result['tree_metadata']['supporting_studies'] = study_list['studies']
 		 
 	end_time = time.time()
 	execution_time = end_time-start_time
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	meta_data = {}
 	meta_data['creation_time'] = creation_time
 	meta_data['execution_time'] = float("{:4.2f}".format(execution_time))
 	#meta_data['service_documentation'] = service_documentation
 	meta_data['source_urls'] = ["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tree_of_life"]

 	final_result['meta_data'] = meta_data  

 	return final_result
 	
#-------------------------------------------
#get supporting studies of the tree from OpenTree
def get_supporting_studies(studyIdList):
 	resource_url = "https://phylo.cs.nmsu.edu/phylotastic_ws/md/studies"    
    
 	payload_data = {
 		'list': studyIdList,
 		'list_type': "studyids"		
    }
 	jsonPayload = json.dumps(payload_data)
    
    #+++++++++++Solution 2++++++++++++++++
 	try: 
 		response = requests.post(resource_url, data=jsonPayload, headers=headers)
 	except requests.exceptions.ConnectionError:
 		alt_url = google_dns.alt_service_url(resource_url)      
 		response = requests.post(alt_url, data=jsonPayload, headers=headers, verify=False)        
    #----------------------------------------------    
    
 	studies_info = {}

 	data_json = json.loads(response.text)  
 	if response.status_code == requests.codes.ok:	
 		studies_info['studies'] = data_json['studies']		
 		studies_info['message'] = data_json['message']
 		studies_info['status_code'] = data_json['status_code']
 	else:
 		studies_info['studies'] = []
 		if 'message' in data_json:
 			studies_info['message'] = data_json['message']
 		else:			
 			studies_info['message'] = "Error: Response error while getting study info using Phylotastic"
 		studies_info['status_code'] = response.status_code

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
 			#print str(e) 
 			if 'quoted_node_names' in str(e):
 				try:
 					tree = Tree(newick_str, format=1, quoted_node_names=True)
 				except NewickError as e:
 					parse_error = True	
 			else:
 				parse_error = True

 	if not(parse_error):
 		tips_list = [leaf for leaf in tree.iter_leaves()]            
 		tips_num = len(tips_list)
 	else:
 		tips_num = -1

 	return tips_num

#-------------------------------------------
def get_tree_version():
 	resource_url = api_url + "about"    
    
 	#----------TO handle requests.exceptions.ConnectionError: HTTPSConnectionPool--------------
    #+++++++++++Solution 2++++++++++++++++
 	try: 
 		response = requests.post(resource_url)
 	except requests.exceptions.ConnectionError:
 		alt_url = google_dns.alt_service_url(resource_url)
 		response = requests.post(alt_url, verify=False)                
    #----------------------------------------------
        
 	metadata = {}
 	if response.status_code == requests.codes.ok:
 		data_json = json.loads(response.text)
 		return data_json['synth_id']
 	else:
 		return "" #Error: getting synth tree version"  

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
    
	#ott_idlist = [433666, 18021, 3802384, 912655, 3746533, 918710, 5121548, 3832795, 952533, 6052258, 3998503, 3509575, 779104, 5000538, 3996806, 3978191, 510792, 532917, 3708728, 197595, 3508673, 737276, 3560838, 4032, 3210188, 3977800, 540895, 377156, 4977863, 3712394, 3681318, 3802710, 4505629, 4006407, 3194147, 2815857, 4107072, 215326, 4595643, 3746391, 4604046, 4378715, 6378722, 454977, 3662585, 4676639, 3915948, 3033580, 695582, 834877, 3203503, 4455150, 690589, 806444, 2985147, 4194163, 6277191, 3369819, 5097835, 919822, 3396588, 953128, 3608996, 3149259, 5105169, 3876440, 3258775, 82316, 723405, 943939, 1059988, 189648, 3903564, 2888162, 3941789, 3052287, 6051794, 6243490, 378262, 743867, 6163921, 439510, 5227132, 4018146, 286185, 3293755, 2995398, 469974, 3023470, 4027260, 3503119, 6071397, 559015, 40332, 3218789, 6112538, 3253119, 3197128, 952687, 4041393, 3091861, 4427421, 3671409, 6244654, 707486, 474175, 3209192, 4768619, 5801096, 309141, 3352412, 17645, 123343, 5146923, 3413028, 3074766, 3310513, 6128184, 3684868, 253039, 4977373, 3183138, 3012947, 6309210, 3466023, 934930, 5975656, 3044514, 2917937, 3748550, 4555170, 4360269, 3757278, 680503, 841628, 475283, 3933266, 5257885, 5155212, 658833, 1022990, 4508624, 918223, 3623431, 3188289, 6119837, 6306013, 616360, 5449983, 6080379, 185290, 37217, 682827, 3390075, 6182283, 2890595, 445886, 6278337, 4585063, 908798, 4703000, 134974, 3565697, 408171, 910430, 784877, 3922738, 2911806, 3630938, 3468181, 4353996, 3877008, 4361402, 785192, 4630284, 485925, 42306, 3986342, 4383501, 3089422, 432031, 3314623, 3591400, 3776487, 10192, 3090364, 75715, 3512710, 2957120, 530789, 67174, 3539273, 5073036, 6274531, 3162559, 4121165, 1016007, 2884772, 2965411, 3276825, 4346374, 2902817, 3920477, 973582, 10732, 6178755, 854212, 283627, 889471, 6099780, 4049235, 1089215, 4510133, 679823, 3303172, 3530185, 824583, 3232630, 3901755, 5400857, 4369781, 306890, 3365436, 4204580, 3702460, 4993266, 4459274, 4158260, 4479740, 5462853, 3490415, 947030, 3795317, 4495330, 3141118, 3266145, 6275540, 6165613, 3392792, 4121880, 373777, 2874479, 695282, 4434715, 4378346, 2941719, 3907816, 3960904, 376782, 3405311, 899169, 3219744, 502615, 35890, 124716, 6046666, 765141, 168215, 134968, 6304101, 68622, 320728, 2952334, 129927, 179844, 3010120, 2912929, 18935, 3530039, 6129056, 6080749, 798674, 3821331, 6049284, 4006484, 3482429, 3224760, 935894, 709107, 1063726, 4006284, 3481406, 4422815, 748946, 1093221, 3748906, 6070096, 2898881, 61760, 3652785, 3867076, 3321502, 3523833, 3917014, 4377787, 5049699, 3352907, 4994682, 4198470, 318763, 6069161, 2864402, 145176, 3414157, 1065584, 6225559, 3504465, 4742977, 3085412, 1054907, 3585909, 4191643, 321812, 4380241, 3048158, 3696230, 3568351, 4050316, 5061282, 4009245, 3328571, 404824, 3028369, 3885240, 3927317, 916304, 3875298, 4724297, 4206775, 3703218, 3476660, 3482304, 161789, 4492740, 3306560, 574802, 534105, 5381675, 3385865, 5262773, 3909665, 4977841, 3193831, 4470996, 3122742, 3111455, 3572428, 3316029, 103249, 3406123, 6086775, 6157204, 5077042, 752644, 252415, 4370491, 676992, 273898, 3441108, 3196679, 553629, 5107001, 790513, 6167067, 3989812, 5450912, 3466729, 3160066, 298091, 5378935, 4355021, 3636743, 2997400, 961176, 270778, 396547, 198230, 785102, 3512451, 4345176, 3589886, 4802995, 510153, 104052, 3640593, 1063158, 454322, 6090760, 195448, 4405746, 3276454, 981621, 6043569, 3292079, 4649559, 3930641, 3944742, 6218059, 5471420, 549422, 4508471, 3777070, 3176039, 6357315, 528727, 5000865, 5338593, 6092514, 3690650, 3689238, 3027073, 201561, 5201077, 4482520, 6094047, 4237344, 5068964, 5783661, 393337, 4697520, 4472986, 586667, 3755374, 3468299, 3118420, 3935680, 5122021, 871618, 6131513, 4341715, 4069977, 4616537, 4373719, 4379798, 6118723, 4431557, 720362, 208871, 4640218, 220141, 977579, 4741117, 4991059, 71357, 3383871, 623625, 2874348, 538350, 3799622, 3054671, 5122047, 6076187, 1001606, 3698765, 603566, 5019074, 844023, 5522559, 3302141]
	#inputNames = ["Dionaea muscipula", "Sarracenia", "Darlingtonia californica", "Drosera", "Pinguicula", "Utricularia", "Roridulaceae"]
	#inputNames = '{"status_code": 200, "message": "Success", "meta_data": {"execution_time": 0.39, "creation_time": "2018-09-15T11:35:29.996768", "source_urls": ["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tnrs"]}, "total_names": 7, "resolvedNames": [{"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Drosera", "search_string": "drosera", "synonyms": ["Drosera"], "taxon_id": 14968}], "input_name": "Drosera"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Sarracenia", "search_string": "sarracenia", "synonyms": ["Sarracenia"], "taxon_id": 639943}], "input_name": "Sarracenia"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Darlingtonia californica", "search_string": "darlingtonia californica", "synonyms": ["Chrysamphora californica", "Darlingtonia californica"], "taxon_id": 639950}], "input_name": "Darlingtonia californica"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Roridulaceae", "search_string": "roridulaceae", "synonyms": ["Roridulaceae"], "taxon_id": 538887}], "input_name": "Roridulaceae"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Utricularia", "search_string": "utricularia", "synonyms": ["Lentibularia", "Lecticula", "Meionula", "Lepiactis", "Pelidnia", "Meloneura", "Nelipus", "Personula", "Akentra", "Orchyllium", "Trixapias", "Askofake", "Biovularia", "Avesicaria", "Bucranion", "Pleiochasia", "Plectoma", "Aranella", "Hamulia", "Vesiculina", "Setiscapella", "Polypompholyx", "Plesisa", "Saccolaria", "Calpidisca", "Sacculina", "Cosmiza", "Enetophyton", "Diurospermum", "Stomoisia", "Enskide", "Trilobulina", "Tetralobus", "Megozipa", "Xananthes", "Utricularia"], "taxon_id": 512422}], "input_name": "Utricularia"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Pinguicula", "search_string": "pinguicula", "synonyms": ["Pinguicula"], "taxon_id": 659715}, {"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Pinguicula", "search_string": "pinguicula", "synonyms": ["Plicatra", "Ringactaeon", "Ringicula", "Ringiculadda", "Ringiculina", "Ringicula (Ringicula)", "Ringicula (Ringiculina)", "Pinguicula", "Ringiculus", "Ringuicula"], "taxon_id": 2915359}], "input_name": "Pinguicula"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Dionaea muscipula", "search_string": "dionaea muscipula", "synonyms": ["Dionaea sessiliflora", "Dionaea muscipula", "Drosera corymbosa", "Dionaea corymbosa", "Dionaea sensitiva", "Dionaea uniflora"], "taxon_id": 14971}], "input_name": "Dionaea muscipula"}]}'
	#print get_inducedSubtree(ott_idlist)
	#inputNames = ["Chelonia mydas", "Amphiprion ocellaris",	"Paracanthurus hepatus", "Zanclus cornutus", "Diodon holocanthus", "Gramma loreto", "Hippocampus kelloggi", "Zebrasoma flavescens", "Pisaster brevispinus", "Opisthoteuthis californiana",	"Aetobatus narinari", "Lysmata amboinensis", "Dascyllus aruanus", "Isurus paucus", "Carcharodon carcharias", "Sphyrna mokarran", "Pelecanus conspicillatus", "Heteractis magnifica"] #finding nemo
	#print get_tree_OT(inputNames)
	#inputNames = '{"status_code": 200, "message": "Success", "meta_data": {"execution_time": 0.37, "creation_time": "2018-09-15T12:10:08.306043", "source_urls": ["https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tnrs"]}, "total_names": 18, "resolvedNames": [{"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Zebrasoma flavescens", "search_string": "zebrasoma flavescens", "synonyms": ["Acanthurus flavescens", "Zebrasoma flavescens"], "taxon_id": 467289}], "input_name": "Zebrasoma flavescens"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Hippocampus kelloggi", "search_string": "hippocampus kelloggi", "synonyms": ["Hippocampus kelloggi", "Hippocampus kellogii", "Hippocampus suezensis"], "taxon_id": 630151}], "input_name": "Hippocampus kelloggi"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Pelecanus conspicillatus", "search_string": "pelecanus conspicillatus", "synonyms": ["Pelecanus australis", "Pelecanus conspicillatus", "Catoptropelicanus perspicillatus"], "taxon_id": 986358}], "input_name": "Pelecanus conspicillatus"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Sphyrna mokarran", "search_string": "sphyrna mokarran", "synonyms": ["Sphyrna mokarran", "Sphyrna mokorran", "Sphyrna ligo", "Zygaena mokarran", "Zygaena dissimilis", "Sphyrna mukaran"], "taxon_id": 970846}], "input_name": "Sphyrna mokarran"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Lysmata amboinensis", "search_string": "lysmata amboinensis", "synonyms": ["Hippolysmata vittata var. amboinensis", "Lysmata amboinensis"], "taxon_id": 810360}], "input_name": "Lysmata amboinensis"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Heteractis magnifica", "search_string": "heteractis magnifica", "synonyms": ["Heteractis ritteri", "Radianthus paumotensis", "Helianthopsis ritteri", "Actinia magnifica id", "Radianthus ritteri", "Radianthus mabrucki", "Radianthus magnifica", "Heteractis paumotensis", "Actinia magnifica", "Heteractis magnifica", "Ropalactis magnifica", "Helianthopsis mabrucki", "Corynactis magnifica", "Antheopsis ritteri"], "taxon_id": 1086126}], "input_name": "Heteractis magnifica"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Aetobatus narinari", "search_string": "aetobatus narinari", "synonyms": ["Aetobatis laticeps", "Aetobates narinari", "Aetobatis narinari", "Aetobatis latirostris", "Raja narinari", "Aetobatus laticeps", "Myliobatis punctatus", "Stoasodon narinari", "Raia quinqueaculeata", "Myliobatis macroptera", "Myliobatis eeltenkee", "Aetobatus narinari"], "taxon_id": 759551}], "input_name": "Aetobatus narinari"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Amphiprion ocellaris", "search_string": "amphiprion ocellaris", "synonyms": ["Amphiprion ocellaris", "Amphiprion melanurus", "Amphiprion bicolor"], "taxon_id": 674643}], "input_name": "Amphiprion ocellaris"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Zanclus cornutus", "search_string": "zanclus cornutus", "synonyms": ["Zanclus cornatus", "Zanclus cornutus", "Chaetodon cornutus", "Chaetodon canescens", "Zanclus cornotus", "Zanclus canescens"], "taxon_id": 199070}], "input_name": "Zanclus cornutus"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Chelonia mydas", "search_string": "chelonia mydas", "synonyms": ["Chelonia virgata", "Chelonia tenuis", "Chelonia bicarinata", "Chelonia maculosa", "Testudo chloronotus", "Chelonia mydas subsp. mydas", "Testudo mydas", "Natator tessellatus", "Chelonia formosa", "Chelonia marmorata", "Chelonia albiventer", "Chelone virgata", "Chelonia lachrymata", "Chelone mydas", "Chelonia agassizzii", "Chelonia lata", "Testudo japonica", "Caretta thunbergi", "Caretta esculenta", "Testudo cepediana", "Mydas viridis", "Testudo viridis", "Euchelus macropus", "Chelonia japonica", "Testudo rugosa", "Caretta thunbergii", "Natator tesselatus", "Chelonia agassizii", "Testudo marina", "Thalassiochelys albiventer", "Caretta cepedii", "Testudo macropus", "Testudo viridisquamosa", "Chelonia midas", "Chelonia mydas caranigra", "Chelonia mydas", "Chelonia agassizi"], "taxon_id": 559133}], "input_name": "Chelonia mydas"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Paracanthurus hepatus", "search_string": "paracanthurus hepatus", "synonyms": ["Acanthurus hepatus", "Paracanthurus hepatus", "Paracanthurus theuthis", "Acanthurus theuthis", "Teuthis hepatus"], "taxon_id": 773222}], "input_name": "Paracanthurus hepatus"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Diodon holocanthus", "search_string": "diodon holocanthus", "synonyms": ["Diodon quadrimaculatus", "Diodon pilosus", "Paradiodon quadrimaculatus", "Diodon sexmaculatus", "Diodon hystrix subsp. holocanthus", "Trichodiodon pilosus", "Atopomycterus bocagei", "Diodon holacanthus", "Diodon maculifer", "Diodon hystrix holocanthus", "Diodon novemaculatus", "Diodon multimaculatus", "Diodon paraholocanthus", "Diodon novemmaculatus", "Diodon holocanthus"], "taxon_id": 166940}], "input_name": "Diodon holocanthus"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Pisaster brevispinus", "search_string": "pisaster brevispinus", "synonyms": ["Asterias brevispina", "Asterias papulosa", "Pisaster brevispinus", "Pisaster papulosus", "Pisaster paucispinus"], "taxon_id": 76842}], "input_name": "Pisaster brevispinus"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Opisthoteuthis californiana", "search_string": "opisthoteuthis californiana", "synonyms": ["Opisthoteuthis californiana"], "taxon_id": 996614}], "input_name": "Opisthoteuthis californiana"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Dascyllus aruanus", "search_string": "dascyllus aruanus", "synonyms": ["Dascyllus arnanus", "Dascyllus aruanus", "Chaetodon arcuanus", "Abudefduf caroli", "Dascyllus blochii", "Chaetodon aruanus", "Pomacentrus emamo", "Pomacentrus devisi", "Tetradrachmum arcuatum", "Pomacentrus trifasciatus", "Chaetodon abudafar", "Tetradrachmum aruanum"], "taxon_id": 49239}], "input_name": "Dascyllus aruanus"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Carcharodon carcharias", "search_string": "carcharodon carcharias", "synonyms": ["Carcharias vorax", "Carcharias verus", "Carcharodon albimors", "Carcharias vulgaris", "Carcharodon rondeletii", "Carcharodon capensis", "Carcharodon smithii", "Carcharodon smithi", "Carcharodon carcharias", "Squalus carcharias", "Carcharadon charcharias", "Carcharias lamia", "Carcharias atwoodi", "Carcharias rondeletti", "Carcharias maso", "Squalus vulgaris", "Squalus lamia", "Carcharodon caifassi", "Carcharodon etruscus", "Squalus caninus", "Carharodon carcharias"], "taxon_id": 554297}], "input_name": "Carcharodon carcharias"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Isurus paucus", "search_string": "isurus paucus", "synonyms": ["Isurus paucus", "Lamiostoma belyaevi", "Isurus alatus"], "taxon_id": 500598}], "input_name": "Isurus paucus"}, {"matched_results": [{"data_source": "Open Tree of Life Reference Taxonomy", "match_type": "Exact", "match_score": 1.0, "matched_name": "Gramma loreto", "search_string": "gramma loreto", "synonyms": ["Gramma loreto"], "taxon_id": 300538}], "input_name": "Gramma loreto"}]}'	
	#result = get_tree_OT(json.loads(inputNames))
	#print result
    

