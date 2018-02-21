import requests
import re
import json
import time
import datetime
import dendropy

#------------------------------------------
#get a tree using phylomatic
def get_phylomatic_tree(megatree, taxa):
	api_url = "http://phylodiversity.net/phylomatic/pmws"    

	payload = {
 		'tree': megatree,
 		'informat': "newick",
 		'method': "phylomatic",
 		'taxaformat' : "slashpath",
 		'outformat': "newick",
 		'clean': "true",
 		'taxa': taxa       
	}
 	#encoded_payload = urllib.urlencode(payload)
 
	response = requests.post(api_url, data=payload) 
	#print response.text  	
	
	if response.status_code == requests.codes.ok:
		phylomatic_result = response.text
	else:
		phylomatic_result = None
		
	return phylomatic_result

#--------------------------------------------
#create list of taxa for phylomatic
def make_phylomatic_input_list(slashpath_names):
    #process list
	ListSize = len(slashpath_names)    
	count = 0;
	phylomatic_input_names = ""
    
	for str_element in slashpath_names:
		count += 1
		if(count != ListSize):
			str_element += '\n' 
		phylomatic_input_names += str_element
    
	#print phylomatic_input_names
	return phylomatic_input_names

#---------------------------------------------
#extract the newick tree from the phylomatic result
def process_phylomatic_result(result):
 	#print result
 	st_indx = result.find("[")
 	en_indx = result.find("]")
 	#print "St indx: %d En indx: %d"%(st_indx, en_indx)
 	extra_note = result[st_indx : en_indx+1]
 	#print extra_note
 	newick_str = result[0: st_indx]
 	if st_indx != -1 and en_indx != -1:
 		newick_str += ";"
 	newick_str = newick_str.replace("_", " ")
 	#print newick_str

 	return {"newick": str(newick_str), "note": extra_note}

#---------------------------------------------
#resolve scientific names
def resolve_sn_gnr(scNames):	
	api_url = "http://resolver.globalnames.org/name_resolvers.json"
	
	scientific_names = make_api_friendly_list(scNames)
	payload = {
        'names': scientific_names,
	}
     
	response = requests.post(api_url, data=payload)     
	#print response.text
	resolvedNamesList = [] 
	data_json = json.loads(response.text)

	if response.status_code == requests.codes.ok:        
		rsnames_list = data_json['data'] 
		for element in rsnames_list:
			input_name = element['supplied_name_string']
			final_class_path = input_name						
			if 'results' in element:
				for match in element['results']: 
					class_path = "" if match['classification_path'] is None else match['classification_path'] 
					match_score = match['score']    
					if match_score >= 0.75 and len(class_path) > 0:
						slash_pos_list = [pos for pos, char in enumerate(class_path) if char == "|"]
						slash_pos_len = len(slash_pos_list)
						if slash_pos_len == 0:
							continue	
						elif slash_pos_len > 4:
							sub_indx = slash_pos_list[slash_pos_len-3] #get the 3rd index from last
						else:
							#print slash_pos_list
							#print class_path				
							sub_indx = slash_pos_list[slash_pos_len-1] #get the 1st index from last
						#extract the classification path upto family or genus or species					
						class_path_sub = class_path[sub_indx+1 : len(class_path)]
						class_path_sub = re.sub(r"\s+","_", class_path_sub)
						final_class_path = class_path_sub.replace("|", "/")
						break

			resolvedNamesList.append(final_class_path)
        
	return resolvedNamesList
        
#----------------------------------------------    
#Process Scientific Names List for GNR
def make_api_friendly_list(scNamesList):
    #process list    
    ListSize = len(scNamesList)    
    
    count = 0;
    TobeResolvedNames = ""
    
    for str_element in scNamesList:
        count += 1
        if(count != ListSize):
            str_element += '||' 
        TobeResolvedNames += str_element
    
    #print "List size:"+ str(ListSize)    
    return TobeResolvedNames

