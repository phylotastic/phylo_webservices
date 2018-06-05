import time
import datetime
import json
import requests

def scale_tree(tree_newick, method="median"):
	api_url = "http://localhost:4646/scale"

	payload = {
        'tree_newick': tree_newick,
        'method': method
    }
    
	#response = requests.get(api_url, params=payload)      
	response = requests.post(api_url, data=payload)     
	if response.status_code == requests.codes.ok:    
		return response.text
	else:
		return json.dumps({"status_code": 500, "message": "Datelife R API error"})
	

#-----------------------------------------------
def metadata_scaling(tree_newick):
	api_url = "http://localhost:4646/metadata_scale"

	payload = {
        'tree_newick': tree_newick
    }
    
	response = requests.post(api_url, data=payload)     
	if response.status_code == requests.codes.ok:    
		return response.text
	else:
		return json.dumps({"status_code": 500, "message": "Datelife R API error"})
	

#----------------------------------------------
def scale_tree_api(tree_newick, method="median"):
	start_time = time.time()
	response = {}
	response['message'] = "Success"
 	response['status_code'] = 200	
	
	sc_tree_response = json.loads(scale_tree(tree_newick, method))
	if sc_tree_response['status_code'] == 200: 	
		sc_tree = sc_tree_response['scaled_tree']		
 		if sc_tree is not None:
			sc_tree = sc_tree.replace("_"," ")
		response['scaled_tree'] = sc_tree	
	else:
		response['scaled_tree'] = ""
		response['message'] = sc_tree_response["message"]
		response['status_code'] = sc_tree_response["status_code"] 	

	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
	response['creation_time'] = creation_time
 	response['execution_time'] = "{:4.2f}".format(execution_time)
	response['input_tree'] = tree_newick
	response['method_used'] = method
 	
	return response

#-----------------------------------------------
def scale_metadata_api(tree_newick):
	start_time = time.time()
	#service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-21"
	response = {}
	response['message'] = "Success"
	response['status_code'] = 200	
	
	meta_data_response = json.loads(metadata_scaling(tree_newick))	
	if meta_data_response['status_code'] == 200: 	
		response['metadata_tree_scaling'] = meta_data_response['citations']	
	else:
		response['message'] = meta_data_response["message"]
		response['status_code'] = meta_data_response["status_code"] 	
	
	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
	response['creation_time'] = creation_time
 	response['execution_time'] = "{:4.2f}".format(execution_time)
	response['input_tree'] = tree_newick
 	 	
	return response 
#-----------------------------------------------

if __name__ == "__main__":

	tree_newick = "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);" 
	#tree_newick = "((((Homo sapiens,Macaca mulatta)Catarrhini,((Melursus ursinus,Canis lupus_pallipes)Caniformia,((Panthera pardus,Panthera tigris)Panthera,Herpestes fuscus))Carnivora)Boreoeutheria,Elephas maximus)Eutheria,Haliastur indus)Amniota;"
	#tree_newick = "(Aulacopone_relicta,(((Myrmecia_gulosa,(Aneuretus_simoni,Dolichoderus_mariae)),((Ectatomma_ruidum,Huberia_brounii),Formica_rufa)),Apomyrma_stygia),Martialis_heureka)Formicidae;"

	'''newick.median
((((Homo sapiens:29.126382,Macaca mulatta:29.126382):69.773618,(((Panthera pardus:6.4,Panthera tigris:6.4):34.300001,Herpestes fuscus:40.700001):24.199999,(Canis lupus pallipes:16.775,Melursus ursinus:16.775):48.125):34):10.65,Elephas maximus:109.55):17.078571,Haliastur indus:126.628571);', 'input_tree': '((((Homo sapiens,Macaca mulatta)Catarrhini,((Melursus ursinus,Canis lupus_pallipes)Caniformia,((Panthera pardus,Panthera tigris)Panthera,Herpestes fuscus))Carnivora)Boreoeutheria,Elephas maximus)Eutheria,Haliastur indus)Amniota;
	'''
	#print scale_metadata_api(tree_newick)
	sc_tree = scale_tree_api(tree_newick, "median")
	print sc_tree	
	


