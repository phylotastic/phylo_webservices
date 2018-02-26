library(ape)
library(phangorn)

#* @get /treebase_status
treebase_status <- function(){
	return("alive")
}

super_tree <- function(tree_path){

	input_tree_path <- paste(tree_path, ".tre", sep="")
	   	
	input_tree <- read.tree(input_tree_path)
	 
	sp_tree <- superTree(input_tree, method="MRP", rooted=TRUE)

	if (length(sp_tree) > 1){
		#print("Applying consensus..")
		output_tree <- consensus(sp_tree)	
	}
	else{
		output_tree <- sp_tree	
	}
	
	write.tree(output_tree, paste(tree_path, "_sp.tre", sep=""))

	return(output_tree)
}


prune_tree <- function(sptree, taxa_list, tree_path){

	all_nodes<-sptree$tip.label

	names_to_keep <- taxa_list

	names_to_remove <- character()
	for (i in 1:length(all_nodes)) { 
		if (!all_nodes[i] %in% names_to_keep) { 
			names_to_remove <- append(names_to_remove, all_nodes[i]) 
		} 
	}

	prunedtree <- drop.tip(sptree, names_to_remove)

	write.tree(prunedtree, paste(tree_path, "_pr.tre", sep=""))

}


#* @post /treebase_tree
treebase_tree <- function(list_id, taxa, file_path="./data/output/"){

	tree_path <- paste(file_path, "tree_", list_id, sep="")

	supertree <- super_tree(tree_path)

	#parsing the taxa string to create a list of taxa
	taxa_list = strsplit(taxa, "|", fixed = TRUE)
  
	prunetree <- prune_tree(supertree, taxa_list[[1]], tree_path)

	return("200") 
}	
