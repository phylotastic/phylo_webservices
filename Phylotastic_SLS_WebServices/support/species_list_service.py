import pymongo
import datetime 
import json

import authenticate_user

from bson import json_util
from bson.json_util import dumps

dbName = "SpeciesList"
dataCollectionName ="userSpecieslist"
counterCollectionName = "listCounter"

#connection to Mongo DB
def connect_mongodb(host='localhost', port=27017):
 	try:
 		conn=pymongo.MongoClient(host, port)
 		print "Connected successfully!!!"
 	except pymongo.errors.ConnectionFailure, e:
 		print "Could not connect to MongoDB: %s" % e 

 	return conn

#get all public lists
def get_public_lists(db_collection, verbose, content):
 	documents = db_collection.find({"lists.is_public":{"$eq":True}})
 	
 	if documents.count() == 0:
 		message = "No public lists found"
  		status_code = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		message = "Success"
 		status_code = 200
 	
 	public_lists = []
 	for doc in documents:
  	 	user_lists = doc['lists'] 				
 		for list_obj in user_lists:
 		 	list_json = retrieve_list_mgdb_obj(list_obj, verbose)
 			if content and verbose:
 				list_json['list_species'] = list_obj['species']
 			elif content and not(verbose):
 				list_json['list_species'] = get_species_list(list_obj['species'])
 	 	 	is_public_list = list_obj['is_public']
 			if is_public_list:
 		 	 	public_lists.append(list_json)

 	return json.dumps({'lists': public_lists, "message": message, "status_code": status_code})

#----------------------------------------
#==================NOT USING in the API=====================================
#find lists using keywords
def find_lists(conn, search_query, user_id, include_all):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	
 	#documents = data_collection.find({"$text":{"$search": search_query}})

 	if user_id == -1:	
 		documents = data_collection.find({"$text":{"$search": search_query }, "lists.is_public":{"$eq":True}})
 		find_public = True
 	else:
 		documents = data_collection.find({"$text":{"$search": search_query }, "user_id": {"$eq": user_id}})
 		find_public = False
 	
 	found_lists = []
 	for doc in documents:
 		u_id = doc['user_id']
 		user_lists = doc['lists'] 				
 		for list_obj in user_lists:
 		 	list_json = retrieve_list_mgdb_obj(list_obj, include_all)
 		 	is_public_list = list_obj['is_public']
 		 	
 		 	if find_public:
 				if is_public_list:
 	 	 	 	 	found_lists.append(list_json)
 		 	else:
 				if user_id == u_id:
 	 	 	 	 	found_lists.append(list_json)

 	if len(found_lists) == 0:
 		message = "No lists found"
  		status_code = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		message = "Success"
 		status_code = 200

 	return json.dumps({'lists': found_lists, "message": message, "status_code": status_code})

#=========================================================================
#-----------------------------------------
#get all lists of a user from the database
def get_user_lists(db_collection, user_id, verbose, content):
  	document = db_collection.find({"user_id":user_id},{"lists" : 1});	
  	
 	if document.count() == 0:
 		message = "No user found with ID %s" %(user_id)
  		status_code = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		message = "Success"
 		status_code = 200
 	
 	user_lists = []
 	for ulist in document:
  		lists = ulist['lists'] 				
 		for list_obj in lists:
 			list_json = retrieve_list_mgdb_obj(list_obj, verbose)
 			if content and verbose:
 				list_json['list_species'] = list_obj['species']
 			elif content and not(verbose):
 				list_json['list_species'] = get_species_list(list_obj['species'])
 			user_lists.append(list_json)
 			
 	return json.dumps({"user_id": user_id, 'lists': user_lists, "message": message, "status_code": status_code})
