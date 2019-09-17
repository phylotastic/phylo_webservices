import pymongo 
import json
import requests
import time

dbName = "EOL_data"
dataCollectionName ="species_info"
counterCollectionName = "speciesCounter"
image_root_loc = ""
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

#----------------------------------------
def get_link_data(sp_name):
    eol_service_uri = "https://phylo.cs.nmsu.edu/phylotastic_ws/sl/eol/links"
    eol_service_payload = {'species': [sp_name]}
    try:
       service_response = execute_webservice(eol_service_uri, json.dumps(eol_service_payload),{'content-type': 'application/json'})
    except:
       try:
          service_response = execute_webservice(eol_service_uri, json.dumps(eol_service_payload),{'content-type': 'application/json'})
       except:
          return None

    if service_response is None:
       return None 
    if service_response['species'][0]['matched_name'] == '':
       species_link_info = None
    else:
       species_link_info = {'species_name': sp_name, 'eol_id': service_response['species'][0]['eol_id'], 'eol_link': service_response['species'][0]['species_info_link']}
       
    return species_link_info

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
 			sp_count += 1
 			if sp_count < 5940:
 				continue
			sp_name = doc['species_name']
			print sp_name
			update_species_info(sp_name, data_collection)
			
			print "Total %d records out of %d has been updated"%(sp_count, total_sp)

	
#----------------------------------------------------------
if __name__ == "__main__":
	conn = connect_mongodb()	
 	db = conn[dbName]
 	data_collection = db[dataCollectionName]
	update_collection(data_collection)			
	#update_species_info("Zebrasoma flavescens", data_collection)

