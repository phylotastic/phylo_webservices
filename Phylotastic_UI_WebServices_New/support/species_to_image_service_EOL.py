#species to image service: version 2.0 (based on new EOL API)
#https://eol.org/docs/what-is-eol/data-services/classic-apis
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
    
 	numResults = 0
 	eol_response = {}
 	if response.status_code == requests.codes.ok:    
 		data_json = json.loads(response.text)
 		numResults = data_json['totalResults']
 		eol_response['status_code'] = 200
 		eol_response['message'] = "Success"    
 	else:
 		eol_response['status_code'] = response.status_code
 		eol_response['message'] = "Error: Response error from EOL while matching species name."

 	if numResults == 0:
 		eol_response['eol_id'] = -1 
 	else: 
 		eol_response['eol_id'] = data_json['results'][0]['id']

 	return eol_response

#--------------------------------------------   
def get_species_info(speciesId):
 	page_url = "http://eol.org/api/pages/1.0/" + str(speciesId) +".json"    
 	payload = {
 		'key': EOL_API_Key,
 		'batch' : False,
 		'id': speciesId,
 		'images_per_page': 5,
 		'images_page': 1,
 		'videos_per_page': 0,
 		'videos_page': 0,
 		'sounds_per_page': 0,
 		'sounds_page': 0,
 		'maps_per_page': 0,
 		'maps_page': 0,
 		'texts_per_page': 0,
 		'texts_page': 0,
 		'iucn': True, #include the IUCN Red List status object
 		'subjects': "overview",  #'overview' to return the overview text (if exists)
 		'licenses': "all",
 		'details': True, #include all metadata for data objects
 		'common_names': False,
 		'synonyms': False,
 		'references': False,
 		'taxonomy': True,
 		'vetted': 2, # only trusted and unreviewed content will be returned (untrusted content will not be returned)
 		'cache_ttl': "", 
 		'language': "en"
    }
 	encoded_payload = urllib.urlencode(payload)
 	response = requests.get(page_url, params=encoded_payload, headers=headers) 
    
 	if response.status_code == requests.codes.ok:    
 		species_info_json = json.loads(response.text)
 		return species_info_json
 	else:
 		return None
 		
#--------------------------------------------
def get_imageObjects(dataObjectsInfo):
 	species_imageobj_list = []
 	for dt_obj in dataObjectsInfo:
 		if dt_obj['dataType'] == 'http://purl.org/dc/dcmitype/StillImage':
 			img_obj = create_image_obj(dt_obj)
 			species_imageobj_list.append(img_obj)

 	return species_imageobj_list

#----------------------------------------------
def create_image_obj(dataObject):
 	#print dataObject
 	image_obj = {}
 	image_obj['source'] = dataObject['source'] if 'source' in dataObject else None
 	image_obj['vettedStatus'] = dataObject['vettedStatus']
 	image_obj['dataRating'] = dataObject['dataRating']
 	image_obj['mediaURL'] = dataObject['mediaURL']
 	image_obj['eolMediaURL'] = dataObject['eolMediaURL']
 	image_obj['eolThumbnailURL'] = dataObject['eolThumbnailURL']
 	image_obj['license'] = dataObject['license']
 	if dataObject.has_key('rightsHolder'):
 		image_obj['rightsHolder'] = dataObject['rightsHolder']
 	else:
 		image_obj['rightsHolder'] = ""

 	return image_obj

#---------------------------------------------------
def get_images_species(inputSpeciesList, post=False):
 	start_time = time.time()
 	
 	response = {}	
 	outputSpeciesList = []

 	for inputSpecies in inputSpeciesList:
 		species_obj = {}
 		images_species = []	 	
 		eol_response = match_species(inputSpecies)
 		if eol_response['status_code'] != 200:
 			return eol_response
 		species_id = eol_response['eol_id'] 
 		species_obj['searched_name'] = inputSpecies	 	
 		if species_id == -1:		 	
 			species_obj['matched_name'] = ""
 			species_obj['total_images'] = 0
 		else: 	
 		 	species_info_json = get_species_info(species_id)
 			if species_info_json is None:
 				return { 'status_code': 500, 'message': "Error: Response error from EOL while retrieving data objects"}
 			else:
 				species_obj['matched_name'] = species_info_json[str(species_id)]['scientificName']
 				species_obj['eol_id'] = species_id			
 				dataObjects_lst = species_info_json[str(species_id)]['dataObjects']
 				length = len(dataObjects_lst)		
 				if length != 0:
 					images_species = get_imageObjects(dataObjects_lst)
 					
 		species_obj['total_images'] = len(images_species)
 		species_obj['images'] = images_species
 		outputSpeciesList.append(species_obj)
	
 	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	
 	meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["http://eol.org"]}

 	response['meta_data'] = meta_data
 	
 	response['message'] = "Success"
 	response['status_code'] = 200
 	response['species'] = outputSpeciesList
 	response['input_species'] = inputSpeciesList
 
 	return response
 	
#--------------------------------------------------
def get_image_species_id(species_id, post=False):
 	response = {}	
 	species_obj = {}
 	species_info_json = get_species_info(species_id)
 	if species_info_json is not None:
 		species_obj['matched_name'] = species_info_json['scientificName']
 		species_obj['eol_id'] = species_id			
 		dataObjects_lst = species_info_json['dataObjects'] 
 		length = len(dataObjects_lst)		
 		if length != 0:
 			images_species = get_imageObjects(dataObjects_lst)
 		else:
			images_species = []

 		species_obj['images'] = images_species
 	else:
 		return {'message': "Error: Response error from EOL while obtaining species info", 'status_code': 500}	

 	response['message'] = "Success"
 	response['status_code'] = 200
 	response['species'] = species_obj

 	if post:
 		return response
 	else:
 	 	return json.dumps(response)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

	inputSpecies = ["Panthera leo"]#, "Panthera onca", "Panthera pardus"]
 	#inputTaxon = 'Panthera leo'
	#inputTaxon = 'Canidae' #family
 	
 	#start_time = time.time()    
 	
 	print get_images_species(inputSpecies)
 	
 	#end_time = time.time()
 	
 	#print end_time-start_time
