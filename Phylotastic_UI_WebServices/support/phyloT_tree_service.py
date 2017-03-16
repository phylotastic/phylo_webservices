# Ref: http://itol2.embl.de/help/batch_help.shtml

import requests
import urllib
import json
import time
import datetime
import os
import random
import re

from itolapi import Itol
from itolapi import ItolExport

#----------------------------------------
temp_path = "/phyloT_temp/"
temp_file_name = "ids"
temp_file_format = ".txt"
#------------------------------------------

#get ncbi id available for a taxon
def find_taxon_id(taxonName):
 	api_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"	  
 	payload = {
 		'retmax': 1000,
 		'retmode': 'json',
 		'db': 'taxonomy',
 		'term': taxonName,
 		'tool': "phylotastic-services",
 		'email': "tayeen@nmsu.edu"      
    }
 	encoded_payload = urllib.urlencode(payload)
 	response = requests.get(api_url, params=encoded_payload)#, headers={'content-type': 'application/json'}) 
 	
 	ncbi_id_list = []	
 	ncbi_response = {}    
 	ncbi_response['status_code'] = 200
 	ncbi_response['message'] = "Success"
 	
 	if response.status_code == requests.codes.ok:    
 		data_json = json.loads(response.text)
 		numResults = int(data_json['esearchresult']['count']) 
 		if numResults > 0:
 			ncbi_id_list = data_json['esearchresult']['idlist']  
 	else: 
 		ncbi_response['status_code'] = 500
 		ncbi_response['message'] = "Error: Response error from NCBI esearch.fcgi API"

	ncbi_response['taxon_ids'] = ncbi_id_list
 	
 	if numResults == 0:
  	 	ncbi_response['message'] = "No match found for term %s" %(taxonName)
 		ncbi_response['status_code'] = 204
 	
 	return ncbi_response 	

#---------------------------------------------------------
#get a tree using phylomatic
def get_tree_itol(file_id, ncbiIdDict):
 	curr_dir_path = os.path.dirname(os.path.realpath(__file__))	
 	phyloT_temp_path = curr_dir_path + temp_path	

 	#-----Create the Itol class------
 	itol_uploader = Itol.Itol()
 	#-----Add parameters-------
 	# parameter name: "ncbiFile"
	# parameter description: instead of uploading a tree, iTOL can automatically generate one from a file containing a list of NCBI tax IDs. NCBI taxonomy will be pruned based on your IDs and a Newick tree generated. Input file location

 	itol_uploader.add_variable('ncbiFile', os.path.join(phyloT_temp_path, temp_file_name+"_"+file_id+temp_file_format))

 	# parameter name: "ncbiFormat"
 	# parameter description: format of the tree generated using NCBI tax IDs:
 	#			'namesFull': generated tree will contain scientific names and internal nodes will not be collapsed
 	#			'namesCollapsed': scientific names will be used, and internal nodes with only one child removed
 	# 			'idsFull': tree will contain NCBI taxonomy IDs and internal nodes will not be collapsed
 	# 			'idsCollapsed': NCBI taxonomy IDs will be used, and internal nodes with only one child remove

 	itol_uploader.add_variable('ncbiFormat', 'idsFull')

 	# parameter name: "treeName"
 	# parameter description: name of the tree generated using NCBI tax IDs:

 	itol_uploader.add_variable('treeName', 'tree'+file_id)

 	upload_status = itol_uploader.upload()

 	if not upload_status:
 		return {"message": "There was an error:" + itol_uploader.comm.upload_output, "status_code": 500}
 	else:    
 		# Read the iTOL API return statement
 		upload_output = str(itol_uploader.comm.upload_output)
 		if upload_output.find("SUCCESS") == -1: # SUCCESS: 174561252042902514884188540
 			return {"message": "No tree found in phyloT" , "status_code": 204}

 	# Read the tree ID
 	tree_id = str(itol_uploader.comm.tree_id) #Tree ID: 174561252042902514884188540

 	# Export the tree above to newick
 	#print('Exporting tree to newick')
 	itol_exporter = itol_uploader.get_itol_export()

 	export_location = os.path.join(phyloT_temp_path, "output_"+temp_file_name+"_"+file_id+temp_file_format)
 	#print export_location
 	if os.path.exists(export_location):
 		#print "Removing output file"
 		os.remove(export_location)	

 	itol_exporter.set_export_param_value('format', 'newick')
 	itol_exporter.export(export_location)
 	#print('exported tree to ', export_location)
	
 	output_file = open(export_location, "r")
 	newick_str = output_file.read()
 	final_newick_str = process_phyloT_result(newick_str, ncbiIdDict)
 
 	output_file.close()

 	return {"newick": final_newick_str, "message": "Success", "status_code": 200}

