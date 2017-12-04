import time
import datetime
import dendropy
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
#import pandas.rpy.common as com
from rpy2.robjects import pandas2ri

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def scale_tree(tree_newick, method="median"):
	ro.r('library(datelife)')
	#ro.r('estdates <- EstimateDates(input =' + tree_newick + ', output.format = "newick.median", partial = TRUE, usetnrs = FALSE, approximatematch = TRUE, method = "PATHd8")')
	if method == "median":
		ro.r('estdates <- EstimateDates(input =' + tree_newick + ', output.format = "newick.median", partial = TRUE, usetnrs = FALSE, approximatematch = TRUE, method = "PATHd8")')
	elif method == "sdm":
		ro.r('estdates <- EstimateDates(input =' + tree_newick + ', output.format = "newick.sdm", partial = TRUE, usetnrs = FALSE, approximatematch = TRUE, method = "PATHd8")')
		
	scaled_tree = ro.r['estdates']
	
	#pandas2ri.activate()	
	# converting <class 'rpy2.robjects.vectors.StrVector'> to <type 'numpy.ndarray'>	
	objstr = pandas2ri.ri2py(scaled_tree)
	# get the 'numpy.string_' object
	scaled_tree_str = objstr[0]
	
	return scaled_tree_str

#----------------------------------------------
def scale_tree_api(tree_newick, method="median"):
	start_time = time.time()
	#service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-20"
	response = {}
	response['message'] = "Success"
 	response['status_code'] = 200	
	formatted_newick = '\"' + tree_newick + '\"'
	
	newick_validity_status, newick_validity_msg = check_newick_validity(tree_newick)
	if newick_validity_status != 200:
		return {'message': newick_validity_msg, 'status_code': newick_validity_status} 

	try:	
		sc_tree = scale_tree(formatted_newick, method)
		sc_tree = sc_tree.replace("_"," ")
		response['scaled_tree'] = sc_tree	
	except:
		response['message'] = "Error: Failed to scale from datelife R package"
 		response['status_code'] = 500		
	
	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
	meta_data = {'creation_time': creation_time, 'execution_time': float("{:4.2f}".format(execution_time)), 'source_urls':["http://datelife.org/"]}
	response['meta_data'] = meta_data
 	 
	response['input_tree'] = tree_newick
	response['method_used'] = method
 	#response['service_documentation'] = service_documentation
 	
	return response

#-----------------------------------------------
def check_newick_validity(tree_nwk):
	try:
		tree = dendropy.Tree.get(data=tree_nwk, schema="newick")

	except Exception, e:
 		if "Incomplete or improperly-terminated tree statement" in str(e): #invalid: "((A,B),C,D));"  valid: ((A,B),(C,D)); 
 			return 400, "NewickReaderIncompleteTreeStatementError: " + str(e)
 		elif "Unbalanced parentheses at tree statement" in str(e):  #invalid: "((A,B),(C,D);"  valid: ((A,B),(C,D)); 
 			return 400, "NewickReaderMalformedStatementError: "+str(e)
 		elif "Multiple occurrences of the same taxa" in str(e): #invalid: "((A,B),(C,C));"  valid: ((A,B),(C,D));
 			return 400, "NewickReaderDuplicateTaxonError: "+str(e)
 		elif "Unexpected end of stream" in str(e): # invalid: "((A,B),(C,D))"  valid: ((A,B),(C,D));
 			return 400, "UnexpectedEndOfStreamError: "+str(e)
 	 	
	return 200, "Success"

#-----------------------------------------------
def metadata_scaling(tree_newick):
	ro.r('library(datelife)')
	
	ro.r('citations <- EstimateDates(input =' + tree_newick + ', output.format = "citations", partial = TRUE, usetnrs = FALSE, approximatematch = TRUE, method = "PATHd8")')
	
	metadata_scaled_tree = ro.r['citations']
	#pandas2ri.activate()	
	# converting <class 'rpy2.robjects.vectors.StrVector'> to <type 'numpy.ndarray'>	
	objstr = pandas2ri.ri2py(metadata_scaled_tree)
	
	list_papers = []	
	# get the 'numpy.string_' object
	for indx in range(len(objstr)):  
		#scaled_tree_str = objstr[0]
		list_papers.append(objstr[indx])
	
	return list_papers

#----------------------------------------------
def scale_metadata_api(tree_newick):
	start_time = time.time()
	#service_documentation = "https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md#web-service-21"
	response = {}
	response['message'] = "Success"
 	response['status_code'] = 200	
	formatted_newick = '\"' + tree_newick + '\"'
	
	newick_validity_status, newick_validity_msg = check_newick_validity(tree_newick)
	if newick_validity_status != 200:
		return {"message": newick_validity_msg, "status_code": newick_validity_status} 

	try:	
		meta_data = metadata_scaling(formatted_newick)
		response['metadata_tree_scaling'] = meta_data	
	except:
		response['message'] = "Error: Failed to get metadata from datelife R package"
 		response['status_code'] = 500		
	
	end_time = time.time()
 	execution_time = end_time-start_time    
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()

	meta_data = {'creation_time': creation_time, 'execution_time': "{:4.2f}".format(execution_time), 'source_urls':["http://datelife.org/"]}
	response['meta_data'] = meta_data
	response['input_tree'] = tree_newick
 	#response['service_documentation'] = service_documentation
 	
	return response 
 
#-----------------------------------------------

#if __name__ == "__main__":

#	tree_newick = "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);" 
	
#	sc_tree = scale_tree_api(tree_newick)
#	print "Result: %s" %sc_tree




