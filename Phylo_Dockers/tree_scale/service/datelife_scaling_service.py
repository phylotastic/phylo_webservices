import time
import datetime
import rpy2.robjects as ro

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Datelife full script
script_str = '''
library(datelife)
scale_datelife<-function(tree_newick, out_method){ normal_op <- function(){ cleaned_input <-make_datelife_query(input=tree_newick, use_tnrs = FALSE, approximate_match = TRUE,get_spp_from_taxon = FALSE, verbose = FALSE);datelife_result_obj <- get_datelife_result(input=cleaned_input, partial = TRUE, use_tnrs = FALSE, approximate_match = TRUE, update_cache = FALSE, dating_method = "PATHd8", get_spp_from_taxon = FALSE, verbose = FALSE);return (list(scaled_tree=summarize_datelife_result(datelife_query = NULL, datelife_result= datelife_result_obj, summary_format = out_method, partial = TRUE, update_cache = FALSE, summary_print = c("taxa"), verbose = FALSE), message="Success", status_code=200) ) };error_op <- function(err){return ( list(scaled_tree=NA, message=paste("Datelife Error: ", err), status_code=500) )};results <- tryCatch(normal_op(), error=error_op);return(results)};
'''

#--------------------------------------------------
def scale_tree(tree, method):
	if method == "median":
		scale_method = "newick_median"
	else:
		scale_method = "newick_sdm"

	try: 
		ro.r(script_str)
		#r_f = ro.globalenv['scale_datelife']	
		#scaled_result = r_f(tree, scale_method)
		ro.r('scaled_result<-scale_datelife("'+tree+'","'+scale_method+'")')
		status_code = ro.r('scaled_result$status_code')[0]	
		message = ro.r('scaled_result$message')[0]
		scaled_tree = ro.r('scaled_result$scaled_tree')[0]
		if int(status_code) == 200:
			return {'scaled_tree': scaled_tree, 'message': "Success", 'status_code': status_code}
		else:
			raise Exception(message)
	except Exception as e:
		return {'scaled_tree': "", 'message': "R access error: "+str(e), 'status_code': 500}

#--------------------------------------------------
def scale_tree_api(tree_newick, method="median"):
	start_time = time.time()
	response = {}
	response['message'] = "Success"
	response['status_code'] = 200	
	
	sc_tree_response = scale_tree(tree_newick, method)
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


#if __name__ == '__main__':
#	input_tree = "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);"
#	print scale_tree_api(input_tree)
