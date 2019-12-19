import pymongo 
import json
import wget
import requests
import re
import time
import os
import operator

from os.path import dirname, abspath
from sys import argv
from ete3 import Tree
from ete3.parser.newick import NewickError

import species_to_url_service_EOL as EOL_url
import species_to_image_service_EOL as EOL_image

dbName = "EOL_data"
dataCollectionName ="species_info"
counterCollectionName = "speciesCounter"
image_root_loc = ""
#===================================================
#connection to Mongo DB
def connect_mongodb(host='mongodb', port=27017):
 	try:
 		conn=pymongo.MongoClient(host, port)
 		#print "Connected to MongoDB successfully!!!"
 	except pymongo.errors.ConnectionFailure as e:
 		print ("Could not connect to MongoDB: %s" % str(e)) 

 	return conn

#---------------------------------------
def check_collection(conn): 
 	does_col_exist = False	
 	try:	
 		db = conn[dbName]          
 		collections = db.collection_names()     
 		does_col_exist = dataCollectionName in collections 

 		if does_col_exist:                                       
 			collection = db[dataCollectionName]
 			is_col_empty = (collection.count() == 0)
 			return {'message': "Collection %s exists and is-empty=%r"%(dataCollectionName, is_col_empty), 'status_code': 200}
 		else:
 			return {'message': "Collection %s does not exist"%dataCollectionName, 'status_code': 200}

 	except Exception as e:
 		return {'message': "Mongo Error: Accessing database failed", 'status_code': 500} 		

#------------------------------------------------------------
#create list of nonexistent species in mongodb 
def find_nonexistent_species(sp_list, data_collection):
 	nonexistent_species = []
 	for sp in sp_list:	
 		sp_info = find_species_info(sp, data_collection)	
 		if sp_info is None: #does not have any data 		
 			nonexistent_species.append({"species_name": sp, "eol_id": ""}) 
 		else: #have link data, need to get image data or already have image data
 			if (type(sp_info['images']) is dict) and sp_info['eol_id'] != -1: #need to get image data
 			   nonexistent_species.append({"species_name": sp, "eol_id": sp_info['eol_id'], "species_id":sp_info['species_id']})
 	
 	return nonexistent_species

#---------------------------------------------------------------
#insert species info to collection 
def insert_species_info(species_info, data_collection): 	
 	if type(species_info) is dict:
 		result = data_collection.insert_one(species_info)
 		ids = result.inserted_id
 	elif type(species_info) is list: 
 		#print (species_info)	
 		result = data_collection.insert_many(species_info)	
 		ids = result.inserted_ids

 	#return len(ids) #number of items inserted

#----------------------------------------------------------
#update species info in collection
def update_species_info(sp_name, sp_id, sp_image_data, data_collection):
 	data_collection.update({"species_id": sp_id, "species_name": sp_name},{"$set": {"images": sp_image_data}})
 	
#---------------------------------------------------------
#find species info in collection 
def find_species_info(sp_name, data_collection):
 	species_info = data_collection.find_one({"species_name": sp_name})

 	return species_info

#----------------------------------------------------------
#get image and link info of nonexistent species in mongodb
def get_species_info(sp_list, data_collection, counter_collection):
 	sequence = "unique_species_id"	
 	for sp in sp_list:
 		sp_name = sp['species_name']
 		sp_eol_id = sp['eol_id']

 		sp_info = {}
 		sp_info['species_name'] = sp_name
 		if sp_eol_id != "" and sp_eol_id != -1: #eol data id is available in database
 			sp_id = sp['species_id']
 			#get image data using image web service
 			sp_image_data = get_image_data(sp_name, sp_eol_id)
 			if sp_image_data is not None:
 				sp_img_info = create_species_image_info(sp_name, sp_image_data, sp_id)			
 				sp_info['images'] = sp_img_info
 			else:
 				sp_info['images'] = []
 			update_species_info(sp_name, sp_id, sp_info['images'], data_collection)
 		elif sp_eol_id == "": #no eol data in database
 			#get link data using link web service			
 			sp_link_data = get_link_data(sp_name)
 			sp_id = getNextSequence(counter_collection, sequence)
 			sp_info['species_id'] = sp_id
 			if sp_link_data is not None:
 				sp_info['link'] = sp_link_data['eol_link']
 				sp_info['eol_id'] = sp_link_data['eol_id']	
 				sp_image_data = get_image_data(sp_name, sp_info['eol_id'])
 				if sp_image_data is not None:
 					sp_img_info = create_species_image_info(sp_name, sp_image_data, sp_id)			
 					sp_info['images'] = sp_img_info
 				else:
 					sp_info['images'] = []
 			else:
 				sp_info['link'] = ""
 				sp_info['eol_id'] = -1
 				sp_info['images'] = []
 			insert_species_info(sp_info, data_collection)

