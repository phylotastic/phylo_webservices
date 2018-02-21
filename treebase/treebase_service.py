import treebase_tree_download
import tree_selection

#-------------------------------------------
def get_treebase_tree(taxa):
	tree_list = treebase_tree_download.get_trees(taxa)
	selected_trees = tree_selection.select_trees(tree_list, taxa)

	return selected_trees    

#-------------------------------------------

	

#----------------------------------------------
if __name__ == "__main__":
	


