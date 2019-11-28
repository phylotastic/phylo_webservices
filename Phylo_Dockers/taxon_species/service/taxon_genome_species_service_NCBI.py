#service description: get species in a named taxon that have genomes in the genomes division of NCBI 
#service version: 1.0
import json
import requests
import time
import datetime 

#----------------------------------------------
base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
headers = {"Content-Type": "application/x-www-form-urlencoded"}

#----------------------------------------------
#get genome ids available for a named taxonomic group
def find_genome_ids(taxonName):
 	api_func = "esearch.fcgi"	
 	api_url = base_url + api_func    
 	payload = {
 		'retmax': 5000,
 		'retmode': 'json',
 		'db': 'genome',
 		'term': taxonName + " [Organism]",
 		'tool': "phylotastic-services",
 		'email': "tayeen@nmsu.edu"      
    }
 	try:
 		#encoded_payload = urllib.urlencode(payload)
 		response = requests.get(api_url, params=payload, headers=headers) 
 	
 		gid_list = []
 		genome_response = {}    
 		genome_response['status_code'] = 200
 		genome_response['message'] = "Success"
 	
 		if response.status_code == requests.codes.ok:    
 			data_json = json.loads(response.text)
 			numResults = int(data_json['esearchresult']['count'])
 			if numResults == 0:
  	 			genome_response['message'] = "No match found for term %s" %(taxonName)
 			else:	 
 				gid_list = data_json['esearchresult']['idlist']  
 		else: 
 			genome_response['status_code'] = response.status_code
 			genome_response['message'] = "Error: Response error from NCBI esearch.fcgi API"

 	except Exception as e:
 		genome_response['status_code'] = 500
 		genome_response['message'] = "Error: exception in find_genome_ids() method"

 	genome_response['genome_ids'] = gid_list
 	#print len(gid_list) 	 	
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
 	sid_list = []
 	taxonomy_response = {}    
 	try:	
 		#encoded_payload = urllib.urlencode(payload)
 		response = requests.get(api_url, params=payload, headers=headers) 
 		#response = requests.post(api_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
 		
 		taxonomy_response['status_code'] = 200
 		taxonomy_response['message'] = "Success"

 		if response.status_code == requests.codes.ok:    
 			data_json = json.loads(response.text)
 			sid_list = data_json['linksets'][0]['linksetdbs'][0]['links'] 
 			#print sid_list
 		else:
 			taxonomy_response['status_code'] = response.status_code
 			taxonomy_response['message'] = "Error: Response error from NCBI elink.fcgi API"
 	
 	except Exception as e:
 		taxonomy_response['status_code'] = 500
 		taxonomy_response['message'] = "Error: exception in find_species_ids() method"

 	taxonomy_response['species_ids'] = sid_list

 	return taxonomy_response

#--------------------------------------------   
#get the species names associated with species ids
def get_species_names(speciesIds):
 	api_func = "esummary.fcgi"	
 	api_url = base_url + api_func    
 	payload = {
 		'retmax': 500,
 		'retmode': 'json',
 		'db': 'taxonomy',
 		'id': speciesIds,
 		'tool': "phylotastic-services",
 		'email': "tayeen@nmsu.edu"
    }
 	#encoded_payload = urllib.urlencode(payload)
 	response = requests.get(api_url, params=payload, headers=headers) 
 	#response = requests.post(api_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})

 	sname_list = []
 	taxonomy_response = {}    
 	taxonomy_response['status_code'] = 200
 	taxonomy_response['message'] = "Success"

 	try:
 		if response.status_code == requests.codes.ok:    
 			data_json = json.loads(response.text)
 			uid_list = data_json['result']['uids']
 			for uid in uid_list:
 				if 'scientificname' in data_json['result'][str(uid)]:
 					if 'rank' in data_json['result'][str(uid)] and data_json['result'][str(uid)]['rank'] == "species": 
 						sname_list.append(data_json['result'][str(uid)]['scientificname'])
 		else:
 			taxonomy_response['status_code'] = response.status_code
 			taxonomy_response['message'] = "Error: Response error from NCBI esummary.fcgi API"
 	
 	except Exception as e:
 		taxonomy_response['status_code'] = 500
 		taxonomy_response['message'] = "Error: exception in get_species_name() method"
		
 	taxonomy_response['species'] = sname_list
 	#print sname_list
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
 	
#-----------------------------------------
def create_sublists(lst, size=500):
	return [lst[i:i+size] for i in xrange(0, len(lst), size)]

#---------------------------------------------------
def get_genome_species(inputTaxon):	
 	start_time = time.time()
 	list_size = 300
 	final_species_list = []

 	final_result = {'status_code': 200, 'message': "Success"}	
 	g_response = find_genome_ids(inputTaxon)
 	
 	if g_response['status_code'] != 200:	 	
 		final_result = g_response
 	else:
 		g_id_list = g_response['genome_ids']
 		#print g_id_list
 		if len(g_id_list) != 0:
 			sp_list = []
 			if len(g_id_list) > list_size:
 				g_sub_lists = create_sublists(g_id_list, list_size)
 				for gsb_lst in g_sub_lists:
 					str_gids = form_cs_ids(gsb_lst)
 					s_response = find_species_ids(str_gids)
 					if s_response['status_code'] != 200:
 						final_result = s_response
 						break
 					sp_list.extend(s_response['species_ids'])
 					time.sleep(.500) #wait 500 ms to avoid choking the NCBI API and getting blocked 
 			else:
 				str_gids = form_cs_ids(g_id_list)
 				sp_list = find_species_ids(str_gids)['species_ids'] 						
 			#print sp_list
 			
 			#to handle large number of species
 			if len(sp_list) > list_size:
 				sublists = create_sublists(sp_list, list_size)
 				#print "Number of sublists: %d"%len(sublists)
 				for sublst in sublists:
 					str_sids = form_cs_ids(sublst)
 					final_species_list.extend(get_species_names(str_sids)['species'])
 					time.sleep(.500) #wait 500 ms to avoid choking the NCBI API and getting blocked
 					#print len(final_species_list)
 						
 			else:
 				str_sids = form_cs_ids(sp_list)
 				final_species_list = get_species_names(str_sids)['species']

 			final_result['species'] = final_species_list
 		else:
 			final_result['message'] = g_response['message']
 			final_result['species'] = g_response['genome_ids']

 	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	
 	meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls': ["https://www.ncbi.nlm.nih.gov/taxonomy", "https://www.ncbi.nlm.nih.gov/genome"]} 
  
 	final_result['meta_data'] = meta_data
 	
 	if 'status_code' in final_result and final_result['status_code'] == 200: 
 		final_result['total_names'] = len(final_result['species'])
 	else:
 		final_result['total_names'] = 0 
 		
 	final_result['input_taxon'] = inputTaxon

 	return final_result #return json.dumps(final_result)
#--------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/

#if __name__ == '__main__':

	#inputTaxon = 'Vulpes' #'Panthera'
 	#inputTaxon = 'Rodentia'
	#inputTaxon = 'Canidae' #family
 	#inputTaxon = 'Primates' #family
 	#inputTaxon= "Enterobacteriaceae"
 	#inputTaxon="Eukaryota"
 	#inputTaxon = "Animalia"
 	#start_time = time.time()
 	#print find_genome_ids(inputTaxon)        
 	#print get_genome_species(inputTaxon)
 	#end_time = time.time()
 	
 	#print end_time-start_time