#------------------------------------------------------------
#get an existing list of a particular user (or public list) from the database 
def get_list_by_id(db_collection, user_id, list_id, verbose, content):
 	#query_result = check_existance_user_list(db_collection, "user_id", user_id) 
 	#if query_result['status_code'] == 204:
 		#return json.dumps(query_result)
 		
 	document = db_collection.find({"lists.list_id":list_id})

 	if document.count() == 0:
  		found_list = False		
 		message = "No list found with ID %s" % (list_id)
 		status_code = 204  #The server successfully processed the request and is not returning any content
 	else:
 		found_list = True
 		message = "Success"
  	 	status_code = 200
	
 	for ulist in document:
  		lists = ulist['lists']
 		list_owner = ulist["user_id"] 				
 		for mglist_obj in lists:
 			if list_id == mglist_obj['list_id']:
 				if ( not(mglist_obj['is_public']) and (user_id != list_owner) ):
 					message = "List with ID %s is not public. user_id must be list owner to access the list" %(list_id)
 					status_code = 204
 					return json.dumps({"message": message, "status_code": status_code})

 				list_obj = retrieve_list_mgdb_obj(mglist_obj, verbose)
 				if content and verbose:
 		 	 		list_obj['list_species'] = mglist_obj['species']
 				elif content and not(verbose):
 					list_obj['list_species'] = get_species_list(mglist_obj['species'])

 	if found_list and (user_id != list_owner):	 	 	 		 	
 		return json.dumps({"list": list_obj, "message": message, "status_code": status_code})
 	elif found_list and (user_id == list_owner):
 		return json.dumps({"user_id": user_id,"list": list_obj, "message": message, "status_code": status_code})
 	else:
 		return json.dumps({"message": message, "status_code": status_code})

#-----------------------------------------
def check_existance_user_list(db_collection, query_cond, query_param):
 	query_result = {}
 	if (query_cond == "user_id"):	
 		document = db_collection.find({query_cond: query_param},{"lists" : 1})
 	else:
 		document = db_collection.find({"lists."+query_cond: query_param},{"lists" : 1})

	if document.count() == 0: 		
 		query_result['message'] = "No %s found with ID %s" %(query_cond[0:(query_cond.index("_"))], query_param) 		
 		query_result['status_code'] = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		query_result['message'] = "Success"
 		query_result['status_code'] = 200

 	return query_result
#-----------------------------------------
#get only the scientific names of species from a list
def get_species_list(species_list_obj):
 	species_list = []
 	for species_obj in species_list_obj:
 		#only the scientific names of species 
 		species_list.append(species_obj['scientific_name'])

 	return species_list 
#==================NOT USING in the API=====================================
#get species of a list from the database
def get_list_species(db_collection, list_id, include_all):	
 	document = db_collection.find({"lists.list_id":list_id},{"lists" : 1});
 	
 	if document.count() == 0:
  		found_list = False		
 		message = "No list found with ID %s" % (list_id)
 		status_code = 204  #The server successfully processed the request and is not returning any content
 	else:
 		found_list = True
 		message = "Success"
  	 	status_code = 200

 	species_list_obj = []
 	species_list = []
 	for ulist in document:
  		lists = ulist['lists'] 				
 		for list_obj in lists:
 		 	if list_id == list_obj['list_id']:
 		 	 	sp_lst = list_obj['species']
 		 	 	for species_obj in sp_lst:
 			 	 	species_json = {}
	  			 	species_json['vernacular_name'] = species_obj['vernacular_name']
			 	 	species_json['scientific_name'] = species_obj['scientific_name']  		 	
	 			 	species_json['scientific_name_authorship'] = species_obj['scientific_name_authorship']
 			 	 	species_json['family'] = species_obj['family']
 			 	 	species_json['order'] = species_obj['order']
 			 		species_json['class'] = species_obj['class']
 			 	 	species_json['phylum'] = species_obj['phylum']
 			 	 	species_json['nomenclature_code'] = species_obj['nomenclature_code']
 	 		 	 	species_list_obj.append(species_json)
 				 	#only the scientific names of species 
 				 	species_list.append(species_obj['scientific_name']) 
 		
 	if include_all:
 		#return species_list_obj
 		return json.dumps({"list_id": list_id, "species": species_list_obj, "message": message, "status_code": status_code})
 	else:
 		#return species_list
 		return json.dumps({"list_id": list_id, "species": species_list, "message": message, "status_code": status_code}) 
