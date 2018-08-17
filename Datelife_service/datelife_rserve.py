import pyRserve
import time
import datetime

#Datelife full script
'''
scale_datelife<-function(tree_newick, out_method){ normal_op <- function(){ cleaned_input <-make_datelife_query(input=tree_newick, use_tnrs = FALSE, approximate_match = TRUE,get_spp_from_taxon = FALSE, verbose = FALSE);datelife_result_obj <- get_datelife_result(input=cleaned_input, partial = TRUE, use_tnrs = FALSE, approximate_match = TRUE, update_cache = FALSE, dating_method = "PATHd8", get_spp_from_taxon = FALSE, verbose = FALSE);return (list(scaled_tree=summarize_datelife_result(datelife_query = NULL, datelife_result= datelife_result_obj, summary_format = out_method, partial = TRUE, update_cache = FALSE, summary_print = c("taxa"), verbose = FALSE), message="Success", status_code=200) ) };error_op <- function(err){return ( list(scaled_tree=NA, message=paste("Datelife Error: ", err), status_code=500) )};results <- tryCatch(normal_op(), error=error_op);return(results)};
'''

#--------------------------------------------------
def scale_tree_1(tree, method):
	if method == "median":
		scale_method = "newick_median"
	else:
		scale_method = "newick_sdm"

	conn = pyRserve.connect(host='localhost', port=6311)

	conn.voidEval('library(datelife);scale_datelife<-function(tree_newick, out_method){ normal_op <- function(){datelife_result_obj <- get_datelife_result(input=tree_newick, partial = TRUE, use_tnrs = FALSE, approximate_match = TRUE, update_cache = FALSE, dating_method = "PATHd8", get_spp_from_taxon = FALSE, verbose = FALSE);return (list(scaled_tree=summarize_datelife_result(datelife_query = NULL, datelife_result= datelife_result_obj, summary_format = out_method, partial = TRUE, update_cache = FALSE, summary_print = c("taxa"), verbose = FALSE), message="Success", status_code=200) ) };error_op <- function(err){return ( list(scaled_tree=NA, message=paste("Datelife Error: ", err), status_code=500) )};results <- tryCatch(normal_op(), error=error_op);return(results)};')
	result = conn.r.scale_datelife(tree, scale_method)
	#print type(result)
	if result[2] == 200: 
		return {'scaled_tree': result[0], 'message': "Success", 'status_code': 200}
	else:
		return {'scaled_tree': "", 'message': "Datelife error: "+str(result[1]), 'status_code': 500}

#--------------------------------------------------
def scale_tree_api_1(tree_newick, method="median"):
	start_time = time.time()
	response = {}
	response['message'] = "Success"
 	response['status_code'] = 200	
	
	sc_tree_response = scale_tree_1(tree_newick, method)
	if sc_tree_response['status_code'] == 200: 	
		sc_tree = sc_tree_response['scaled_tree']		
 		if sc_tree != "":
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
 	meta_data = {}
 	meta_data['creation_time'] = creation_time
 	meta_data['execution_time'] = "{:4.2f}".format(execution_time)
 	meta_data['source_urls'] = ["http://datelife.org/"]
	response['meta_data'] = meta_data

	response['input_tree'] = tree_newick
	response['method_used'] = method
 	
	return response



#--------------------------------------------------
def scale_tree_2(tree, method="newick_median"):
	if method == "median":
		scale_method = "newick_median"
	else:
		scale_method = "newick_sdm"
	#******Different server with a different port***** 
	conn = pyRserve.connect(host='localhost', port=6312)
	#---------------------------------------------------
	conn.voidEval('library(datelife);scale_datelife<-function(tree_newick, out_method){ normal_op <- function(){ datelife_result_obj <- get_datelife_result(input=tree_newick, partial = TRUE, use_tnrs = FALSE, approximate_match = TRUE, update_cache = FALSE, dating_method = "PATHd8", get_spp_from_taxon = FALSE, verbose = FALSE);return (list(scaled_tree=summarize_datelife_result(datelife_query = NULL, datelife_result= datelife_result_obj, summary_format = out_method, partial = TRUE, update_cache = FALSE, summary_print = c("taxa"), verbose = FALSE), message="Success", status_code=200) ) };error_op <- function(err){return ( list(scaled_tree=NA, message=paste("Datelife Error: ", err), status_code=500) )};results <- tryCatch(normal_op(), error=error_op);return(results)};')
	result = conn.r.scale_datelife(tree, scale_method)
	#print type(result)
	if result[2] == 200: 
		return {'scaled_tree': result[0], 'message': "Success", 'status_code': 200}
	else:
		return {'scaled_tree': "", 'message': "Datelife error: "+str(result[1]), 'status_code': 500}


#--------------------------------------------------
def scale_tree_api_2(tree_newick, method="median"):
	start_time = time.time()
	response = {}
	response['message'] = "Success"
 	response['status_code'] = 200	
	
	sc_tree_response = scale_tree_2(tree_newick, method)
	if sc_tree_response['status_code'] == 200: 	
		sc_tree = sc_tree_response['scaled_tree']		
 		if sc_tree != "":
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
 	meta_data = {}
 	meta_data['creation_time'] = creation_time
 	meta_data['execution_time'] = "{:4.2f}".format(execution_time)
 	meta_data['source_urls'] = ["http://datelife.org/"]
	response['meta_data'] = meta_data
 	
	response['input_tree'] = tree_newick
	response['method_used'] = method
 	
	return response
