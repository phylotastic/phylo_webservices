#service description: get species in a named taxon that have genomes in the genomes division of NCBI 
#service version: 1.0
import json
import requests
import time
import datetime 
import urllib

#----------------------------------------------
base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
headers = {'content-type': 'application/json'}

#----------------------------------------------
#get genome ids available for a named taxonomic group
def find_genome_ids(taxonName):
 	api_func = "esearch.fcgi"	
 	api_url = base_url + api_func    
 	payload = {
 		'retmax': 5000,
 		'retmode': 'json',
 		'db': 'genome',
 		'term': taxonName,
 		'tool': "phylotastic-services",
 		'email': "tayeen@nmsu.edu"      
    }
 	encoded_payload = urllib.urlencode(payload)
 	response = requests.get(api_url, params=encoded_payload, headers=headers) 
 	
 	gid_list = []
 	genome_response = {}    
 	genome_response['status_code'] = 200
 	genome_response['message'] = "Success"
 	
 	if response.status_code == requests.codes.ok:    
 		data_json = json.loads(response.text)
 		numResults = int(data_json['esearchresult']['count']) 
 		gid_list = data_json['esearchresult']['idlist']  
 	else: 
 		genome_response['status_code'] = 500
 		genome_response['message'] = "Error: Response error from NCBI esearch.fcgi API"

	genome_response['genome_ids'] = gid_list
 	
 	if numResults == 0:
  	 	genome_response['message'] = "No match found for term %s" %(taxonName)
 		genome_response['status_code'] = 204
 	
 	return genome_response 	

#--------------------------------------------   
#get the species ids associated with genome ids
def find_species_ids(genomeIds):
 	api_func = "elink.fcgi"	
 	api_url = base_url + api_func    
 	payload = {
 		'retmax': 5000,
 		'retmode': 'json',
 		'dbfrom' : 'genome',
 		'db': 'taxonomy',
 		'id': genomeIds,
 		'tool': "phylotastic-services",
 		'email': "tayeen@nmsu.edu"
    }
 	encoded_payload = urllib.urlencode(payload)
 	response = requests.get(api_url, params=encoded_payload, headers=headers) 
 	#response = requests.post(api_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})

 	sid_list = []
 	taxonomy_response = {}    
 	taxonomy_response['status_code'] = 200
 	taxonomy_response['message'] = "Success"

 	if response.status_code == requests.codes.ok:    
 		data_json = json.loads(response.text)
 		sid_list = data_json['linksets'][0]['linksetdbs'][0]['links'] 
 	else:
 		taxonomy_response['status_code'] = 500
 		taxonomy_response['message'] = "Error: Response error from NCBI elink.fcgi API"
 	
 	taxonomy_response['species_ids'] = sid_list

 	return taxonomy_response

#--------------------------------------------   
#get the species names associated with species ids
def get_species_names(speciesIds):
 	api_func = "esummary.fcgi"	
 	api_url = base_url + api_func    
 	payload = {
 		'retmax': 5000,
 		'retmode': 'json',
 		'db': 'taxonomy',
 		'id': speciesIds,
 		'tool': "phylotastic-services",
 		'email': "tayeen@nmsu.edu"
    }
 	encoded_payload = urllib.urlencode(payload)
 	response = requests.get(api_url, params=encoded_payload, headers=headers) 
 	#response = requests.post(api_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})

 	sname_list = []
 	taxonomy_response = {}    
 	taxonomy_response['status_code'] = 200
 	taxonomy_response['message'] = "Success"

 	if response.status_code == requests.codes.ok:    
 		data_json = json.loads(response.text)
 		uid_list = data_json['result']['uids']
 		for uid in uid_list:
 			sname_list.append(data_json['result'][str(uid)]['scientificname']) 
 	else:
 		taxonomy_response['status_code'] = 500
 		taxonomy_response['message'] = "Error: Response error from NCBI elink.fcgi API"
 	
 	taxonomy_response['species'] = sname_list

 	return taxonomy_response
 	
#----------------------------------------------
#form comma separated ids for the APIs 
def form_cs_ids(id_list):
 	str_ids = ""
 	length = len(id_list)
 	count = 0
 	for Id in id_list:
 		count = count + 1
 		str_ids = str_ids + str(Id)
 		if count != length:
 			str_ids = str_ids + ","
 			
 	return str_ids
 	
#---------------------------------------------------
def get_genome_species(inputTaxon):	
 	start_time = time.time()
 	service_url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi/genome_species?taxon=" + inputTaxon
 	service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-9"

 	final_result = {}	
 	g_response = find_genome_ids(inputTaxon)
 	
 	if g_response['status_code'] != 200:	 	
 		final_result = g_response
 	else:
 		str_gids = form_cs_ids(g_response['genome_ids'])
 		s_response = find_species_ids(str_gids)
 		if s_response['status_code'] != 200:
 			final_result = s_response
 		else:
 			str_sids = form_cs_ids(s_response['species_ids'])
 			final_result = get_species_names(str_sids)
	
 	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	
 	final_result['creation_time'] = creation_time
 	final_result['execution_time'] = "{:4.2f}".format(execution_time)
 	if final_result['status_code'] == 200: 
 		final_result['total_names'] = len(final_result['species'])
 	else:
 		final_result['total_names'] = 0 
 	final_result['source_urls'] = ["https://www.ncbi.nlm.nih.gov/taxonomy", "https://www.ncbi.nlm.nih.gov/genome"]
 	#final_result['source_version'] = "ott2.9draft12"
 	final_result['service_url'] = service_url
 	final_result['service_documentation'] = service_documentation	
 	final_result['taxon'] = inputTaxon

 	return final_result #return json.dumps(final_result)
#--------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':

	#inputTaxon = 'Vulpes' #'Panthera'
 	inputTaxon = 'Rodentia'
	#inputTaxon = 'Canidae' #family
 	
 	#start_time = time.time()    
 	
 	print get_genome_species(inputTaxon)
 	
 	#end_time = time.time()
 	
 	#print end_time-start_time

