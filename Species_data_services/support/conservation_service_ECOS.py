#species-conservation service: version 1.0
import json
import time
import requests
import datetime
import xml.etree.ElementTree as ET

#============================================
#https://ecos.fws.gov/ecp/species-query
#=============================================

#---------------------------------------------------
def get_conservation(inputSpeciesList):
	start_time = time.time()

	response = {}	
	outputSpeciesList = []
	error_resp_list = []

	for inputSpecies in inputSpeciesList:
		species_obj = {}	 	
		match_species_result = search_species(inputSpecies)
		species_obj['searched_name'] = inputSpecies	 	
		if match_species_result is None:		 	
			error_resp_list.append(inputSpecies)		
		else:
			species_conservation_info = parse_xml(match_species_result)
			if species_conservation_info is not None:
				species_obj['tsn_id'] = species_conservation_info['tsn_id']
				species_obj['conservation_status'] = species_conservation_info['conservation_status']
				species_obj['matched_name'] = species_conservation_info['matched_name']
			else:
				species_obj['matched_name'] = "" 
 				
			outputSpeciesList.append(species_obj)	
 	
	end_time = time.time()
	execution_time = end_time-start_time
    #service result creation time
	creation_time = datetime.datetime.now().isoformat()
	meta_data = {'creation_time': creation_time, 'execution_time': float('{:4.2f}'.format(execution_time)), 'source_urls':["https://ecos.fws.gov/ecp/services"] }
	
	if len(error_resp_list) == len(inputSpeciesList):
		response['message'] = "Error while getting response from ECOS API"
		response['status_code'] = 500	
	else:
		response['meta_data'] = meta_data
 		response['message'] = "Success"
		response['status_code'] = 200
		response['species'] = outputSpeciesList

	return response

#----------------------------------------------
#https://ecos.fws.gov/ecp0/TessQuery?request=query&xquery=/SPECIES_DETAIL[SCINAME=%22Panthera%20tigris%22]
def search_species(species_name):
	api_url = "https://ecos.fws.gov/ecp0/TessQuery"    
	payload = {
 		'request': "query",
 		'xquery': "/SPECIES_DETAIL[SCINAME="+'"'+species_name+'"]'
    }
 	
	response = requests.get(api_url, params=payload) 

	xml_result = None     
 	if response.status_code == requests.codes.ok:    
		xml_result = response.text
		
	return xml_result 

#----------------------------------------
def parse_xml(xml_str):
	root = ET.fromstring(xml_str)
	if len(root) == 0: #no match found
		return None
	#print root.tag
	detail = root.find('SPECIES_DETAIL')
	sc_name = detail.find('SCINAME').text
	conservaion_status = detail.find('STATUS_TEXT').text
	tsn_id = detail.find('TSN').text

	return {'matched_name': sc_name, 'tsn_id': tsn_id, 'conservation_status': conservaion_status}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':

	#inputSpecies = ["Pongo pygmaeus", "Rhinoceros sondaicus", "Panthera tigris", "Pan troglodytes", "Loxodonta africana"]
	#https://www.worldwildlife.org/species/directory
	#inputSpecies = ["Ursus maritimus", "Ailuropoda melanoleuca", "Vulpes lagopus", "Delphinapterus leucas", "Diceros bicornis", "Balaenoptera musculus", "Pan paniscus", "Balaena mysticetus", "Pan troglodytes", "Balaenoptera physalus", "Carcharodon carcharias", "Chelonia mydas", "Hippopotamus amphibius", "Orcaella brevirostris", "Panthera onca", "Dermochelys coriacea", "Ara ararauna", "Amblyrhynchus cristatus"]
 	#inputSpecies = "unknown"#"Panthera tigris"
	#print len(inputSpecies)
 	#print get_conservation(inputSpecies)
 	
 	
