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

data_rows = [('ph_1', 'Find Scientific Names on Webpages', 'Name Recognition', 'A service to find scientific names on web pages, PDFs, Microsoft Office documents, images.', 'ws_1'),
	('ph_2', 'Find Scientific Names on Text', 'Name Recognition', 'A service to find scientific names on free-form text.', 'ws_2'), 
	('ph_3', 'Resolve Scientific Names with OToL TNRS', 'Name Resolver', 'A service which resolves lists of scientific names against known sources using Open Tree of Life', 'ws_3'),
	('ph_4', 'Resolve Scientific Names with GNR TNRS', 'Name Resolver', 'A service which resolves lists of scientific names against known sources using Global Names Resolver', 'ws_4'),
	('ph_5', 'Get Phylogenetic Trees from OToL', 'Tree Extraction', 'A service to get Phylogenetic Trees from Open Tree of life.', 'ws_5'),
	('ph_6', 'Get All Species from a Taxon', 'Species Retrieval', 'A service to get all Species that belong to a particular Taxon.', 'ws_6'),
	('ph_7', 'Get All Species from a Taxon Filtered by Country', 'Species Retrieval', 'A service to get all Species that belong to a particular Taxon and established in a particular country.', 'ws_7'),
	('ph_8', 'Get Image URLs of a List of Species', 'SpeciesInfo Retrieval', 'A service to get image urls and corresponding license information of a list of species from EOL.', 'ws_8'),	
	('ph_9', 'Get Species (of a Taxon) having genome sequence in NCBI', 'Species Retrieval', 'A service to get subset of Species that belong to a particular Taxon and have genome sequence in NCBI.', 'ws_9'),
	('ph_10', 'Get Information URLs of a List of Species', 'SpeciesInfo Retrieval', 'A service to get information urls of a list of species from EOL.', 'ws_10'),
	('ph_17', 'Find Supported Studies of an Induced Tree', 'TreeMetadata Retrieval', 'A service to get supported studies of an induced tree from Open Tree Of Life.', 'ws_17'),
	('ph_18', 'Get Phylogenetic Trees from Phylomatic', 'Tree Extraction', 'A service to get Phylogenetic Trees from phylomatic.', 'ws_18'),
	('ph_19', 'Get Phylogenetic Trees from PhyloT', 'Tree Extraction', 'A service to get Phylogenetic Trees from the NCBI taxonomy using phyloT', 'ws_19'),
	('ph_20', 'Scale Phylogenetic Trees with Branch Lengths', 'BranchLength Estimation', 'A service to get chronograms (trees with branch lengths proportional to time).', 'ws_20')
]

# Insert web services info
for row in data_rows:
	cursor.execute(add_webservice, row)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()
