import dendropy
from sets import Set

#================================
data_folder = "./data/tree_collection/"
results_folder = "./data/results/"

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
 
	print "Creating tree objects from TreeBase trees..."
	tree_objects = create_tree_objects(tree_ids_list, species_list)
	tree_objects = sorted(tree_objects, key=getKey, reverse=True)
	
	for tree_obj in tree_objects:
		num_species_found = len(tree_obj.cspecies)
		common_species = Set(tree_obj.cspecies)	
		tree_size = tree_obj.size
		if num_species_found > min_count and tree_size < max_size:
			print "Tree ID: %s"%tree_obj.id
			print "Tree size: %d"%tree_size
			print "Number of species exists: %d"%num_species_found
			if common_species.issubset(coverage_set):
				continue
			else:
				print coverage_set
				print selected_tree_list
				coverage_set = coverage_set.union(common_species)
				selected_tree_list.append(tree_obj.id)

	print "%d species covered out of total %d input species"%(len(coverage_set), len(species_list))
	print "%d trees selected out of %d trees"%(len(selected_tree_list),len(tree_ids_list))
	print selected_tree_list
	
	return selected_tree_list
	
#--------------------------------------------
def combine_trees(selected_trees, list_id):
	#read the selected trees in nexus format and append to a file in newick format
	for tree_id in selected_trees:
		file_nxs = tree_id + ".nex"
		tree_obj = dendropy.Tree.get(path=data_folder+file_nxs, schema="nexus")
		tree_obj.write(file=open(results_folder+list_id+'_tree.tre', 'a'), schema="newick")

#----------------------------------------------
if __name__ == '__main__':
       
	trees_list = ['Tr62772', 'Tr48657', 'Tr6827', 'Tr107890', 'Tr1784', 'Tr66092', 'Tr4031', 'Tr108069', 'Tr62774', 'Tr101469', 'Tr101487', 'Tr2328', 'Tr48656', 'Tr3552', 'Tr66090', 'Tr48891', 'Tr62759', 'Tr63192', 'Tr62768', 'Tr48658', 'Tr93747', 'Tr107982', 'Tr1222', 'Tr62769', 'Tr78127', 'Tr43787', 'Tr4676', 'Tr1483', 'Tr87201', 'Tr107983', 'Tr609', 'Tr6977', 'Tr105486', 'Tr49971', 'Tr62773', 'Tr5278', 'Tr62766', 'Tr75486', 'Tr108075', 'Tr96000', 'Tr75498', 'Tr62763', 'Tr6596', 'Tr93748', 'Tr6174', 'Tr58985', 'Tr43789', 'Tr66084', 'Tr1481', 'Tr61834', 'Tr66085', 'Tr108037', 'Tr6974', 'Tr3240', 'Tr93749', 'Tr106399', 'Tr62771', 'Tr4677', 'Tr1478', 'Tr3830', 'Tr2051', 'Tr66733', 'Tr3570', 'Tr107984', 'Tr62396', 'Tr108078', 'Tr62477', 'Tr66087', 'Tr62761', 'Tr6976', 'Tr101517', 'Tr3828', 'Tr66083', 'Tr66086', 'Tr3829', 'Tr75487', 'Tr66082', 'Tr62767', 'Tr1485', 'Tr6975', 'Tr74399', 'Tr64557', 'Tr70810', 'Tr99610', 'Tr61835', 'Tr48654', 'Tr75489', 'Tr107980', 'Tr66089', 'Tr2571', 'Tr101822', 'Tr62764', 'Tr1479', 'Tr107981', 'Tr101484', 'Tr1783', 'Tr106987', 'Tr62775', 'Tr62760', 'Tr2801', 'Tr70841', 'Tr61622', 'Tr95999', 'Tr62776', 'Tr78128', 'Tr49193', 'Tr6269', 'Tr66094', 'Tr108073', 'Tr61623', 'Tr1482', 'Tr5279', 'Tr108074', 'Tr101483', 'Tr108077', 'Tr98883', 'Tr101488', 'Tr3093', 'Tr3553', 'Tr4678', 'Tr48655', 'Tr108038', 'Tr3239', 'Tr232', 'Tr75488', 'Tr75403', 'Tr62765', 'Tr51126', 'Tr74400', 'Tr74362', 'Tr1484', 'Tr62762', 'Tr79866', 'Tr101486', 'Tr108076', 'Tr1480', 'Tr76710', 'Tr43788', 'Tr50676', 'Tr75485', 'Tr101485', 'Tr70477', 'Tr62770']
	#species_list = ["Solanum lycopersicum", "Carica papaya", "Prunus persica", "Vitis amurensis", "Musa balbisiana", "Glycine max", "Theobroma cacao", "Oryza sativa"]
	species_list = ["Bos taurus", "Cervidae", "Hippopotamus amphibius", "Sus scrofa", "Tayassuidae", "Camelus", "Orcinus orca"]
	#species_list = ["Panthera pardus", "Taxidea taxus", "Enhydra lutris", "Lutra lutra", "Canis latrans", "Canis lupus", "Mustela altaica", "Mustela eversmanni", "Martes americana", "Ictonyx striatus", "Canis anthus", "Lycalopex vetulus", "Lycalopex culpaeus", "Puma concolor", "Felis catus","Leopardus jacobita"]
	selected_trees = select_trees(trees_list, species_list)
	#combine_trees(selected_trees, "list-3_200_bestcovg")     


