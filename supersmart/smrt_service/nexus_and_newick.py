import os
import time
import re
from Bio import Phylo
from nexus import NexusReader
from os.path import dirname, abspath

#===================================================
def nexus_to_newick_file(input_path, original_file, output_path, converted_file):
	Phylo.convert(input_path + original_file, 'nexus', output_path+converted_file, 'newick')
	
#--------------------------------------------------
def remove_tree_annotations(annotated_newick_tree):
	plain_newick_tree = re.sub(r'\[\\\[&(.*?)\]\]', "", annotated_newick_tree)
	
	return plain_newick_tree

#--------------------------------------------------
def read_newick_tree(input_path, file_name):
	newick_tree = None
	file_path = os.path.join(input_path, file_name)
	with open(file_path, "r") as f:
		text = f.read()
		#print text
		annotated_newick_tree = text.rstrip('\n')
		newick_tree = remove_tree_annotations(annotated_newick_tree)

	return newick_tree

#------------------------------------------------
def read_nexus_tree(input_path, file_name):
	file_path = os.path.join(input_path, file_name)
	n = NexusReader(file_path)	
	#print n.trees.ntrees
	nexus_tree_block = n.trees.block
	#print n.trees.trees[0]
	
	return nexus_tree_block

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':
	#path = os.getcwd() + "/output/"
	#path = dirname(dirname(abspath(__file__))) + "/output/"
	#input_file_name = "1c6a0_11-14-2017_11-21-15_consensus"
	
	#original_file = input_file_name + ".nex"
	#converted_file = "converted_" +input_file_name+ ".nhx"
	#nexus_to_newick_file(path, original_file, path, converted_file)
	#print remove_tree_annotations(path, converted_file)
	#nexus_tree = read_nexus(path, original_file)
	#print nexus_tree
	