#===================================================================================
#-----------------------------------------
#controller for get list
def get_list(conn, user_id, list_id, verbose, content, access_token):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	
 	if ((user_id == None) and (list_id == -1) and (access_token == None)):
 		get_list_result = get_public_lists(data_collection, verbose, content)
 	elif ((user_id != None) and (list_id == -1) and (access_token == None)):
 		return json.dumps({'status_code': 400, 'message': "Need to provide a valid access_token to get private lists of user"})
 	elif ((user_id == None) and (list_id == -1) and (access_token != None)):
 		return json.dumps({'status_code': 400, 'message': "Need to provide a valid user_id to get private lists of user"})
 	elif ((user_id != None) and (list_id == -1) and (access_token != None)): # get users private lists
 		token_verification = authenticate_user.verify_access_token(access_token, user_id)
 		if not(token_verification['is_access_token_valid']):
 			return json.dumps({'status_code': 400, 'message': "Error: "+token_verification['message']})
 		get_list_result = get_user_lists(data_collection, user_id, verbose, content)
 	elif ((user_id == None) and (list_id != -1) and (access_token == None)):
 		return json.dumps({'status_code': 400, 'message': "Need to provide valid user_id and access_token to get the list with ID %s"%(list_id)})
 	elif ((user_id != None) and (list_id != -1) and (access_token == None)):
 		return json.dumps({'status_code': 400, 'message': "Need to provide a valid access_token to get the list with ID %s"%(list_id)})
 	elif ((user_id != None) and (list_id != -1) and (access_token != None)):
 		token_verification = authenticate_user.verify_access_token(access_token, user_id)
 		if not(token_verification['is_access_token_valid']):
 			return json.dumps({'status_code': 400, 'message': "Error: "+token_verification['message']})
 		get_list_result = get_list_by_id(data_collection, user_id, list_id, verbose, content)
 	elif ((user_id == None) and (list_id != -1) and (access_token != None)):
 		return json.dumps({'status_code': 400, 'message': "Need to provide valid user_id to get the list with ID %s"%(list_id)})
 	else:
 		return json.dumps({'status_code': 400, 'message': "Bad request with missing parameters"})

 	return get_list_result
#---------------------------------------------------------------
#insert species to an existing list (supports adding multiple species) 
def insert_species_to_list(input_json, conn):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	response = {}
 	try:
 		#input_info_json = json.loads(input_json)
 		input_info_json = input_json
 		user_id =  input_info_json["user_id"]
 		list_id = int(input_info_json["list_id"])	
 		species_info = input_info_json["species"]
 	except KeyError, e:
 		response['message'] = "KeyError-%s"% str(e)
 		response['status_code'] = 500		
 		return  response 
 	except IndexError, e:
 		response['message'] = "IndexError-%s"% str(e)
 		response['status_code'] = 500
 		return response

 	document = data_collection.find({"user_id":user_id},{"lists" : 1});	
  	
 	if document.count() == 0:
 		message = "No user found with ID %s" %(user_id)
  		user_found = False 		
 		status_code = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		message = "Success"
 		user_found = True
 		status_code = 200
 
 	response['user_id'] = user_id
 	response['message'] = message
 	response['status_code'] = status_code

 	if not(user_found):
 		return response	
 	
 	list_found = False
 	
 	for ulist in document:
  		lists = ulist['lists'] 				
 		for list_obj in lists:
  			if list_id == list_obj['list_id']:
 				for species in species_info:
 		 			sp_name = species['scientific_name']
			 		data_collection.update({"user_id": user_id, "lists.list_id": list_id, "lists.$.species.scientific_name": {"$nin": [sp_name]}},{"$push": {"lists.$.species": species}})	
  				list_found = True 				
 				break;
 			
 	if list_found:
 		return response
 	else:
 		response['message'] = "No list found with ID %s" %(list_id)
 		response['status_code'] = 204
 		return response
 	
