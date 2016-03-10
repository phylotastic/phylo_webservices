import pymongo
import datetime 
import json

from bson import json_util
from bson.json_util import dumps

dbName = "SpeciesList"
dataCollectionName ="userSpecieslist"
counterCollectionName = "listCounters"

#connection to Mongo DB
def connect_mongodb(host='localhost', port=27017):
 	try:
 		conn=pymongo.MongoClient(host, port)
 		print "Connected successfully!!!"
 	except pymongo.errors.ConnectionFailure, e:
 		print "Could not connect to MongoDB: %s" % e 

 	return conn

#-------------------------------------
#get lists of a user from the database
def get_user_lists(user_id, conn, include_all):
  	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	document = data_collection.find({"user_id":user_id},{"lists" : 1});	
  	
 	if document.count() == 0:
 		message = "No user found"
  		status_code = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		message = "Success"
 		status_code = 200
 	
 	user_lists_obj = []
 	user_lists = []
 	for ulist in document:
  		lists = ulist['lists'] 				
 		for list_obj in lists:
  			list_json = {}
 			list_short_json = {} 
  			
 			list_json['list_id'] = list_obj['list_id']			
  			list_short_json['list_id'] = list_obj['list_id']
			
 			list_json['list_title'] = list_obj['title']  		 	
 			list_short_json['list_title'] = list_obj['title']
 			
 			list_json['list_description'] = list_obj['description']
 			list_json['list_date_published'] = list_obj['date_published'].strftime("%m-%d-%Y")
 			list_json['list_author'] = list_obj['author']
  			list_json['list_curator'] = list_obj['curator']			
 			list_json['list_curation_date'] = list_obj['curation_date'].strftime("%m-%d-%Y")
 			list_json['list_source'] = list_obj['source']
 			list_json['list_keywords'] = list_obj['keywords']
 			list_json['list_focal_clade'] = list_obj['focal_clade']
 			list_json['list_extra_info'] = list_obj['extra_info']
 			#list_json['is_list_public'] = list_obj['is_public']  # hidden property
 		 	#list_json['list_origin'] = list_obj['origin'] 		# hidden property

 			user_lists_obj.append(list_json)
 			user_lists.append(list_short_json)
 
 	if include_all:
 	 	return json.dumps({"user_id": user_id, 'lists': user_lists_obj, "message": message, "status_code": status_code})
 	else:
 		return json.dumps({"user_id": user_id, 'lists': user_lists, "message": message, "status_code": status_code})

#-----------------------------------------
#get species of a list of a particular user from the database
def get_user_list_species(user_id, list_id, conn, include_all):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]	
 	document = data_collection.find({"user_id":user_id},{"lists" : 1});
 	
 	if document.count() == 0:
 		message = "No user found"
 		status_code = 204  #The server successfully processed the request and is not returning any content
 	else:
 		message = "Success"
  	 	status_code = 200

 	found_list = False	
 	species_list_obj = []
 	species_list = []
 	for ulist in document:
  		lists = ulist['lists'] 				
 		for list_obj in lists:
 			if list_obj['list_id'] == list_id: 			
				found_list = True	 			
 				sp_lst = list_obj['species']
 				for species_obj in sp_lst:
 				 	species_json = {}
	  			 	species_json['vernacular_name'] = species_obj['vernacular_name']
			 		species_json['scientific_name'] = species_obj['scientific_name']  		 	
	 			 	species_json['scientific_name_authorship'] = species_obj['scientific_name_authorship']
 					species_json['family'] = species_obj['family']
 					species_json['order'] = species_obj['order']
 					species_json['phylum'] = species_obj['phylum']
 					species_json['nomenclature_code'] = species_obj['nomenclature_code']
 	 				species_list_obj.append(species_json)
 					#only the scientific names of species 
 					species_list.append(species_obj['scientific_name']) 
 	
 	if found_list == False:
 		message = "Invalid List ID"
 	 	status_code = 404 #The requested resource could not be found but may be available again in the future

 	if include_all:
 		return json.dumps({"user_id": user_id, "list_id": list_id, "species": species_list_obj, "message": message, "status_code": status_code})
 	else:
 		return json.dumps({"user_id": user_id, "list_id": list_id, "species": species_list, "message": message, "status_code": status_code}) 
	
