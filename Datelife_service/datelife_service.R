library("datelife")
library("jsonlite")

#* @serializer unboxedJSON
#* @post /scale
function(tree_newick, method="median"){
    
    if (method == "sdm"){
       out_method = "newick_sdm"
    }
    else{
       out_method = "newick_median"
    }
     
    normal_op <- function(){
           datelife_result_obj <- get_datelife_result(input=tree_newick, partial = TRUE, use_tnrs = FALSE, approximate_match = TRUE, update_cache = FALSE, dating_method = "PATHd8", get_spp_from_taxon = FALSE, verbose = FALSE)
           return ( list(scaled_tree=summarize_datelife_result(datelife_query = NULL, datelife_result= datelife_result_obj, summary_format = out_method, partial = TRUE, update_cache = FALSE, summary_print = c("taxa"), verbose = FALSE), message="Success", status_code=200) ) 
    }

    error_op <- function(err){
           return ( list(scaled_tree=NA, message=paste("Datelife Error: ", err), status_code=500) )
    }
    
 	results <- tryCatch(normal_op(), error=error_op)
    return(results)
    
}


#* @serializer unboxedJSON
#* @post /metadata_scale
function(tree_newick){
     
    normal_op <- function(){
           return ( list(citations=EstimateDates(input=tree_newick, output.format = "citations", partial = TRUE, usetnrs = FALSE, approximatematch = TRUE, method = "PATHd8"), message="Success", status_code=200) ) 
    }

    error_op <- function(err){
           return ( list(citations=NA, message=paste("Datelife Error: ", err), status_code=500) )
    }
    
 	results <- tryCatch(normal_op(), error=error_op)
    return(results)
    
}
