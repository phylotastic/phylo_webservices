import pymongo 
import json
import requests
import time
import re
import os
import urllib2

dbName = "EOL_data"
dataCollectionName ="species_info"
counterCollectionName = "speciesCounter"
image_root_loc = "/home/abusaleh/Phylotastic"
#===================================================
def timeit(f):
    def a_wrapper_accepting_arguments(*args, **kargs):
        t1 = time.time()
        r = f(*args, **kargs)
        print " %0.3f secs: %s" %(time.time() - t1, f.__name__)
        return r
    return a_wrapper_accepting_arguments

#---------------------------------
#connection to Mongo DB
def connect_mongodb(host='localhost', port=27017):
 	try:
 		conn=pymongo.MongoClient(host, port)
 		#print "Connected to MongoDB successfully!!!"
 	except pymongo.errors.ConnectionFailure, e:
 		print "Could not connect to MongoDB: %s" % e 

 	return conn

#------------------------------------
#update species info in a document
def update_species_info(sp_name, data_collection):
 	link_info = get_link_data(sp_name)	
	if link_info is None:
		return #no update
	else:
 		data_collection.update({"species_name": sp_name},{"$set": {"link": link_info['eol_link'], "eol_id": link_info['eol_id']}})

#--------------------------------------
#update species image info in collection
def update_species_image_info(sp_name, sp_image_data, data_collection):
 	data_collection.update({"species_name": sp_name},{"$set": {"images": sp_image_data}})

#----------------------------------------
def get_link_data(sp_name):
    eol_service_uri = "https://phylo.cs.nmsu.edu/phylotastic_ws/sl/eol/links"
    eol_service_payload = {'species': [sp_name]}
    
    service_response = execute_webservice(eol_service_uri, json.dumps(eol_service_payload),{'content-type': 'application/json'})
    if service_response['species'][0]['matched_name'] == '':
       species_link_info = None
    else:
       species_link_info = {'species_name': sp_name, 'eol_id': service_response['species'][0]['eol_id'], 'eol_link': service_response['species'][0]['species_info_link']}
       
    return species_link_info

#------------------------------------------
def get_image_data(sp_name):
    image_service_uri = "https://phylo.cs.nmsu.edu/phylotastic_ws/si/eol/images"
    image_service_payload = {'species': [sp_name]}
    service_response = execute_webservice(image_service_uri, json.dumps(image_service_payload), {'content-type': 'application/json'})
    if service_response['species'][0]['matched_name'] == '':
       img_lst = []
    else:
       img_lst = service_response['species'][0]['images']
    
    return img_lst

#-----------------------------------------------------------
def execute_webservice(service_url, service_payload, header=None):
    if header is None:
       response = requests.post(service_url, data=service_payload)
    else:    
       response = requests.post(service_url, data=service_payload, headers=header)

    if response.status_code == requests.codes.ok:        
        res_json = json.loads(response.text)
    else:
        res_json = None

    return res_json 

#----------------------------------------
#create image info of nonexistent species in mongodb
def create_species_image_info(sp_name, sp_image_data):
 	image_info_list = []	
 	img_count = 0
 	for sp_image in sp_image_data:
 		thumb_url = sp_image['eolThumbnailURL']
 		img_count += 1
 		img_format = thumb_url[thumb_url.rindex(".")+1:len(thumb_url)]
 		relative_path = "/images2/" + re.sub(r"\s+", '_', sp_name) + "_" + str(img_count) + "." + img_format
 		absolute_path = image_root_loc + relative_path
 		if not(download_image(thumb_url, absolute_path)):
 			img_count -= 1
 			continue

 		image_info = {} 
 		image_info['thumb_id'] = img_count
 		image_info['thumb_http_url'] = thumb_url
 		image_info['thumb_local_path'] = relative_path.replace("images2", "images")
 		
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

#----------------------------------------
#download the image from http url and save it on local file system
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


#------------------------------------------
@timeit
def update_collection(data_collection):
	documents = data_collection.find()
	sp_count = 0
	total_sp = documents.count()
 	if documents.count() == 0:
  		return 
 	else:
 		for doc in documents:
			sp_name = doc['species_name']
			print sp_name
			update_species_info(sp_name, data_collection)
			sp_count += 1

	print "Total %d records out of %d has been updated"%(sp_count, total_sp)

#-----------------------------------------
@timeit
def update_image_collection(data_collection):
	documents = data_collection.find()
	sp_count = 0
	total_sp = documents.count()
 	if documents.count() == 0:
  		return 
 	else:
 		for doc in documents:
 			sp_count += 1
			sp_name = doc['species_name']
			print sp_name
			img_info = get_image_data(sp_name)
 			new_img_info = create_species_image_info(sp_name, img_info)
 			update_species_image_info(sp_name, new_img_info, data_collection)

			print "Total %d records out of %d has been updated"%(sp_count, total_sp)

#----------------------------------------------------------
if __name__ == "__main__":
	conn = connect_mongodb()	
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
	#update_collection(data_collection)			
	#update_species_info("Zebrasoma flavescens", data_collection)
 	update_image_collection(data_collection)
	#img_info = get_image_data("Zebrasoma flavescens")
	#new_img_info = create_species_image_info("Zebrasoma flavescens", img_info)
	#update_species_image_info("Zebrasoma flavescens", new_img_info, data_collection)