#-----------------------------------------------------
#create image info of nonexistent species in mongodb
def create_species_image_info(sp_name, sp_image_data, sp_id):
 	image_info_list = []	
 	img_count = 0
 	for sp_image in sp_image_data:
 		thumb_url = sp_image['eolThumbnailURL']
 		img_count += 1
 		img_format = thumb_url[thumb_url.rindex(".")+1:len(thumb_url)]
 		relative_path = "/images/" + re.sub(r"\s+", '_', sp_name) + "_" + str(img_count) + "." + img_format
 		absolute_path = image_root_loc + relative_path
 		if not(download_image(thumb_url, absolute_path)):
 			img_count -= 1
 			continue

 		image_info = {} 
 		image_info['thumb_id'] = img_count
 		image_info['thumb_http_url'] = thumb_url
 		image_info['thumb_local_path'] = relative_path
 		
 		data_ratings = float(sp_image['dataRating'])
 		if (data_ratings > 3.5 and data_ratings <= 4.0): 
 			image_info['thumb_likes'] = 3
 		elif (data_ratings > 3.0 and data_ratings <= 3.5):
 			image_info['thumb_likes'] = 2
 		elif (data_ratings > 2.5 and data_ratings <= 3.0):
 			image_info['thumb_likes'] = 1
 		else:
 			image_info['thumb_likes'] = 0

 		image_info['media_url'] = sp_image['eolMediaURL']
 		image_info['license'] = sp_image['license']
 		image_info['rights_holder'] = sp_image['rightsHolder']
 		image_info['vetted_status'] = sp_image['vettedStatus']
 		image_info['data_rating'] =	sp_image['dataRating']
 		image_info_list.append(image_info)		
            
 	return image_info_list
#-----------------------------------------------------
#update image score of an existent species in mongodb
def update_species_img_score(sp_name, thumb_img_id, data_collection):
 	result = data_collection.update({ "species_name": sp_name, "images.thumb_id": thumb_img_id},{'$inc': {"images.$.thumb_likes": 1} })
 	#result_json = json.loads(result)	
 	#return True if result_json['Modified'] == 1 else False
 	
#---------------------------------------------------------
#create a sequence for the species_id (in 'speciesCounter' collection)
def	createNewSequence(collection, seq_name): 
 	collection.insert({'_id': seq_name, 'seq': 0}) #returns seq_name when inserts successfully

#----------------------------------------------------------
#remove a sequence for the species_id (in 'speciesCounter' collection)
def removeSequence(collection, seq_name):
 	collection.remove({'_id': seq_name}) #returns {u'ok': 1, u'n': 1} when removes successfully 

#-------------------------------------------------------
#reduce a sequence with a value
def reduceSequence(collection, seq_name):
 	return collection.find_and_modify(query= { '_id': seq_name },update= { '$inc': {'seq': -1}}, new=True ).get('seq')

#-----------------------------------------------------------
#get next sequence for the species_id
def getNextSequence(collection, seq_name):   
 	return collection.find_and_modify(query= { '_id': seq_name },update= { '$inc': {'seq': 1}}, new=True ).get('seq')  

#--------------------------------------------------------------
def get_image_data(sp_name=None, sp_eol_id=None):
    img_lst = []
    if sp_eol_id is None:
       service_response = EOL_image.get_images_species([sp_name], True)
       img_lst = service_response['species'][0]['images']
    else:
       num_tries = 0
       while num_tries < 6:
          try:
              service_response = EOL_image.get_image_species_id(int(sp_eol_id))
              if service_response is not None:
                 img_lst = service_response['species']['images']
              else:
                 img_lst = []
              break  
          except KeyError as e:
              print ("Exception getting EOL image data: %s"%str(e))
              num_tries += 1
              pass
    #print (img_lst)
    #print "image data response %s" %service_response
    if len(img_lst) != 0:
       species_img_urls = img_lst
    else:
       species_img_urls = None

    return species_img_urls

