#species-habitat service: version 1.0
import json
import time
import requests
import datetime
import ConfigParser

from os.path import dirname, abspath

#============================================
base_url = "http://eol.org/api/"

#------------------------------------------
def get_api_key():
	config = ConfigParser.ConfigParser()
	current_dir = dirname(abspath(__file__))
	config.read(current_dir + "/"+ "habitat_service.cfg")
	
	eol_api_key = config.get('EOL', 'api_key')

	return eol_api_key

#----------------------------------------------
def match_species(species_name):
	EOL_API_Key = get_api_key()

	search_url = base_url+"search/1.0.json"    
	payload = {
 		'key': EOL_API_Key,
 		'q': species_name,
 		'page': 1,
 		'exact': True,
 		'filter_by_taxon_concept_id': "",
 		'filter_by_hierarchy_entry_id': "",
 		'filter_by_string': "", 
 		'cache_ttl': ""
    }
 	
	#encoded_payload = urllib.urlencode(payload)
	response = requests.get(search_url, params=payload) 

	match_result = {}     
 	if response.status_code == requests.codes.ok:    
		data_json = json.loads(response.text) 
		numResults = data_json['totalResults']
		if numResults != 0:
			match_result['matched_name'] = data_json['results'][0]['title']
			match_result['eol_id'] = data_json['results'][0]['id']
		else:
			match_result['matched_name'] = ""
			match_result['eol_id'] = ""
	else:	 	
 		match_result = None
 	 
 	return match_result

#----------------------------------------------------
def get_traits(species_eol_id):
	traits_url = base_url+ "traits/" + str(species_eol_id)   
	
	response = requests.get(traits_url) 

	trait_result = {}
	habitats_set = set()
	conservation_status = None
     
 	if response.status_code == requests.codes.ok:    
		data_json = json.loads(response.text) 
		trait_result['matched_species'] = data_json['item']['scientificName']
		traits_list = data_json['item']['traits']
		for trait in traits_list:
			if trait['predicate'] == "habitat":
				habitats_set.add(trait['value'])
			elif trait['predicate'] == "conservation status":		
				conservation_status = trait['value']

		trait_result['habitats'] = list(habitats_set)
		trait_result['conservation_status'] = conservation_status	
	else:	 	
 		trait_result = None
 	 
 	return trait_result


#---------------------------------------------------
def get_habitat_conservation(inputSpeciesList):
	start_time = time.time()

	response = {}	
	outputSpeciesList = []

	for inputSpecies in inputSpeciesList:
		species_obj = {}	 	
		match_species_result = match_species(inputSpecies)
		species_obj['searched_name'] = inputSpecies	 	
		if match_species_result is None:		 	
			species_obj['matched_name'] = ""		
		elif match_species_result['eol_id'] != "":
			species_habitat_info = get_traits(match_species_result['eol_id'])
			if species_habitat_info is not None:
				species_obj['eol_id'] = match_species_result['eol_id']
			 	species_obj['habitats'] = species_habitat_info['habitats']
				species_obj['conservation_status'] = species_habitat_info['conservation_status']
				species_obj['matched_name'] = species_habitat_info['matched_species']
			else:
				species_obj['habitats'] = []
				species_obj['matched_name'] = []
		else:
			species_obj['matched_name'] = "" 
 				
		outputSpeciesList.append(species_obj)	
 	
	end_time = time.time()
	execution_time = end_time-start_time
    #service result creation time
	creation_time = datetime.datetime.now().isoformat()
	meta_data = {'creation_time': creation_time, 'execution_time': float('{:4.2f}'.format(execution_time)), 'source_urls':["http://eol.org/traitbank"] }

	response['meta_data'] = meta_data
 	
	response['message'] = "Success"
	response['status_code'] = 200
	response['species'] = outputSpeciesList

	return response

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':

#	inputSpecies = ["Potos flavus", "Panthera leo"]
 	
# 	print get_habitat_species(inputSpecies)
 	
 	
