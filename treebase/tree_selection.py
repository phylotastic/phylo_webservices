import dendropy
from sets import Set

#================================
data_folder = "./data/tree_collection/"
results_folder = "./data/output/"

#----------------------------------------------
class TBTree(object):
	"""
	Represents a Treebase Tree object with its Identifier, Number of unique taxa present and species list matched with input list 
	"""
	def __init__(self, tree_id, tree_size, tree_common_species):
		self.id = tree_id
		self.size = tree_size
		self.cspecies = tree_common_species

#----------------------------------------------
def create_tree_objects(tree_ids_list, species_list):
	"""
	Create TreeBase tree objects for each input tree  
	"""
	tree_objects = []

	for tree_id in tree_ids_list:
		fname = tree_id+".nex"	
		tree_nxobj = dendropy.Tree.get(file=open(data_folder+fname, "r"), schema="nexus")
		tree_size = count_taxa_tree(tree_nxobj)
		found_list = []
		for species in species_list:	
			node = tree_nxobj.find_node_with_taxon_label(species)
			if node is None:
				continue #taxon not found
			else:
				found_list.append(species)

		if len(found_list) > 0: #removing trees that do not contain any of the input species
			tree_objects.append(TBTree(tree_id, tree_size, found_list))

	return tree_objects

#-------------------------------------------
def getKey(tree_obj): #helper for sorted function
    return len(tree_obj.cspecies)

#------------------------------------------------
def count_taxa_tree(tree_nxobj):
	"""
	Returns the number of taxa (size of tree) in the tree object 
	"""
	node_count = 0 #number of taxa in the tree
	for node in tree_nxobj.preorder_node_iter():
		node_count += 1

	return node_count

#----------------------------------------------
def select_trees(tree_ids_list, species_list):
	selected_tree_list = []
	min_count = 2  #minimum number of species that need to be found in a source tree for selection
	max_size = 500  #maximum number of taxons allowed in a source tree to be selected 
	coverage_set = Set([]) #set of species already covered by current selection of trees
 
	#print "Creating tree objects from TreeBase trees..."
	tree_objects = create_tree_objects(tree_ids_list, species_list)
	tree_objects = sorted(tree_objects, key=getKey, reverse=True)
	
	for tree_obj in tree_objects:
		num_species_found = len(tree_obj.cspecies)
		common_species = Set(tree_obj.cspecies)	
		tree_size = tree_obj.size
		if num_species_found > min_count and tree_size < max_size:
			#print "Tree ID: %s"%tree_obj.id
			#print "Tree size: %d"%tree_size
			#print "Number of species exists: %d"%num_species_found
			if common_species.issubset(coverage_set):
				continue
			else:
				#print coverage_set
				#print selected_tree_list
				coverage_set = coverage_set.union(common_species)
				selected_tree_list.append(tree_obj.id)

	#print "%d species covered out of total %d input species"%(len(coverage_set), len(species_list))
	#print "%d trees selected out of %d trees"%(len(selected_tree_list),len(tree_ids_list))
	#print selected_tree_list
	
	return selected_tree_list
	
#--------------------------------------------
def combine_trees(selected_trees, list_id):
	#read the selected trees in nexus format and append to a file in newick format
	for tree_id in selected_trees:
		file_nxs = tree_id + ".nex"
		tree_obj = dendropy.Tree.get(path=data_folder+file_nxs, schema="nexus")
		tree_obj.write(file=open(results_folder+'tree_'+str(list_id)+'.tre', 'a'), schema="newick")

#------------------------------------------------
