import datetime
import time
import dendropy
from dendropy.calculate import treecompare


def compare_trees(tree1_str, tree2_str):
 	response = {}
 	start_time = time.time()
 	try:	
 		tns = dendropy.TaxonNamespace() 	
 	
 		tree1 = dendropy.Tree.get(data=tree1_str, schema="newick",taxon_namespace=tns)
 		tree2 = dendropy.Tree.get(data=tree2_str, schema="newick",taxon_namespace=tns)

 		tree1.encode_bipartitions()
 		tree2.encode_bipartitions()

 		#-----------------------------------------------------------
 		#This method returns the symmetric distance between two trees. 
 		#The symmetric distance between two trees is the sum of the number of  splits found in one of the trees but not the other. 
 		#It is common to see this statistic called the Robinson-Foulds distance

 		areSame = True if treecompare.symmetric_difference(tree1, tree2) == 0 else False
 		status = 200
 		message = "Success"
 		response['are_same_tree'] = areSame
 
 	except Exception as e:
 		if "Incomplete or improperly-terminated tree statement" in str(e): #invalid: "((A,B),C,D));"  valid: ((A,B),(C,D)); 
 			message = "NewickReaderIncompleteTreeStatementError: " + str(e)
 			status = 400
 		elif "Unbalanced parentheses at tree statement" in str(e):  #invalid: "((A,B),(C,D);"  valid: ((A,B),(C,D)); 
 			message = "NewickReaderMalformedStatementError: "+str(e) 
 			status = 400
 		elif "Multiple occurrences of the same taxa" in str(e): #invalid: "((A,B),(C,C));"  valid: ((A,B),(C,D));
 			message = "NewickReaderDuplicateTaxonError: "+str(e)
 			status = 400
 		elif "Unexpected end of stream" in str(e): # invalid: "((A,B),(C,D))"  valid: ((A,B),(C,D));
 			message = "UnexpectedEndOfStreamError: "+str(e)
 			status = 400
 		else:
 			message = "Error: Failed to compare trees."
 			status = 500
 	 	
 	response['status_code'] = status
 	response['message'] = message

 	end_time = time.time()
 	execution_time = end_time-start_time
    #service result creation time
 	creation_time = datetime.datetime.now().isoformat()
 	meta_data = {'creation_time': creation_time, 'execution_time': float('{:4.2f}'.format(execution_time)), 'source_urls':["http://dendropy.org/library/treecompare.html#module-dendropy.calculate.treecompare"] }

 	response['meta_data'] = meta_data
 	
 	return response

