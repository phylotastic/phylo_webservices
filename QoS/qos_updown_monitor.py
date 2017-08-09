#import smtplib
import os
import re
import requests
import time
import datetime
import importlib
from database import DatabaseAPI 

SessionID = 1
QosID = 1

#-------------------------------------------------
def service_dbstate_checker(service_id):
	"""
	Checks the state of the (up/down) service in database
	"""
	#create a database connection
	db = DatabaseAPI("qos")
	#query the table
	result = db.query_db("qos_updown", ["state"], "ws_id = %s and qos_id = %s and session_id = %s", (service_id, QosID, SessionID)) 
	state = result[0][0]  #up(U) or down(D)

	if state == "U":
		return True 
	elif state == "D":
		return False

#--------------------------------------------------
def service_dbtimestamp_adder(service_id, state):
	"""
	Insert timestamp to the database for service state
	"""
	#create a database connection
	db = DatabaseAPI("qos")

	ts = time.time()
	update_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	db.insert_db("qos_updown", ["ws_id", "qos_id", "session_id", "state", "state_updated"], [(service_id, QosID, SessionID, state, update_time)])

#------------------------------------------------------
def service_status_checker(service_id, service_api, service_input):
	"""
	Checks the status (up/down) of a service
	"""

	status = send_request(service_api, service_input['method'], service_input['input_data'])
	#print status
	state = service_dbstate_checker(service_id)
	#print state
	if status == True and state == True:
		print "service was not down. Running"
	elif status == False and state == True:
		print "service was running, now went down"
		#add timestamp to the database
		service_dbtimestamp_adder(service_id, "D")
	elif status == True and state == False:
		print "service was down, now went up"
		#add timestamp to the database
		service_dbtimestamp_adder(service_id, "U")
	elif status == False and state == False:
		print "service was down and still it is down"

	
#--------------------------------------------
def send_request(api_url, method, payload):
	
	if method == "GET":
		response = requests.get(api_url, params=payload)
	elif method == "POST":
		jsonPayload = json.dumps(payload)
		response = requests.post(api_url, data=jsonPayload, headers={'content-type': 'application/json'})

	if response.status_code == requests.codes.ok:    
		return True #service is up
	else:
		return False #service is down

#-------------------------------------------
def get_configs():
	config_re = re.compile('.py$', re.IGNORECASE)
	config_files = filter(config_re.search, os.listdir(os.path.join(os.path.dirname(__file__), "input_configs")))
	
	input_modules = lambda fp: "." + os.path.splitext(fp)[0]
	module_list = map(input_modules, config_files)	
 
	#print module_list
	return module_list
#-----------------------------------------

if __name__ == "__main__":

	#print request_sender()
	#service_dbtimestamp_adder("ws1")
	#service_dbstate_checker("ws1")
	#service_status_checker("ws1", "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/all_species", {'method': "GET",'input_data':{'taxon': "Vulpes"}})	
	
	while (True):	
		module_list = get_configs()
		importlib.import_module("input_configs")
		print "Number of modules: %s" %len(module_list)
		
		for module in module_list:
			if not module.startswith(".__"):  	
				module_instance = importlib.import_module(module, package="input_configs")
				service_id = module_instance.service_id
				service_api = module_instance.service_endpoint
				input_settings = module_instance.input_settings
				service_status_checker(service_id, service_api, input_settings[0])
				print "Status checked for %s"%service_id
		print "Modules imported"
		time.sleep(10)
	