#--------------------------------------------------------------
#insert a list into the database
def insert_user_list(list_info, conn):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	counter_collection = db[counterCollectionName]

 	response = {}
 	try:
 		#list_info_json = json.loads(list_info)	
 		list_info_json = list_info
 		user_id =  list_info_json["user_id"]	
 	except KeyError, e:
 		response['message'] = "KeyError-%s"% str(e)
 		response['status_code'] = 500
 		return response 
 	except IndexError, e:
 		response['message'] = "IndexError-%s"% str(e)
 		response['status_code'] = 500
 		return response

 	sequence = "unique_list_id"

 	document = data_collection.find({"user_id":user_id})
 	if document.count() == 0:
 		#user does not have any list
 		user_found = False
 	else:
 		#user already has some lists
 		user_found = True

 	list_id = getNextSequence(counter_collection, sequence)
 	
 	insert_status = None
 	 	
 	mgdb_obj = create_list_mgdb_obj(json.dumps(list_info_json['list']), list_id)
 	
 	if not(mgdb_obj['mg_obj_valid']):
 	 	response['message'] = "Error parsing input json: %s" %(mgdb_obj['mg_obj'])
 		response['status_code'] = 500
 	 	reduceSequence(counter_collection, sequence)
 	 	return response	
 	else:
 	 	list_mgdb_obj = mgdb_obj['mg_obj']

 	if user_found:
 	 	insert_status = data_collection.update({"user_id":user_id},{"$push":{"lists":list_mgdb_obj}})
 	else:	
 	 	document = { "user_id": user_id, "lists":[list_mgdb_obj] }
 	 	insert_status = data_collection.insert(document)
 	
 	if insert_status != None:
 		response['message'] = "Success"
 		response['status_code'] = 200
 		response['list_id'] = list_id
 	else:
 		response['message'] = "Error inserting document"
 		response['status_code'] = 500

 	return response
 	
#-----------------------------------------------------
#replace species array of an existing list with new species array
def replace_species_in_list(input_json, conn):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]

 	response = {}
 	try:
 		#input_info_json = json.loads(input_json)	
 		input_info_json = input_json
 		user_id =  input_info_json["user_id"]
 		list_id = int(input_info_json["list_id"])
 		species_info = input_info_json["species"]
 	except KeyError, e:
 		response['message'] = "KeyError-%s"% str(e)
 		response['status_code'] = 500
 		return response 
 	except IndexError, e:
 		response['message'] = "IndexError-%s"% str(e)
 		response['status_code'] = 500
 		return response

 	species_obj_validity = is_species_obj_valid(species_info)
 	if not(species_obj_validity['species_obj_valid']):
 		response['message'] = species_obj_validity['species_obj']
 		response['status_code'] = 500	
 	 	return response

 	document = data_collection.find({"user_id":user_id},{"lists" : 1});	
  	if document.count() == 0:
 		message = "No user found with ID %s" %(user_id)
  		user_found = False 		
 		status_code = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		message = "Success"
 		user_found = True
 		status_code = 200
 
 	response['user_id'] = user_id
 	response['message'] = message
 	response['status_code'] = status_code

 	if not(user_found):
 	 	return response
 	
 	document2 = data_collection.find({"user_id": user_id, "lists.list_id": list_id},{"lists" : 1});
  	if document2.count() == 0:	
 		response['message'] = "No list found with ID %s" %(list_id)
 		response['status_code'] = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		data_collection.update({"user_id": user_id, "lists.list_id": list_id},{"$set": {"lists.$.species": species_info}})
  				
 	return response

#----------------------------------------------------------
#==================NOT USING in the API=====================================
#update list properties (metadata) of an existing list with new metadata
def update_list_metadata(input_json, conn):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]

 	response = {}
 	try:
 		#input_info_json = json.loads(input_json)	
 		input_info_json = input_json
 		user_id =  input_info_json["user_id"]
 		list_id = input_info_json["list_id"]
 		list_info = input_info_json["list"]
 	except KeyError, e:
 		response['message'] = "KeyError-%s"% str(e)
 		response['status_code'] = 500
 		return response 
 	except IndexError, e:
 		response['message'] = "IndexError-%s"% str(e)
 		response['status_code'] = 500
 		return response

 	
 	document = data_collection.find({"user_id":user_id},{"lists" : 1});	
  	if document.count() == 0:
 		message = "No user found with ID %s" %(user_id)
  		user_found = False 		
 		status_code = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		message = "Success"
 		user_found = True
 		status_code = 200
 
 	response['user_id'] = user_id
 	response['message'] = message
 	response['status_code'] = status_code

 	if not(user_found):
 	 	return response
 	
 	date_published_str = list_info['list_date_published']
 	if len(date_published_str) != 0 and not("NA" in date_published_str.upper()):
 		date_validity = is_date_valid(date_published_str)
 		if not(date_validity['date_valid']):
 			response['message'] = "Error: %s does not match format 'mm-dd-yyyy'" %("list_date_published")
 			response['status_code'] = 500
 		else:	 	
 			date_published_obj = datetime.datetime.strptime(date_published_str, "%m-%d-%Y")
 	else:
 		date_published_obj = date_published_str
 	
 	curation_date_str = list_info['list_curation_date']	
 	if len(curation_date_str) != 0 and not("NA" in curation_date_str.upper()):
 		date_validity = is_date_valid(curation_date_str)
 		if not(date_validity['date_valid']):
 			response['message'] = "Error: %s does not match format 'mm-dd-yyyy'" %("list_curation_date")
 			response['status_code'] = 500
 		else:	
 			curation_date_obj = datetime.datetime.strptime(curation_date_str, "%m-%d-%Y")
 	else:
 		curation_date_obj = curation_date_str

 	if response['status_code'] == 500:
 		return response

 	document2 = data_collection.find({"user_id": user_id, "lists.list_id": list_id},{"lists" : 1});
  	if document2.count() == 0:	
 		response['message'] = "No list found with ID %s" %(list_id)
 		response['status_code'] = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		data_collection.update({"user_id": user_id, "lists.list_id": list_id},{"$set": {"lists.$.title": list_info['list_title'], "lists.$.description": list_info['list_description'], "lists.$.author": list_info['list_author'], "lists.$.date_published": date_published_obj, "lists.$.curator": list_info['list_curator'], "lists.$.curation_date": curation_date_obj, "lists.$.source": list_info['list_source'], "lists.$.keywords": list_info['list_keywords'], "lists.$.focal_clade": list_info['list_focal_clade'], "lists.$.extra_info": list_info['list_extra_info'], "lists.$.is_public": list_info['is_list_public'], "lists.$.origin": list_info['list_origin']}})
  				
 	return response