#--------------------------------------------------------------
def get_link_data(sp_name):
    service_response = EOL_url.get_eolurls_species([sp_name], True)
    if service_response['species'][0]['matched_name'] == '':
       species_link_info = None
    else:
       species_link_info = {'species_name': sp_name, 'eol_id': service_response['species'][0]['eol_id'], 'eol_link': service_response['species'][0]['species_info_link']}
       
    return species_link_info

#------------------------------------------------
def timeit(f):
    def a_wrapper_accepting_arguments(*args, **kargs):
        t1 = time.time()
        r = f(*args, **kargs)
        print (" %0.3f secs: %s" %(time.time() - t1, f.__name__))
        return r
    return a_wrapper_accepting_arguments

#-----------------------------------------------------
#download the image from http url and save it on local file system
'''
@timeit
def download_image(http_url, local_path):
 	abs_file_path = image_root_loc + local_path
 	#print abs_file_path    
 	if os.path.isfile(abs_file_path):
 		print "%s exists" %abs_file_path
 		return True 
 	try:	
 		response = urllib2.urlopen(http_url)
 		with open(local_path, 'w') as f: 
 			f.write(response.read())
 	except urllib2.HTTPError as e: #http error
 		return False #image download failed
 	except urllib2.URLError as e: #connection error: no route to the specified server
 		return False #image download failed
 	else:
 		return True #image downloaded successfully
'''
@timeit
def download_image(http_url, local_path):
 	abs_file_path = image_root_loc + local_path
 	#print (abs_file_path)    
 	if os.path.isfile(abs_file_path):
 		print ("%s exists" %abs_file_path)
 		return True 
 	try:
 		wget.download(http_url, abs_file_path)
 	except Exception as e:
 		print("Image %s download failed"%http_url)
 		return False #image download failed
 	else:
 		return True #image downloaded successfully

#-----------------------------------------------------
@timeit
def list_info_controller(species_list):
 	conn = connect_mongodb()	
 	db = conn[dbName]
 	counter_collection = db[counterCollectionName]
 	data_collection = db[dataCollectionName]
 	set_image_loc()
 	nonexistent_species = find_nonexistent_species(species_list, data_collection)
 	if len(nonexistent_species) != 0:
 	 	get_species_info(nonexistent_species, data_collection, counter_collection)

 	return True
#--------------------------------------------------------
def set_image_loc():
 	global image_root_loc
 	#get the parent directory of the directory containing the script
 	d = dirname(dirname(abspath(__file__)))
 	image_root_loc = d

#----------------------------------------------------------
def estimate_image_download(newick_str):
 	conn = connect_mongodb()	
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	species_list = get_leaves(newick_str)
 	
 	extra_delay = 5.0
 	avg_download_time = 0.50*5  #5 images by 0.40s/image
 	num_nonexistent_species = 0
 	estimated_download_time = 0.0
	
 	if len(species_list) !=0:
 		nonexistent_species = find_nonexistent_species(species_list, data_collection)
 		num_nonexistent_species = len(nonexistent_species)
 		estimated_download_time = num_nonexistent_species * avg_download_time + extra_delay   
 		print ("estimate completed")      	
 	return {"download_time": estimated_download_time, "number_species": num_nonexistent_species}

#---------------------------------------------------------
def load_all_images(newick_str):
 	load_status = find_image_leaves(newick_str)
 	print ("loading done")
 	return {"download_complete": load_status}

#---------------------------------------------
def images_exists(species):
 	conn = connect_mongodb()	
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	species_info = find_species_info(species, data_collection)
 	if species_info is None: 
 		conn.close()
 		return {"image_info_exists": False, "species": species}
 	else:
 		images_obj = species_info['images']
 		conn.close()
 		#check whether the images obj is list_type or dic_type
 		if type(images_obj) is dict: #need to get image data and update record
 			return {"image_info_exists": False, "species": species}
 		elif type(images_obj) is list:
 			return {"image_info_exists": True, "species": species, "image_info": images_obj}			
   
