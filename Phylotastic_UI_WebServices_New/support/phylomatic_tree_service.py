import requests
import urllib
import json
import time
import datetime

#----------------------------------------
megatree_plants = ["R20120829", "smith2011", "zanne2014"]
megatree_mammals = ["binindaemonds2007"]

#------------------------------------------
#get a tree using phylomatic
def get_phylomatic_tree(megatree_id, taxa):
 	api_url = "http://phylodiversity.net/phylomatic/pmws"    

 	payload = {
 		'storedtree': megatree_id,
 		'informat': "newick",
 		'method': "phylomatic",
 		'taxaformat' : "slashpath",
 		'outformat': "newick",
 		'clean': "true",
 		'taxa': taxa       
	}
 	encoded_payload = urllib.urlencode(payload)
 
 	response = requests.post(api_url, data=encoded_payload) 
  	
 	phylomatic_response = {}
 	
 	if response.status_code == requests.codes.ok:
 		phylomatic_response['response'] = response.text
 		phylomatic_response['status_code'] = 200
 		phylomatic_response['message'] = "Success"
 	else:
 		phylomatic_response['response'] = None
 		phylomatic_response['status_code'] = response.status_code
 		phylomatic_response['message'] = "Error: Response error while getting tree from phylomatic"

 	return phylomatic_response

#--------------------------------------------------------
#infer the taxonomic context from a list of taxonomic names 
def get_taxa_context(taxaList):
 	resource_url = "https://api.opentreeoflife.org/v2/tnrs/infer_context"    
    
 	payload_data = {
     	'names': taxaList
    }

 	jsonPayload = json.dumps(payload_data)
    
 	response = requests.post(resource_url, data=jsonPayload, headers={'content-type': 'application/json'})
        
 	
 	if response.status_code == requests.codes.ok:
 		json_response = json.loads(response.text)
 		context = json_response['context_name']
 	else:
 		context = None

 	return context

#-----------------------------------------------
#get a list of pre-defined taxonomic contexts from OpenTree
def get_contexts():
 	resource_url = "https://api.opentreeoflife.org/v2/tnrs/contexts"    
    
 	response = requests.post(resource_url, headers={'content-type': 'application/json'})
 	
 	if response.status_code == requests.codes.ok:
 		return response.text
 	else:
 		return None

#---------------------------------------------
def process_taxa_list(taxaList):
 	taxa = "\n".join(taxaList)
 	taxa = taxa.replace(" ", "_")

 	return taxa

#---------------------------------------------
def process_phylomatic_result(result):
 	#print result
 	st_indx = result.find("[")
 	#print "St indx:" + str(st_indx)
 	en_indx = result.find("]")
 	#print "En indx:" + str(en_indx)
 	extra_note = result[st_indx : en_indx+1]
 	#print extra_note
 	newick_str = result[0: st_indx]
 	if st_indx != -1 and en_indx != -1:
 		newick_str += ";"
 	#print newick_str
 	#newick_str = newick_str.replace("_", " ")
 	#print newick_str

 	return {"newick": newick_str, "note": extra_note}

#---------------------------------------------
def tree_controller(taxaList):
 	start_time = time.time()	
 	 	
 	context = get_taxa_context(taxaList)
 	if context is not None:
 		contexts = json.loads(get_contexts())	
 		for cname, clist in contexts.items():
 			if context in clist:
 				context_name = cname
 				break
 		context_l = context_name.lower()
	else:
		context_l = ""

 	#find megatree corresponding to this list	
 	if  context_l == "animals":
 		megatree_list = megatree_mammals
 	elif context_l == "plants":
 		megatree_list = megatree_plants
 	else:
 		megatree_list = None

 	taxa = process_taxa_list(taxaList)

 	final_result = {}

 	if megatree_list is None: #try all megatrees
 		megatree_list = megatree_mammals + megatree_plants

 	for megatree_id in megatree_list:
 		phylomatic_result = get_phylomatic_tree(megatree_id, taxa)
 		if phylomatic_result['response'] is None:
 			final_result = {"newick": "", "status_code": phylomatic_result['status_code'], "message": phylomatic_result['message']}
 			break
 		else:
 			if "No taxa in common" in phylomatic_result['response']:
 				continue
 			else:			
 				processed_result = process_phylomatic_result(phylomatic_result['response'])
 				final_result = {"newick": processed_result['newick'], "status_code": 200, "message": "Success"}
 				break

 	if not(final_result):
 		final_result = {"newick": "", "status_code": 200, "message": "No tree found using phylomatic web service"}

 	end_time = time.time()
 	execution_time = end_time-start_time
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-18"
 	source_urls = ["http://phylodiversity.net/phylomatic/"]
 	
	meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': source_urls} #'service_documentation': service_documentation
 	final_result['meta_data'] = meta_data 
 	final_result['input_taxa'] = taxaList 	 

 	return final_result    
 	
#-----------------------------------------------
#if __name__ == '__main__':
 	#input_list = ["Panthera uncia", "Panthera onca", "Panthera leo", "Panthera pardus"]
 	#input_list = ["Annona cherimola", "Annona muricata", "Quercus robur", "Shorea parvifolia" ]
 	#input_list = ["Quercus robur", "Quercus petraea", "Castanea sativa", "Salix alba"]
 	#print tree_controller(input_list)

