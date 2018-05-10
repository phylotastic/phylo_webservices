from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import credentials #for database credentials

DB_NAME = 'qos'

#----------------------------------------------

cnx = mysql.connector.connect(user=credentials.mysql['user'], password=credentials.mysql['password'] ,database=DB_NAME)
cursor = cnx.cursor()

add_webservice = ("INSERT INTO qos_wsinfo "
               "(ws_id, ws_title, ws_group, ws_description, ws_map_id) "
               "VALUES (%s, %s, %s, %s, %s)")

data_rows = [('ph_1', 'GNRD_wrapper_URL', 'Scientific Name Extraction', 'A service to extract scientific names from URL of a web page using Global Names Recognition and Discovery (GNRD) services', 'ws_1'),
	('ph_2', 'GNRD_wrapper_text', 'Scientific Name Extraction', 'A service to find scientific names on free-form text', 'ws_2'), 
	('ph_3', 'OToL_TNRS_wrapper', 'Taxonomic Name Resolution', 'A service which resolves scientific names using Open Tree of Life Taxonomic name resolution services', 'ws_3'),
	('ph_4', 'GNR_TNRS_wrapper', 'Taxonomic Name Resolution', 'A service which resolves scientific names against known taxonomy sources using Global Names Resolution services', 'ws_4'),
	('ph_5', 'OToL_wrapper_Tree', 'Phylogenetic Tree Retrieval', ' service to get Phylogenetic Trees from a list of taxa using Open Tree of Life induced_subtree method', 'ws_5'),
	('ph_6', 'Taxon_all_species', 'Taxon to Species', 'A service to get all Species that belong to a particular Taxon', 'ws_6'),
	('ph_7', 'Taxon_country_species', 'Taxon to Species', 'A service to get a set of Species that belong to a particular Taxon and established in a particular country using INaturalist services', 'ws_7'),
	('ph_8', 'Image_url_species', 'Image-Information URL Retrieval', 'A service to get image urls and corresponding license information of a list of species from EOL.', 'ws_8'),	
	('ph_9', 'Taxon_genome_species', 'Taxon to Species', 'A service to get a set of Species that belong to a particular Taxon and have genome sequence in NCBI database', 'ws_9'),
	('ph_10', 'Info_url_species', 'Image-Information URL Retrieval', 'A service to get information urls of a list of species using EOL services', 'ws_10'),
	('ph_17', 'OToL_supported_studies', 'Miscellaneous', 'A service to get supported studies of an induced tree from OpenTreeOfLife', 'ws_17'),
	('ph_18', 'Phylomatic_wrapper_Tree', 'Phylogenetic Tree Retrieval', 'A  service to get Phylogenetic Trees from a list of taxa using Phylomatic service', 'ws_18'),
	('ph_19', 'PhyloT_wrapper_Tree', 'Phylogenetic Tree Retrieval', 'A service to get Phylogenetic Trees (based on NCBI taxonomy) from a list of taxa using phyloT', 'ws_19'),
	('ph_20', 'Datelife_scale_tree', 'Tree Scaling', 'A service to get Phylogenetic Trees with branch lengths using Datelife R package', 'ws_20'),
	('ph_21', 'TaxonFinder_wrapper_URL', 'Scientific Name Extraction', 'A service to extract scientific names from URL of a web page using TaxonFinder API', 'ws_21'),
	('ph_22', 'TaxonFinder_wrapper_text', 'Scientific Name Extraction', 'A service to extract scientific names on free-form text using TaxonFinder API', 'ws_22'),
	('ph_23', 'iPlant_TNRS_wrapper', 'Taxonomic Name Resolution', 'A service which resolves scientific names (of plants) using iPlant Collaborative services', 'ws_23'),
	('ph_24', 'NCBI_common_name', 'Common Name to Scientific Name', 'A service to get scientific name of a species from its common name(vernacular name) using NCBI API', 'ws_24'),
	('ph_25', 'ITIS_common_name', 'Common Name to Scientific Name', 'A service to get scientific name of a species from its common name(vernacular name) using ITIS API', 'ws_25'),
	('ph_26', 'TROPICOS_common_name', 'Common Name to Scientific Name', 'A service to get scientific name of a species from its common name(vernacular name) using TROPICOS API', 'ws_26'),
	('ph_27', 'Compare_trees', 'Miscellaneous', 'A service to compare two Phylogenetic Trees symmetrically', 'ws_27'),
	('ph_28', 'EOL_Habitat_Conservation', 'Species data services', 'A service to get habitat and conservation status of a list of species from EOL traitsbank', 'ws_28'),
	('ph_29', 'Treebase_Tree', 'Phylogenetic Tree Retrieval', 'A service to get Phylogenetic Trees from a list of taxa by constructung super-trees using source trees of TreeBase', 'ws_29'),
	('ph_30', 'Species_List', 'Species List Manipulation', 'Services to publish/remove/update/access lists of species owned by a phylotastic web application/services user', 'ws_30'),
	('ph_31', 'ETE_Tree_Viewer', 'Tree Viewer', 'A service to draw image of a Phylogenetic Tree', 'ws_31'),
	('ph_32', 'ECOS_Conservation', 'Species data services', 'A service to get conservation status of a list of species using ECOS services', 'ws_32') 
]

# Insert web services info
for row in data_rows:
	cursor.execute(add_webservice, row)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()
