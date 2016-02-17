import json
import requests

#GBIF API
api_url = "http://api.gbif.org/v1/species/"

def get_children(taxonKey):
    resource_url = api_url + str(taxonKey) + "/children"    
    payload = {
        'limit': 1000,   
    }
    children_result = requests.get(resource_url, params=payload)
    res_json = json.loads(children_result.text)
        
    children_list = []
    for child in res_json['results']:
        childAtt = {}         
        childAtt['canonicalName'] = child['canonicalName']
        childAtt['key'] = child['key']
        children_list.append(childAtt)
        
    return children_list

#---------------------------------------------
def get_species_from_class(classKey):
    species_list = [] 
    #get all family of a order    
    order_list = get_children(classKey)
    for order in order_list: 
        children_lst = get_species_from_order(order['key'])
        for child in children_lst:         
            species_list.append(child)            
        
    return species_list

#---------------------------------------------
def get_species_from_order(orderKey):
    species_list = [] 
    #get all genus of a family    
    family_list = get_children(orderKey)
    for family in family_list: 
        children_lst = get_species_from_family(family['key'])
        for child in children_lst:         
            species_list.append(child)            
        
    return species_list

#------------------------------------------
def get_species_from_family(familyKey):
    species_list = [] 
    #get all genus of a family    
    genus_list = get_children(familyKey)
    for genus in genus_list: 
        children_lst = get_species_from_genus(genus['key'])
        for child in children_lst:         
            species_list.append(child)            
        
    return species_list

def get_species_from_genus(genusKey):
    species_list = []
    #get all species of a genus 
    children_lst = get_children(genusKey)
    for child in children_lst: 
        species_list.append(child['canonicalName'])            
        
    return species_list
                
def match_taxon(taxonName):
    resource_url = api_url + "match"    
    payload = {
        'name': taxonName,
        'verbose': 'true',
        'strict': 'true'
    }    
    
    matched_result = requests.get(resource_url, params=payload)
    res_json = json.loads(matched_result.text) 
    
    taxonAtt = {}
    taxonAtt['matchType'] = res_json['matchType']
    if res_json['matchType'] == 'NONE':
        for s in res_json['alternatives']:
            if s['matchType'] == 'EXACT':
                taxonAtt['matchType'] = s['matchType']                
                taxonAtt['rank'] = s['rank']
                taxonAtt['canonicalName'] = s['canonicalName']
                taxonAtt['usageKey'] = s['usageKey']                
                break;
    else:
        taxonAtt['matchType'] = res_json['matchType']
        taxonAtt['rank'] = res_json['rank']
        taxonAtt['canonicalName'] = res_json['canonicalName']
        taxonAtt['usageKey'] = res_json['usageKey']
    
    return taxonAtt
    
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


def get_all_species(inputTaxon):
    
    result = match_taxon(inputTaxon)
    if result['rank'] == 'GENUS':
        species_list = get_species_from_genus(result['usageKey'])
    elif result['rank'] == 'FAMILY':
        species_list = get_species_from_family(result['usageKey'])        
    elif result['rank'] == 'ORDER':
        species_list = get_species_from_order(result['usageKey'])
 	elif result['rank'] == 'CLASS':
        species_list = get_species_from_class(result['usageKey'])
    
    #species_list.sort()
    
    return json.dumps({'species': species_list})	


def get_country_species(inputTaxon, countries):
    
    result = match_taxon(inputTaxon)
    if result['rank'] == 'GENUS':
        species_list = get_species_from_genus(result['usageKey'])
    elif result['rank'] == 'FAMILY':
        species_list = get_species_from_family(result['usageKey'])        
    elif result['rank'] == 'ORDER':
        species_list = get_species_from_order(result['usageKey'])   
    elif result['rank'] == 'CLASS':
        species_list = get_species_from_class(result['usageKey'])
    
 	#species_list.sort()
   
    #countries = ['Bhutan', 'Nepal', 'Canada']
    
    countries = [country]	

    species_lst = []
    for species in species_list:    
        if check_species_by_country(species, countries):        
            species_lst.append(species)
    
    return json.dumps({'species': species_lst})


'''
if __name__ == '__main__':
    inputTaxon = 'Vulpes'
    
    result = match_taxon(inputTaxon)
    if result['rank'] == 'GENUS':
        species_list = get_species_from_genus(result['usageKey'])
    elif result['rank'] == 'FAMILY':
        species_list = get_species_from_family(result['usageKey'])        
    elif result['rank'] == 'ORDER':
        species_list = get_species_from_order(result['usageKey'])   
    
    species_list.sort()
    
    print json.dumps({'species': species_list})    
'''    