#---------------------------------------------------------------
#insert lists into the database
def insert_user_lists(list_info, conn):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	counter_collection = db[counterCollectionName]
 	
 	#list_info_json = json.loads(list_info)
 	list_info_json = list_info
  	user_id =  list_info_json["user_id"]
 	user_name = list_info_json["user_name"]	
 	
 	sequence = "list_id_" + str(user_id)

 	user_found = False
 	document = data_collection.find({"user_id":user_id})
 	if document.count() == 0:
 		#new user
 		createNewSequence(counter_collection, sequence)
 	else:
 		#exsiting user
 		user_found = True

 	list_id = getNextSequence(counter_collection, sequence)
 	
 	valid_mgdb_list = True
 	status = None
 	try: 	
 	 	list_mgdb_obj = create_list_mgdb_obj(json.dumps(list_info_json['list']), list_id)
 		if user_found:
 	 	 	status = data_collection.update({"user_id":user_id},{"$push":{"lists":list_mgdb_obj}})
 	 	else:	
 	 	 	document = { "user_id": user_id, "user_name": user_name, "lists":[list_mgdb_obj] }
 	 	 	status = data_collection.insert(document)
 	except:
 	 	seq_doc = counter_collection.find({"_id": sequence})
 		valid_mgdb_list = False
 		if seq_doc.count() != 0:
 			removeSequence(counter_collection, sequence)	
 	
 	if not(valid_mgdb_list):
 		return json.dumps({'message': "Error parsing input json", 'status_code': 500})	
 	elif status != None:
 		return json.dumps({'message': "Success", 'status_code': 200})
 	else:
 		return json.dumps({'message': "Error inserting document", 'status_code': 500})
 	
#--------------------------------------
#create list object to store in mongodb 
def create_list_mgdb_obj(list_info, list_id):
 	list_json = json.loads(list_info)
  	
 	date_published_str = list_json['list_date_published']	
 	date_published_obj = datetime.datetime.strptime(date_published_str, "%m-%d-%Y")
  	#date_published_obj = datetime.datetime(2009, 11, 12)
 	curation_date_str = list_json['list_curation_date']	
 	curation_date_obj = datetime.datetime.strptime(curation_date_str, "%m-%d-%Y")
 	#curation_date_obj = datetime.datetime(2010, 11, 12)

 	list_mgdb_obj = {"list_id": list_id,
         "title": list_json['list_title'],
         "description": list_json['list_description'],
         "author": list_json['list_author'],
         "date_published": date_published_obj,
         "curator": list_json['list_curator'],
         "curation_date": curation_date_obj,
         "source": list_json['list_source'],		
         "keywords": list_json['list_keywords'],
         "focal_clade": list_json['list_focal_clade'],
         "extra_info": list_json['list_extra_info'],
         "is_public": list_json['is_list_public'],
         "origin": list_json['list_origin'],
 		 "species": list_json['list_species']
 	}
 	#print list_mgdb_obj
 	return list_mgdb_obj

#----------------------------------------------------
#create a sequence for the list_id (in 'counters' collection)
def	createNewSequence(collection, seq_name): 
 	collection.insert({'_id': seq_name, 'seq': 0}) #returns seq_name when inserts successfully

#remove a sequence for the list_id (in 'counters' collection)
def removeSequence(collection, seq_name):
 	collection.remove({'_id': seq_name}) #returns {u'ok': 1, u'n': 1} when removes successfully 

#------------------------------------------------------
#get next list_id
def getNextSequence(collection, seq_name):   
 	return collection.find_and_modify(query= { '_id': seq_name },update= { '$inc': {'seq': 1}}, new=True ).get('seq');  

#--------------------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == "__main__":
# 	conn = connect_mongodb()
 	
  	