#-------------------------------------------------------
#create list object to store in mongodb 
def create_list_mgdb_obj(list_info, list_id):
 list_json = json.loads(list_info)
 mgdb_obj_validity = {}  	
 mgdb_obj_validity['mg_obj_valid'] = True
 mgdb_obj_validity['mg_obj'] = ''

 species_obj_validity = is_species_obj_valid(list_json['list_species'])
 if not(species_obj_validity['species_obj_valid']):
  	mgdb_obj_validity['mg_obj_valid'] = False
 	mgdb_obj_validity['mg_obj'] = species_obj_validity['species_obj']	
 	return mgdb_obj_validity

 try:	
 	date_published_str = list_json['list_date_published']
 	date_published_obj = date_published_str
 	curation_date_str = list_json['list_curation_date']
 	curation_date_obj = curation_date_str

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
 	mgdb_obj_validity['mg_obj_valid'] = True
 	mgdb_obj_validity['mg_obj'] = list_mgdb_obj
 except KeyError, e:
 	mgdb_obj_validity['mg_obj'] = "KeyError-%s"% str(e)
 	mgdb_obj_validity['mg_obj_valid'] = False

 return mgdb_obj_validity

'''
def create_list_mgdb_obj(list_info, list_id):
 list_json = json.loads(list_info)
 mgdb_obj_validity = {}  	
 mgdb_obj_validity['mg_obj_valid'] = True
 mgdb_obj_validity['mg_obj'] = ''

 species_obj_validity = is_species_obj_valid(list_json['list_species'])
 if not(species_obj_validity['species_obj_valid']):
  	mgdb_obj_validity['mg_obj_valid'] = False
 	mgdb_obj_validity['mg_obj'] = species_obj_validity['species_obj']	
 	return mgdb_obj_validity

 try:	
 	date_published_str = list_json['list_date_published']
 	if len(date_published_str) != 0 and not("NA" in date_published_str.upper()):
 		date_validity = is_date_valid(date_published_str)
 		if not(date_validity['date_valid']):
 			mgdb_obj_validity['mg_obj_valid'] = False
 			mgdb_obj_validity['mg_obj'] = date_validity['message']
 			return mgdb_obj_validity
 	 	date_published_obj = datetime.datetime.strptime(date_published_str, "%m-%d-%Y")
 	else:
 		date_published_obj = date_published_str
 	#date_published_obj = datetime.datetime(2009, 11, 12)
 	curation_date_str = list_json['list_curation_date']	
 	if len(curation_date_str) != 0 and not("NA" in curation_date_str.upper()):
 		date_validity = is_date_valid(curation_date_str)
 		if not(date_validity['date_valid']):
 			mgdb_obj_validity['mg_obj_valid'] = False
 			mgdb_obj_validity['mg_obj'] = date_validity['message']
 			return mgdb_obj_validity	
 		curation_date_obj = datetime.datetime.strptime(curation_date_str, "%m-%d-%Y")
 	else:
 		curation_date_obj = curation_date_str
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
 	mgdb_obj_validity['mg_obj_valid'] = True
 	mgdb_obj_validity['mg_obj'] = list_mgdb_obj
 except KeyError, e:
 	mgdb_obj_validity['mg_obj'] = "KeyError-%s"% str(e)
 	mgdb_obj_validity['mg_obj_valid'] = False

 return mgdb_obj_validity
'''
#-----------------------------------------------
#retrieve list info from mongodb list_obj 
def retrieve_list_mgdb_obj(list_obj, verbose=False):
 	list_json = {}
 	list_short_json = {} 
  			
 	list_json['list_id'] = list_obj['list_id']			
  	list_short_json['list_id'] = list_obj['list_id']
			
 	list_json['list_title'] = list_obj['title']  		 	
 	list_short_json['list_title'] = list_obj['title']
 			
 	list_json['list_description'] = list_obj['description']
 	list_json['list_date_published'] = list_obj['date_published']
 	#check the availability of date_published
 	#date_published_obj = list_obj['date_published']
 	#date_availability = isinstance(date_published_obj, datetime.datetime)
 	#if date_availability:
 	 	#list_json['list_date_published'] = date_published_obj.strftime("%m-%d-%Y")
 	#else:
		#list_json['list_date_published'] = date_published_obj

 	list_json['list_author'] = list_obj['author']
  	list_json['list_curator'] = list_obj['curator']			
	list_json['list_curation_date'] = list_obj['curation_date']
 	#check the availability of curation_date
 	#curation_date_obj = list_obj['curation_date']
 	#date_availability = isinstance(curation_date_obj, datetime.datetime)
 	#if date_availability:
 	# 	list_json['list_curation_date'] = curation_date_obj.strftime("%m-%d-%Y")
 	#else:
    #	list_json['list_curation_date'] = curation_date_obj

 	list_json['list_source'] = list_obj['source']
 	list_json['list_keywords'] = list_obj['keywords']
  	list_json['list_focal_clade'] = list_obj['focal_clade']
 	list_json['list_extra_info'] = list_obj['extra_info']
 	list_json['is_list_public'] = list_obj['is_public']  # hidden property
 	list_json['list_origin'] = list_obj['origin'] 		# hidden property

 	if verbose: 
 		return list_json
 	else:
 		return list_short_json

