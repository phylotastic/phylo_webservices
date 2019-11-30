library(ape);
# Fetch command line arguments
myArgs <- commandArgs(trailingOnly = TRUE)
tree_newick = myArgs
tree_phylo <-read.tree(text=tree_newick); 
collapsed_tree <- collapse.singles(tree_phylo); 
collapsed_tree_nwk<-write.tree(collapsed_tree); 
# cat will write the result to the stdout stream
cat(collapsed_tree_nwk);
