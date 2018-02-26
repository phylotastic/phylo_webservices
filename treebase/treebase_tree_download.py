#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Downloads source trees from TreeBase using its search API
#API Source: https://web.archive.org/web/20130521145240/http://sourceforge.net/apps/mediawiki/treebase/index.php?title=API
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import requests
import urllib
import urllib2
import xml.etree.ElementTree as ET
import dendropy
import os

#=========================================
url = "http://purl.org/phylo/treebase/phylows/taxon/find?"
headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'}
data_path = "./data/tree_collection/"

#------------------------------------------
def create_payload(species_list):
	querystr = 'tb.title.taxon='
	num_species = len(species_list)
	query = ""

	#Sample Query: http://purl.org/phylo/treebase/phylows/taxon/find?query=tb.title.taxon=%22Angelica archangelica%22%20and%20tb.title.taxon=%22Anthriscus cerefolium%22%20and%20tb.title.taxon=%22Foeniculum vulgare%22%20and%20tb.title.taxon=%22Apium graveolens%22%20and%20tb.title.taxon=%22Cicuta virosa%22%20and%20tb.title.taxon=%22Coriandrum sativum%22&format=rss1&recordSchema=tree

	for indx, species in enumerate(species_list):
		#need to quote the species name
		dqote = '"'    
		query = query + querystr + dqote + species + dqote
		if indx != (num_species-1):
			query += " and "  

	payload = {
		'query': query, 
		'format': 'rss1',
		'recordSchema':  'tree' 
    }
    
	encoded_payload = urllib.urlencode(payload)
	#print encoded_payload    
	return encoded_payload

#----------------------------------------
# Downloads the source trees and return the tree ids
def get_trees(species_list):
	tree_ids = []

	payload = create_payload(species_list)
	try:
		page = requests.get(url, params=payload, headers=headers)
    	#print page.url
	except requests.exceptions.ConnectionError:
		print "Connection error from Treebase API"
		return tree_ids

	NSMap = {
         'dcterms': 'http://purl.org/rss/1.0/',
         'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
         'dc' :'http://purl.org/dc/elements/1.1/', 
         'ns' : 'http://purl.org/rss/1.0/'
        }

	tree_root = ET.fromstring(page.content)

	if tree_root.find('ns:item', NSMap) is None:
		#print "No Tree found"
		return tree_ids
	else:    
		for child in tree_root.findall('ns:item', NSMap):
			item_link = child.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', NSMap)
			colon_indx = item_link.rfind(":")
			tree_id = item_link[colon_indx+1:]

			if not isFileExist(data_path+tree_id):
				print "Downloading %s"%item_link
				try:
					tree = dendropy.Tree.get(url=item_link+'?format=nexus', schema="nexus")
				except urllib2.URLError:
					print "Error getting tree file"
					continue
				
				tree.write(path=data_path+tree_id+".nex", schema="nexus")
			tree_ids.append(tree_id)			
			
	#print tree_ids
	return tree_ids

#------------------------------------------
#check if nexus file exists
def isFileExist(path):
	if os.path.isfile(path+".nex"):
		#print "Nexus tree file exists"
		return True
	else:
		return False

#-------------------------------------------
#if __name__ == '__main__':
       
	#taxa = ["Solanum lycopersicum", "Carica papaya", "Prunus persica", "Vitis amurensis", "Musa sapientum", "Glycine max", "Theobroma cacao", "Oryza sativa"]
	#taxa = ["Panthera pardus", "Taxidea taxus", "Enhydra lutris", "Lutra lutra", "Canis latrans", "Canis lupus", "Mustela altaica", "Mustela eversmanni", "Martes americana", "Ictonyx striatus", "Canis anthus", "Lycalopex vetulus", "Lycalopex culpaeus", "Puma concolor", "Felis catus","Leopardus jacobita"]

	#treebase_result = get_trees(taxa)    
    #print "Number of trees matched: %d"%len(treebase_result)