#-------------------------------------------------------
#remove species from an existing list (supports removing multiple species) 
def remove_species_from_list(input_json, conn):
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	response = {}
 	try:
 		#input_info_json = json.loads(input_json)	
 		input_info_json = input_json
 		user_id =  input_info_json["user_id"]
 		list_id = input_info_json["list_id"]	
 		species_info = input_info_json["species"]
 	except KeyError, e:
 		response['message'] = "KeyError-%s"% str(e)
 		response['status_code'] = 500
 		return response 
 	except IndexError, e:
 		response['message'] = "IndexError-%s"% str(e)
 		response['status_code'] = 500
 		return response 		

 	document = data_collection.find({"user_id":user_id},{"lists" : 1});	
  	if document.count() == 0:
 		message = "No user found with ID %s" %(user_id)
  		user_found = False 		
 		status_code = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		message = "Success"
 		user_found = True
 		status_code = 200
 
 	response['user_id'] = user_id
 	response['message'] = message
 	response['status_code'] = status_code

 	if not(user_found):
 	 	return response	
 	
 	document2 = data_collection.find({"user_id": user_id, "lists.list_id": list_id},{"lists" : 1});
  	if document2.count() == 0:	
 		response['message'] = "No list found with ID %s" %(list_id)
 		response['status_code'] = 204  #The server successfully processed the request and is not returning any content
 	else:
 		for species in species_info:
 		 	#sp_name = species['scientific_name']
 			sp_name = species			
 			data_collection.update({"user_id": user_id, "lists.list_id": list_id},{"$pull": {"lists.$.species": {"scientific_name": sp_name}}})
  				
 	return response
 		