#------------------------------------------
def check_newick_validity(tree_str):
	message = "Valid"
	try:
		tree = dendropy.Tree.get(data=tree_str, schema="newick")
	except Exception, e:
 		if "Incomplete or improperly-terminated tree statement" in str(e): #invalid: "((A,B),C,D));"  valid: ((A,B),(C,D)); 
 			message = "NewickReaderIncompleteTreeStatementError: " + str(e)
 		elif "Unbalanced parentheses at tree statement" in str(e):  #invalid: "((A,B),(C,D);"  valid: ((A,B),(C,D)); 
 			message = "NewickReaderMalformedStatementError: "+str(e) 
 		elif "Multiple occurrences of the same taxa" in str(e): #invalid: "((A,B),(C,C));"  valid: ((A,B),(C,D));
 			message = "NewickReaderDuplicateTaxonError: "+str(e)
 		elif "Unexpected end of stream" in str(e): # invalid: "((A,B),(C,D))"  valid: ((A,B),(C,D));
 			message = "UnexpectedEndOfStreamError: "+str(e)
 		else:
			message = "Read error: Invalid newick string"

	return message

#---------------------------------------------
def phylomatic_tree_controller(megatree, species_list):

	nw_msg = check_newick_validity(megatree)
	if "Valid" not in nw_msg:
		return {'status_code': 400, 'message': nw_msg, 'newick': ""}

	sp_list = [species.replace(" ", "_") for species in species_list]
	slashpath_names = resolve_sn_gnr(species_list)
	
	#print sp_list
	#print slashpath_names
	if len(slashpath_names) > 0:
		taxa = slashpath_names
	else:
		taxa = sp_list
	 
	phylomatic_input = make_phylomatic_input_list(taxa)
	#print "Get pruned tree using phylomatic..."	
	phylomatic_result = get_phylomatic_tree(megatree, phylomatic_input)
	#print phylomatic_result

	final_result = {'status_code': 200, 'message': "Success", 'newick': ""}

	if phylomatic_result is None:
		final_result['status_code'] = 500
		final_result['message'] = "Error: Response error while pruning megatree using phylomatic"
	elif "No taxa in common" in phylomatic_result:
		final_result['status_code'] = 422
		final_result['message'] = "No common taxa found: Unable to prune megatree using phylomatic"
	else:
		final_tree = process_phylomatic_result(phylomatic_result)
		final_result['newick'] = final_tree['newick']
		
	return final_result

#----------------------------------------------
#if __name__ == '__main__':
       
	#megatree = "((((((((((((((((((((((Arabidopsis_lyrata,Arabidopsis_thaliana),Capsella_rubella),Thellungiella_parvula),Carica_papaya),(Gossypium_raimondii,Theobroma_cacao)),(Citrus_clementina,Citrus_sinensis)),(((Phaseolus_vulgaris,Glycine_max),Medicago_truncatula),(Prunus_persica,Fragaria_vesca)),((Ricinus_communis,Manihot_esculenta),Populus_trichocarpa)),Eucalyptus_grandis),(((Solanum_tuberosum,Solanum_lycopersicum),Mimulus_guttatus),(Lactuca_sativa,Artemisia_annua))),Vitis_vinifera),Buxus_sinica),Platanus_acerifolia),Aquilegia_coerulea),((((((((((Panicum_virgatum,Setaria_italica),(Sorghum_bicolor,Zea_mays)),Brachypodium_distachyon),(Canna_indica,Musa_acuminata)),Trachycarpus_fortunei),Oryza_sativa),(((Asparagus_officinalis,Yucca_filamentosa),Iris_japonica),Lilium_brownii)),(Pandanus_utilis,Dioscorea_opposita)),(Pinellia_ternata,Alismaplantago-aquatica)),Acorus_calamus)),Selaginella_moellendorffii),Physcomitrella_patens),((((((Persea_americana,Cinnamomum_camphora),Chimonanthus_praecox),Volvox_carteri),((Magnolia_denudata,Liriodendron_tulipifera),Chlamydomonas_reinhardtii)),(((Aristolochia_tagala,Saruma_henryi),Houttuynia_cordata),Chlorella_sp)),((((Ceratophyllum_demersum,Ceratophyllum_oryzetorum),Ostreococcus_lucimarinus),((Sarcandra_glabra,Chloranthus_japonicus),Ostreococcus_tauri)),(Micromonas_pusilla_2,Micromonas_pusilla_1)))),Illicium_henryi),(Cabomba_caroliniana,Nuphar_advena)),Cyanidioschyzon_merolae),Amborella_trichopoda),Ginkgo_biloba);"
	#species_list = ["Solanum lycopersicum", "Carica papaya", "Prunus persica", "Vitis amurensis", "Musa balbisiana", "Glycine max", "Theobroma cacao", "Oryza sativa"]
	
	#print phylomatic_tree_controller(megatree, species_list)
