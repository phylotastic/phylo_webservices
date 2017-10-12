#service description: get species for an input common name using NCBI taxonomy database 
#service version: 0.1
import json
import requests
import time
import datetime 
import urllib
from bs4 import BeautifulSoup

#----------------------------------------------
base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
headers = {'content-type': 'application/json'}

#-----------------------------------------------------
def search_scientific_name(commonName):
	api_url = "https://www.ncbi.nlm.nih.gov/taxonomy/?"

	taxonomy_response = {}    
	taxonomy_response['status_code'] = 200
 	taxonomy_response['message'] = "Success"
	
	payload = {'term': commonName}
	encoded_payload = urllib.urlencode(payload)
	response_html = requests.get(api_url, params=encoded_payload, headers=headers) 
	
	if response_html.status_code == requests.codes.ok:
		#print response_html.text	 	
		soup = BeautifulSoup(response_html.text, "lxml")
		sname, sninfo = extract_scientific_name_info(soup)	
		extra_info = extract_more_info(soup)
		if sname is None:
			taxonomy_response['message'] = "No info found"
		elif extra_info is None:
			taxonomy_response['message'] = "No info found"
		else:
			taxonomy_response['scientific_name'] = sname
			taxonomy_response['ncbi_info_url'] = sninfo
			taxonomy_response['extra_info'] = extra_info
	else:
		taxonomy_response['status_code'] = 500
		taxonomy_response['message'] = "Error: Could not parse html"

	return taxonomy_response

#--------------------------------------------
def extract_scientific_name_info(SoupObj):
	divRprtTag = SoupObj.find_all("div", {"class": "rprt"})
	if len(divRprtTag) == 0:
		return None, None	#no info found	
	else:
		aTags = divRprtTag[0].find_all("a")
		if len(divRprtTag) > 0:
			#extract scientific name
			sc_name = aTags[0].text
			sc_name_link = aTags[0].attrs['href']		
			sc_info_link = "https://www.ncbi.nlm.nih.gov" + sc_name_link
			#print sc_info_link
			return sc_name, sc_info_link
		else:
			return None, None

#----------------------------------------------
def extract_more_info(SoupObj):
	divSuppTag = SoupObj.find_all("div", {"class": "supp"})
	info = {}	
	if len(divSuppTag) == 0:
		info = None	#no info found	
	else:
		info_list = divSuppTag[0].text.split(",")
		#print info_list
		try:
			gen_comm_name_raw = info_list[0]
			gen_comm_name =  gen_comm_name_raw[1:len(gen_comm_name_raw)-1]
			rank = info_list[1]
			blast_name = info_list[2]
			info = {'genbank_common_name': gen_comm_name, 'rank': rank, 'inherited_blast_name': blast_name}
		except IndexError:
			info = None
	
	return info 	

#---------------------------------------------------
def get_scientific_name(inputName):	
 	start_time = time.time()
 	#service_url = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi/genome_species?taxon=" + inputTaxon
 	service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-9"
	final_result = {}
	final_result =search_scientific_name(inputName)
 	
	end_time = time.time()
 	execution_time = end_time-start_time    
    
	#service result creation time
 	creation_time = datetime.datetime.now().isoformat()

	final_result['metadata'] = {'creation_time': creation_time, 'execution_time': "{:4.2f}".format(execution_time), 'source_urls': ["https://www.ncbi.nlm.nih.gov/taxonomy"] }   	 
 	
 	
 	#final_result['service_url'] = service_url
 	#final_result['service_documentation'] = service_documentation	
 	final_result['common_name'] = inputName
	

 	return final_result
#--------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#if __name__ == '__main__':

#	commonName = "cat"
#	commonName = "cow"
#	commonName = "tiger"
#	commonName = "bird" #multiple search results
# 	commonName = "whale"
#	commonName = "bear"
#	commonName = "lion"
#	commonName = "horse"

# 	print get_scientific_name(commonName)
 	
 	
