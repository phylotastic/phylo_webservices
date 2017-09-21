#species to eol URL service: version 1
import json
import requests
import time
import datetime 
import urllib

#----------------------------------------------
EOL_API_Key = "b6499be78b900c60fb28d38715650e826240ba7b"
headers = {'content-type': 'application/json'}

#----------------------------------------------
def match_species(speciesName):
 	search_url = "http://eol.org/api/search/1.0.json"    
 	payload = {
 		'key': EOL_API_Key,
 		'q': speciesName,
 		'page': 1,
 		'exact': True,
 		'filter_by_taxon_concept_id': "",
 		'filter_by_hierarchy_entry_id': "",
 		'filter_by_string': "", 
 		'cache_ttl': ""
    }
 	encoded_payload = urllib.urlencode(payload)
 	response = requests.get(search_url, params=encoded_payload, headers=headers) 
    
 	if response.status_code == requests.codes.ok:    
 		data_json = json.loads(response.text) 
 		numResults = data_json['totalResults']
 	 	
 	if numResults == 0:
 		return None 
 	else: 
 		return data_json

#---------------------------------------------------
def get_eolurls_species(inputSpeciesList, post=False):
 	start_time = time.time()
 	#service_url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/get_images?species=" + inputSpeciesList
 	service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-10"
 	response = {}	
 	outputSpeciesList = []

 	for inputSpecies in inputSpeciesList:
 		species_obj = {}
 		url_species = []	 	
 		match_species_json = match_species(inputSpecies)
 		species_obj['searched_name'] = inputSpecies	 	
 		if match_species_json is None:		 	
 			species_obj['matched_name'] = ""
 		else: 	
 		 	species_info_link = match_species_json['results'][0]['link']
 			species_obj['matched_name'] = match_species_json['results'][0]['title']
 			species_obj['eol_id'] = match_species_json['results'][0]['id']			
 			species_obj['species_info_link'] = species_info_link 
 				
 		outputSpeciesList.append(species_obj)	
 	
 	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	
 	response['creation_time'] = creation_time
 	response['execution_time'] = "{:4.2f}".format(execution_time)
 	response['message'] = "Success"
 	response['status_code'] = 200
 	response['species'] = outputSpeciesList
 	response['source_urls'] = ["http://eol.org"]
 	#final_result['source_version'] = "ott2.9draft12"
 	#response['service_url'] = service_url
 	response['service_documentation'] = service_documentation
 	response['input_query'] = inputSpeciesList


 	return response
 	#if post:
 	#	return response
 	#else:
 	# 	return json.dumps(response)
#--------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':

#	inputSpecies = ["Panthera leo", "Panthera onca"]
 	#inputTaxon = 'Felidae'
	
 	#start_time = time.time()    
 	
 	#print get_eolurls_species(inputSpecies)
 	
 	#end_time = time.time()
 	
 	#print end_time-start_time