#---------------------------------------------------
def image_info_controller(species, image_id, next_image):
 	conn = connect_mongodb()	
 	db = conn[dbName]
 	counter_collection = db[counterCollectionName]
 	data_collection = db[dataCollectionName]
 	set_image_loc()
 	nonexistent_species = find_nonexistent_species([species], data_collection)
 	if len(nonexistent_species) != 0:
 		get_species_info(nonexistent_species, data_collection, counter_collection)
 	species_info = find_species_info(species, data_collection)
 	
 	result_info = {} 
 	images_obj = species_info['images']
 	sp_id = species_info['species_id']
 	sp_eol_id = species_info['eol_id']
 	#check whether the images obj is list_type or dic_type
 	if type(images_obj) is dict: #need to get image data and update record
 		sp_image_data = get_image_data(species, sp_eol_id)
 		sp_id = species_info['species_id']
 		if sp_image_data is not None:
 			sp_img_info = create_species_image_info(species, sp_image_data, sp_id)	
 		else:
 			sp_img_info = []
 		update_species_info(species, sp_id, sp_img_info, data_collection)
 		images_obj = sp_img_info

 	if len(images_obj) != 0 and image_id != 0 and not(next_image):		
 		for image in images_obj:
 			if image_id == image['thumb_id']:
 				result_info = image
 	elif len(images_obj) != 0 and image_id !=0 and next_image:
 		next_image = get_next_image(images_obj, image_id)
 		result_info = next_image
 	elif len(images_obj) != 0 and image_id == 0:
 		popular_image = get_popular_image(images_obj) 
 		result_info = popular_image
 	
 	conn.close()
 	return result_info

#------------------------------------------------------
def link_info_controller(species):
 	conn = connect_mongodb()	
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	counter_collection = db[counterCollectionName]
 	sequence = "unique_species_id"

 	species_info = find_species_info(species, data_collection)
 	sp_info = {}	
 	if species_info is None: #info is not in database
 		sp_link_data = get_link_data(species)
 		sp_id = getNextSequence(counter_collection, sequence)
 		if sp_link_data is not None:
 			sp_info['eol_link'] = sp_link_data['eol_link']
 			sp_info['eol_id'] = sp_link_data['eol_id']
 			sp_image = {}			  
 		else:
 			sp_info['eol_link'] = ""
 			sp_info['eol_id'] = -1
 			sp_image = []

 		species_info = {'species_id': sp_id, 'images': sp_image, 'species_name': species, 'link': sp_info['eol_link'], 'eol_id': sp_info['eol_id']}
 		insert_species_info(species_info, data_collection)
 	else: #info is in database
 	 	sp_info['eol_link'] = species_info['link']	
 	
 	sp_info['species'] = species
 	conn.close()

 	return sp_info

#------------------------------------------------------------
def get_popular_image(image_list):
 	images = {}
 	for img in image_list:
 		images[img['thumb_id']] = int(img['thumb_likes'])

 	sorted_images = sorted(images.items(), key=operator.itemgetter(1), reverse=True)
 	popular_img_id = sorted_images[0][0]
 	for img in image_list:
 		if img['thumb_id'] == popular_img_id:
 			return img

#--------------------------------------------------------------
def get_next_image(image_list, image_id):
 	for img_index, img in enumerate(image_list):
 		if (image_id == img['thumb_id']):
 			current_img_index = img_index

 	next_img_index = (current_img_index+1)%(len(image_list))
 	return image_list[next_img_index]

#------------------------------------------------------------
def parse_newick(newick_str):
 	try:
 		print (newick_str)      
 		tree = Tree(newick_str)
 		print (tree)
 	except NewickError:
 		try:
 			tree = Tree(newick_str, format=1)
 		except NewickError as e:
 			return None
 	
 	return tree 

#--------------------------------------------------------------
def get_leaves(newick_str):
 	species_list = []
 	treeobj = parse_newick(newick_str)
 	if treeobj is not None:
 		species_list = [leaf.name for leaf in treeobj.iter_leaves()]
 	
 	return species_list

#-------------------------------------------------------------
def find_image_leaves(newick_str):
 	speciesList = get_leaves(newick_str)
 	if len(speciesList) != 0:
 	 	return list_info_controller(speciesList)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == "__main__":

# 	script, newick_str = argv
# 	find_image_leaves(newick_str)