#-----------------------------------------------
#create a dictionary of ncbi ids from a taxa list
def get_ncbi_ids(taxaList):
 	ncbi_id_dic = {}
 	for taxon_name in taxaList:
 		taxon_result = find_taxon_id(taxon_name)
 		if taxon_result['status_code'] == 200:
 			ncbi_id_taxon = taxon_result['taxon_ids'][0]
 			ncbi_id_dic[ncbi_id_taxon] = taxon_name

 	return ncbi_id_dic		

#---------------------------------------------
#create a input file with ncbi ids
def create_file_input_ids(ncbiIdDict):
 	file_id = str(random.randint(1, 100))

 	curr_dir_path = os.path.dirname(os.path.realpath(__file__))
 	#print curr_dir_path
 	file_path = curr_dir_path+temp_path+temp_file_name+"_"+file_id+temp_file_format
 	if os.path.exists(file_path):
 		#print "Removing input file" 
 		os.remove(file_path)
 	input_file = open(file_path, "w")

 	counter = 0
 	dictLen = len(ncbiIdDict)
 	for ncbi_id, taxon in ncbiIdDict.items():
 		input_file.write(ncbi_id)
 		counter += 1
 		if counter != dictLen:
 			input_file.write("\n")

 	input_file.close()

 	return file_id

#---------------------------------------------
def process_phyloT_result(newick_str, ncbiDict):
 	for ncbi_id, taxon in ncbiDict.items():	
 		newick_str = newick_str.replace(ncbi_id, taxon)
 	
 	newick_str = newick_str.replace("\n", "")
 	newick_str = re.sub(r'[\:\.0-9]', "", newick_str)
 	newick_str = newick_str.replace(" ", "_")

 	return newick_str

#---------------------------------------------
def service_controller(taxaList, post=False):
 	
 	start_time = time.time()
 	service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-19"	
 	 	
 	NCBI_dict = get_ncbi_ids(taxaList)
 	input_file_id = create_file_input_ids(NCBI_dict)
	get_tree_response = get_tree_itol(input_file_id, NCBI_dict)
 	
 	final_result = {}
 	if get_tree_response['status_code'] == 200:
 		final_result['tree_newick'] = get_tree_response['newick']
	else:
 		final_result['tree_newick'] = ""
 			
 	final_result['status_code'] = get_tree_response['status_code']
 	final_result['message'] = get_tree_response['message']	
 		
 	end_time = time.time()
 	execution_time = end_time-start_time
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	final_result['creation_time'] = creation_time
 	final_result['execution_time'] = "{:4.2f}".format(execution_time)
 	final_result['service_documentation'] = service_documentation
 	final_result['query_taxa'] = taxaList		

 	if post: 	    
 		return final_result
 	else:
 		return json.dumps(final_result) 

#-----------------------------------------------
#if __name__ == '__main__':
 	#To remove the warning: "the InsecurePlatformWarning: A true SSLContext object is not available"
 	#requests.packages.urllib3.disable_warnings()

 	#input_list = ["Panthera uncia", "Panthera onca", "Panthera leo", "Panthera pardus"]
 	#input_list = ["Annona cherimola", "Annona muricata", "Quercus robur", "Shorea parvifolia" ]
 	#input_list = ["Quercus robur", "Quercus petraea", "Castanea sativa", "Salix alba"]
 	#input_list = ["Setophaga striata","Setophaga magnolia", "Setophaga angelae", "Setophaga plumbea", "Setophaga virens"]	
 	#print service_controller(input_list)

