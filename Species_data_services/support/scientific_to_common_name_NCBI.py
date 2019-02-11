#service description: get common names for input scientific names using NCBI taxonomy database 
#service version: 0.1
import json
import requests
import time
import datetime 
import urllib
from bs4 import BeautifulSoup

#----------------------------------------------
base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

#-----------------------------------------------------
def search_name(scName, best_match):
	api_url = "https://www.ncbi.nlm.nih.gov/taxonomy/?"

	taxonomy_response = {}    
	taxonomy_response['status_code'] = 200
 	taxonomy_response['message'] = "Success"
	
	payload = {'term': scName}
	encoded_payload = urllib.urlencode(payload)
	response_html = requests.get(api_url, params=encoded_payload) 
	
	match_name_info = {'searched_name': scName}
	match_name_list = []

	if response_html.status_code == requests.codes.ok:
		#print response_html.text	 	
		soup = BeautifulSoup(response_html.text, "lxml")
		match_name_list, sc_name, ncbi_id = extract_common_names_info(soup, not best_match) #best match true = don't want multiple results	
	else:
		taxonomy_response['status_code'] = 500
		taxonomy_response['message'] = "Error: Could not parse retrieved data from NCBI"

	match_name_info['common_names'] = match_name_list
	match_name_info['matched_name'] =  sc_name
	match_name_info['identifier'] = ncbi_id

	taxonomy_response['result'] = match_name_info 

	return taxonomy_response

#----------------------------------------------
#get multiple results
def extract_common_names_info(SoupObj, multiple=False):
	divRprtTags = SoupObj.find_all("div", {"class": "rprt"})
	common_names_list = []
	scientific_name = None
	identifier = None

	if len(divRprtTags) == 0:
		return common_names_list	#no info found	
	else:
		for indx, divtag in enumerate(divRprtTags):
			aTags = divtag.find_all("a")
			#extract scientific name
			sc_name = aTags[0].text
			sc_name_link = aTags[0].attrs['href']
			ncbi_id = sc_name_link[sc_name_link.rfind("=")+1:]		
			sc_info_link = "https://www.ncbi.nlm.nih.gov" + sc_name_link
			#print sc_info_link
			if scientific_name is None:
				scientific_name = sc_name
			if identifier is None:
				identifier = int(ncbi_id)
		
			divSuppTag = divtag.find_all("div", {"class": "supp"})

			extra_info = extract_more_info(divSuppTag)
			common_name = extra_info['commonName'] if extra_info is not None else ""
			if common_name != "":
				common_names_list.append(common_name)
			if not multiple:
				break 
	
	return	common_names_list, scientific_name, identifier

#----------------------------------------------
def extract_more_info(divSuppTag):
	#divSuppTag = SoupObj.find_all("div", {"class": "supp"})
	
	info = {}	
	if len(divSuppTag) == 0:
		info = None	#no info found	
	else:
		info_list = divSuppTag[0].text.split(",")
		#print info_list
		try:
			if len(info_list) >= 3:
				gen_comm_name_raw = info_list[0].strip()
				gen_comm_name =  gen_comm_name_raw[1:len(gen_comm_name_raw)-1] #Genbank common name
				rank = info_list[1].strip()
				#blast_name = info_list[2]
			elif len(info_list) >= 2:
				gen_comm_name = "" #None creates a problem, so used empty string
				rank = info_list[0].strip()

			info = {'commonName': gen_comm_name, 'rank': rank}
			#info = {'common_name': gen_comm_name, 'rank': rank, 'inherited_blast_name': blast_name}
		except IndexError:
			info = None
		except Exception as e:
			info = None
	
	return info 	

#---------------------------------------------------
def get_sci_to_comm_names(inputNameList, best_match=True):	
 	start_time = time.time()
 	
	final_result = {'status_code': 200, 'message': "Success" }

	results = []
	for inputName in inputNameList:
		match_result = search_name(inputName, best_match)
		if match_result['status_code'] == 200:
			results.append(match_result['result'])

	final_result['result'] = results

	end_time = time.time()
 	execution_time = end_time-start_time    
    
	#service result creation time
 	creation_time = datetime.datetime.now().isoformat()

	final_result['metadata'] = {'creation_time': creation_time, 'execution_time': "{:4.2f}".format(execution_time), 'source_urls': ["https://www.ncbi.nlm.nih.gov/taxonomy"] }   	 
 	
 	return final_result
#--------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':

	#inputSpecies = ["Rangifer tarandus", "Cervus elaphus", "Bos taurus", "Ovis orientalis", "Suricata suricatta", "Cistophora cristata", "Mephitis mephitis"]
	inputSpecies = ["Trichostema arizonicum", "Coccoloba uvifera", "Cypripedium montanum"]

	#commonNameList = ["cattle", "cat", "goat", "pig", "sheep", "duck", "chicken", "horse", "domestic dog"]
	
	#multiple results ["frog", "black bear"]
	
	#commonNameList = ["lion", "tiger", "reindeer", "brown bear", "gray wolf", "red fox", "american crocodile", "black rhinoceros"]  
	
	#commonNameList = ["blue whale", "swordfish", "killer whale"]

	#commonNameList = ["american crow", "rock dove", "american robin", "barn owl", "bald eagle"]

	#commonNameList = ["Christmas fern", "cutleaf coneflower", "Castor bean", "Indian sandalwood", "African marigold"]
	#commonNameList = ["cucumber","tomato","lettuce","pea"]
	
	print get_sci_to_comm_names(inputSpecies)
 	
 	