import os
from os.path import dirname, abspath
import nexus_and_newick

#========================================
def get_parent_dir():
	parent_dir = dirname(dirname(abspath(__file__)))

	return parent_dir

#----------------------------------------
def load_tree_ids(file_format=".nhx"):
	root_dir = get_parent_dir()
	tree_ids = []
	for file_name in os.listdir(root_dir+"/output/"):
		if file_name.endswith(file_format):
			tid = file_name[: file_name.rfind("_")]
			tree_ids.append(tid)

	return tree_ids

#------------------------------------------
def get_tree(tree_id):
	root_dir = get_parent_dir()
	newick_tree = nexus_and_newick.read_newick_tree(root_dir+"/output/", tree_id+"_consensus.nhx")
	nexus_tree = nexus_and_newick.read_nexus_tree(root_dir+"/output/", tree_id+"_consensus.nex")
	
	return newick_tree, nexus_tree 

#-----------------------------------------
def get_tree_input(tree_id):
	root_dir = get_parent_dir()
	with open(root_dir+"/input/"+tree_id+"_input.txt") as infile:
		input_list = infile.read().splitlines()	

	return input_list

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == "__main__":
	#tids = load_tree_ids()
	#print tids
	#print get_tree(tids[1])
	#print get_tree_input(tids[1])