#----------------------------------------------------------
#remove a list of a user from the database
def remove_user_list(user_id, list_id, conn):
  	db = conn[dbName]
 	data_collection = db[dataCollectionName]
 	
 	document = data_collection.find({"user_id":user_id},{"lists" : 1});		
  	if document.count() == 0:
 		message = "No user found with ID %s" %(user_id)
  		user_found = False 		
 		status_code = 204  #The server successfully processed the request and is not returning any content	
 	else:
 		message = "Success"
 		user_found = True
 		status_code = 200
 
 	if not(user_found):
 	 	return json.dumps({"user_id": user_id, "message": message, "status_code": status_code})	

 	document2 = data_collection.find({"user_id": user_id, "lists.list_id": list_id},{"lists" : 1});
  	if document2.count() == 0:	
 	 	message = "No list found with ID %s" %(list_id)
 		status_code = 204  #The server successfully processed the request and is not returning any content	 	
 	else:
 		data_collection.update({"user_id": user_id, "lists.list_id": list_id},{"$pull": {"lists": {"list_id":list_id}}})

 	return json.dumps({"user_id": user_id, "message": message, "status_code": status_code})
 	
#----------------------------------------------------
def is_date_valid(date_str):
 validity_response = {}
 validity_response['date_valid'] = True
 validity_response['message'] = "Success"

 try:	
 	#date_obj = datetime.datetime.strptime(date_str, "%m-%d-%Y")
 	#date_st = date_obj.strftime("%m-%d-%Y")
 	date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
 	date_st = date_obj.strftime("%Y-%m-%d")
 except ValueError, e:
 	validity_response['date_valid'] = False
 	#validity_response['message'] = "%s does not match format 'mm-dd-yyyy' " % date_str
 	validity_response['message'] = "%s does not match format 'yyyy-mm-dd' " % date_str

 return validity_response

#-----------------------------------------------------------
'''
def validate_date(date_text):
    try:
        #print datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d')
        #print date_text
        if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False
'''
#------------------------------------------------------
def is_species_obj_valid(species_obj_list):
 	species_obj_validity = {}
 	species_obj_validity['species_obj'] = ""
 	species_obj_validity['species_obj_valid'] = True	
 	try:
 		for species_json in species_obj_list:
 			vernacular_name = species_json['vernacular_name']
 			scientific_name = species_json['scientific_name']
 			scientific_name_authorship = species_json['scientific_name_authorship']
 	 		family = species_json['family']
 			order =	species_json['order']
 			sp_class =	species_json['class']
 			phylum = species_json['phylum']
 			nomenclature_code = species_json['nomenclature_code']
 	except KeyError, e:
 		species_obj_validity['species_obj'] = "KeyError-%s"% str(e)
 		species_obj_validity['species_obj_valid'] = False 

 	return species_obj_validity	
#----------------------------------------------------
#create a sequence for the list_id (in 'counters' collection)
def	createNewSequence(collection, seq_name): 
 	collection.insert({'_id': seq_name, 'seq': 0}) #returns seq_name when inserts successfully
#---------------------------------
#remove a sequence for the list_id (in 'counters' collection)
def removeSequence(collection, seq_name):
 	collection.remove({'_id': seq_name}) #returns {u'ok': 1, u'n': 1} when removes successfully 
#-------------------------------
#reduce a sequence with a value
def reduceSequence(collection, seq_name):
 	return collection.find_and_modify(query= { '_id': seq_name },update= { '$inc': {'seq': -1}}, new=True ).get('seq')

#------------------------------------------------------
#get next list_id
def getNextSequence(collection, seq_name):   
 	return collection.find_and_modify(query= { '_id': seq_name },update= { '$inc': {'seq': 1}}, new=True ).get('seq')  

#--------------------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == "__main__":
 	#conn = connect_mongodb()
 	#db = conn[dbName]
 	#counter_collection = db[counterCollectionName]
 	#print reduceSequence(counter_collection, 'unique_list_id')
 	#input_json = '{"user_id": 2, "list_id": 22, "species": [{"family": "", "scientific_name": "my species 1", "scientific_name_authorship": "", "vernacular_name": "W", "phylum": "", "nomenclature_code": "I", "order": "new"}, {"family": "", "scientific_name": "my species 2", "scientific_name_authorship": "", "vernacular_name": "D", "phylum": "", "nomenclature_code": "C", "order": ""}]}'
 	#print check_existance_user_list(data_collection, "user_id", "102")
 	#validate_date("2015-1-12")
