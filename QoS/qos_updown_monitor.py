#Monitor and notify the status of phylotastic services 

import os
import re
import requests
import time
import datetime
import importlib
import signal
import sys
import json

from database import DatabaseAPI
from notify import send_notifications 

SessionID = None

#-------------------------------------------------
def service_dbstate_checker(service_id):
	"""
	Checks the state of the (up/down) service in database
	"""
	#create a database connection
	db = DatabaseAPI("qos")
	#query the table
	result = db.query_db("qos_updown", ["state"], "ws_id = %s and session_id = %s ORDER BY state_updated DESC", (service_id, SessionID)) 
	state = result[0][0]  #up(U) or down(D)
	#print "DB state: %s"%state

	if state == "U":
		return True 
	elif state == "D":
		return False

#--------------------------------------------------
def services_init_status(list_services_info):
	"""
	Checks the initial states of the services at the start of monitoring  
	"""
	services_init_status_list = []
	for indx, (service_id, service_api, service_input) in enumerate(list_services_info):
		status = service_status_checker(service_id, service_api, service_input)
		status = "U" if status else "D"
		ts = time.time()
		status_check_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		services_init_status_list.append( (service_id, status, status_check_time) )

	return services_init_status_list

#-------------------------------------------------
def service_init_state_adder(services_init_status_list):
	"""
	Inserts inital states (up/down) of the services in database
	"""
	#prepare the data rows
	data_rows = []
	for indx, (service_id, status, status_check_time) in enumerate(services_init_status_list):
		data_rows.append( (service_id, SessionID, status, status_check_time) )
	#create a database connection
	db = DatabaseAPI("qos")
	#insert all data rows into database
	db.insert_db_multiple("qos_updown", ["ws_id", "session_id", "state", "state_updated"], data_rows) 
	
#--------------------------------------------------
def session_start_marker():
	"""
	Inserts date/time of new monitoring session 
	"""
	#create a database connection
	db = DatabaseAPI("qos")
	global SessionID

	ts = time.time()
	session_start_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
	print "Mark the start timestamp of the monitoring session"
	SessionID = db.insert_db_single("qos_session", ["session_start_time"], (session_start_time,) )
	
#-------------------------------------------------
def session_end_marker():
	"""
	Inserts date/time of ending for current monitoring session 
	"""
	#create a database connection
	db = DatabaseAPI("qos")

	ts = time.time()
	session_end_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
	print "Mark the end timestamp of the monitoring session"
	db.update_db_single("qos_session", ["session_end_time"], (session_end_time,), "session_id = "+str(SessionID) )
	
#-------------------------------------------------
def service_dbtimestamp_adder(service_id, state):
	"""
	Insert timestamp to the database for service state
	"""
	#create a database connection
	db = DatabaseAPI("qos")

	ts = time.time()
	update_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	db.insert_db_single("qos_updown", ["ws_id", "session_id", "state", "state_updated"], (service_id, SessionID, state, update_time) )

	return update_time

#------------------------------------------------------
def service_status_checker(service_id, service_api, service_input, status_only=True):
	"""
	Checks the status (up/down) of a service
	"""
	
	status = send_request(service_api, service_input['method'], service_input['input_data'])
	#print status
	#If True, only checks the status of the service by sending ping request
	if status_only:
		return status

	state = service_dbstate_checker(service_id)
	#print state
	if status == True and state == True:
		print "Service %s is running"%(service_id)
	elif status == False and state == True:
		print "Service %s was running, now went down"%(service_id)
		#print "Adding timestamp to the database"
		status_time = service_dbtimestamp_adder(service_id, "D")
		#notify developer of the state
		notify_service_status(service_id, status_time, "D")
	elif status == True and state == False:
		print "Service %s was down, now went up"%(service_id)
		#print "Adding timestamp to the database"
		status_time = service_dbtimestamp_adder(service_id, "U")
		#notify developer of the state
		notify_service_status(service_id, status_time, "U")
	elif status == False and state == False:
		print "Service %s was down and still it is down"%(service_id)

#-----------------------------------------
def notify_service_status(service_id, status_time, state):
	subject = "Phylotastic service(s) status"

	#create a database connection
	db = DatabaseAPI("qos")
	#query the table to get the service name
	result = db.query_db("qos_wsinfo", ["ws_title"], "ws_map_id = %s", (service_id, )) 
	service_name = result[0][0]
	#print service_name

	if state == "D":
		messg = "Phylotastic service %s was running, now went down at %s"%(service_name, status_time)
	elif state == "U":	
		messg = "Phylotastic service %s was down, now went up at %s"%(service_name, status_time)
	else:
		messg = "Unknown state!!"

	#print messg
	#send email notifications 	
	send_notifications( subject, messg )

#--------------------------------------------
def send_request(api_url, method, payload=None):
	try:	
		if method == "GET" and payload is not None:
			response = requests.get(api_url, params=payload)
		elif method == "GET" and payload is None:
			response = requests.get(api_url)
		elif method == "POST":
			jsonPayload = json.dumps(payload)
			response = requests.post(api_url, data=jsonPayload, headers={'content-type': 'application/json'})
		#print response.status_code
	except requests.exceptions.RequestException:
		return False

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

#-------------------------------------------
#when the monitoring process is killed, mark the timestamp
def signal_term_handler(signal, frame):
	print 'Got SIGTERM. Process shutting down..'
	session_end_marker()
	sys.exit(0)

    
#-----------------------------------------

if __name__ == "__main__":
	list_services_info = []
	signal.signal(signal.SIGTERM, signal_term_handler)
	
	if SessionID is None:
		session_start_marker()
		module_list = get_configs()
		importlib.import_module("input_configs")
		print "Number of modules: %s" %len(module_list)
		
		for module in module_list:
			if not module.startswith(".__"):  	
				module_instance = importlib.import_module(module, package="input_configs")
				service_id = module_instance.service_id
				service_endpoint = module_instance.service_endpoint
				input_settings = module_instance.input_settings
				if service_id == "ws_31": #exception for ETE_Tree_Viewer
					service_endpoint = service_endpoint + "/status"
					input_settings[0]['method'] = "GET"
	
				input_settings[0]['input_data'] = None
				list_services_info.append( (service_id, service_endpoint, input_settings[0]) )
		
		init_status_list = services_init_status(list_services_info)
		service_init_state_adder(init_status_list)
		try:
			while (True):	
				for indx, (service_id, service_api, input_settings) in enumerate(list_services_info):	
					service_status_checker(service_id, service_api, input_settings, False)
					#print "Status checked for %s"%service_id
				print "Waiting for 10 min...."
				time.sleep(600) #wait 600s (10 min) 
		except KeyboardInterrupt:
			print "Keyboard interrupted"			
			session_end_marker()
			sys.exit(0)
