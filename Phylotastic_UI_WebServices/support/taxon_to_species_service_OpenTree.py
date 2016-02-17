import json
import requests
import time

#Open Tree of Life API
api_url = "https://api.opentreeoflife.org/v2/"
headers = {'content-type': 'application/json'}

#----------------------------------------------
def match_taxon(taxonName):
    resource_url = api_url + "tnrs/match_names"    
    payload = {
        'names': [taxonName], 
        'do_approximate_matching': 'false'
    }
    response = requests.post(resource_url, data=json.dumps(payload), headers=headers)
     
    data_json = json.loads(response.text)
    length = len(data_json['results']) 
    
    if length == 0:
        return -1 
    else: 
        return data_json['results'][0]['matches'][0]['ot:ottId']

#-------------------------------------------
def get_children(ottId):
    resource_url = api_url + "taxonomy/taxon"    
    payload = {
        'ott_id': ottId,
        'include_children': 'true'    
    }
    response = requests.post(resource_url, data=json.dumps(payload), headers=headers)
     
    #print response.text 
    return json.loads(response.text)

#----------------------------------------    
def get_species_from_class(classChildren):
    species_list = [] 
    #get all family of a order    
    for child in classChildren: 
        species_lst = []
        if child['rank'] == 'order':
 		 	#get all family of a order
 			res_json = get_children(child['ot:ottId'])
 			children_lst = res_json['children']
 			if len(children_lst) == 0:
 				continue
 			species_lst = get_species_from_order(children_lst)
        #extend the species list with the species of this genus
        species_list.extend(species_lst)         
                    
    return species_list

#----------------------------------------    
def get_species_from_order(orderChildren):
    species_list = [] 
    #get all family of a order    
    for child in orderChildren: 
        species_lst = []
        if child['rank'] == 'family':
 			#get all genus of a family
 			res_json = get_children(child['ot:ottId'])
 			children_lst = res_json['children']
 			if len(children_lst) == 0:
 				continue
 			species_lst = get_species_from_family(children_lst)
        #extend the species list with the species of this genus
        species_list.extend(species_lst)         
                    
    return species_list

#--------------------------------------------
def get_species_from_family(familyChildren):
    species_list = [] 
    #get all genus of a family    
    for child in familyChildren:
        species_lst = [] 
        if child['rank'] == 'genus':
 			#get all species of a genus
 			res_json = get_children(child['ot:ottId'])
 			children_lst = res_json['children']
 			if len(children_lst) == 0:
 				continue
 			species_lst = get_species_from_genus(children_lst)
        #extend the species list with the species of this genus
        species_list.extend(species_lst)         
                           
    return species_list

#-------------------------------------------
def get_species_from_genus(genusChildren):
    species_list = []
    #get all species of a genus 
    for child in genusChildren:
 		if child['rank'] == 'species':
 			species_list.append(child['ot:ottTaxonName'])            
        
    return species_list

#-------------------------------------------------    
def check_species_by_country(species, countries):
    INaturalistApi_url = 'https://www.inaturalist.org/places.json'

    payload = {
        'taxon': species,
        'place_type': 'Country',
    }    
    
    matched_result = requests.get(INaturalistApi_url, params=payload)
    res_json = json.loads(matched_result.text) 
    
    countryList = []
    for country in res_json:
        countryList.append(country['name'])
    
    commonList = list(set(countries).intersection(set(countryList)))
    
    if len(commonList) > 0:
        return True
    else:
        return False

#---------------------------------------------------
def get_all_species(inputTaxon):
 	
 	ott_id = match_taxon(inputTaxon)
 	if ott_id == -1:
 		final_result = create_json_msg([], 'No Taxon found', 404)
 		return final_result

 	data_json = get_children(ott_id)
 	if data_json['rank'] == 'genus':
 		species_list = get_species_from_genus(data_json['children'])
 	elif data_json['rank'] == 'family':
 		species_list = get_species_from_family(data_json['children'])
 	elif data_json['rank'] == 'order':
 		species_list = get_species_from_order(data_json['children'])
 	elif data_json['rank'] == 'class':
 		species_list = get_species_from_class(data_json['children'])
 	else:
		species_list = []
    
 	#species_list.sort()
 	len_splist = len(species_list)
 	
 	if len_splist != 0:
 	 	final_result = create_json_msg(species_list, 'Success', 200)
 	else:	
 	 	final_result = create_json_msg(species_list, 'Too many species for a higher ranked taxon', 204)

 	return final_result

#--------------------------------------------------
def get_country_species(inputTaxon, country):
 	
 	all_species_result = get_all_species(inputTaxon)  
  	
	all_species_json = json.loads(all_species_result)
 	status_code = all_species_json['statuscode']
  	species_list = all_species_json['species']
 	message = all_species_json['message']	
 	
 	#species_list.sort()
    #countries = ['Bhutan', 'Nepal', 'Canada']

 	len_splist = len(species_list)
  	
 	if status_code == 404:  #no taxon found
  		return species_json
 	elif status_code == 204: #high rank taxon
 		return species_json
 	elif status_code == 200:
 		countries = [country]
 		species_lst = []
 		for species in species_list:
 			if check_species_by_country(species, countries):
 				species_lst.append(species)
  	
 	if len(species_lst) != 0: 	
 	 	final_result = create_json_msg(species_lst, 'Success', 200)
   	else:
 		final_result = create_json_msg(species_lst, 'No species found on this country', 206)
 	
 	return final_result
 	
#--------------------------------------------

def create_json_msg(species_lst, msg, code):
 	
 	return json.dumps({'species': species_lst, 'message': msg, 'statuscode': code})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

	inputTaxon = 'Vulpes' #genus
 	#inputTaxon = 'Canidae' #family
    #inputTaxon = 'Carnivora' #order
 	#inputTaxon = 'Arthropoda'
	#inputTaxon = 'Arthra'   #invalid input
 	country = 'Nepal'
 	#country = 'Brazil'
 	start_time = time.time()    
 	
 	print get_all_species(inputTaxon)
 	print get_country_species(inputTaxon, country)
 	end_time = time.time()
 	
 	print end_time-start_time
