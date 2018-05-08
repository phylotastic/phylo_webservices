import os
import re
import requests
import json
import time
import datetime
import importlib

from database import DatabaseAPI 
#------------------------------------------
def request_sender(api_url, method, payload):
	
	start_time = time.time()
	#print "Start time %f: "%start_time
	
	if method == "GET":
		response = requests.get(api_url, params=payload)
	elif method == "POST":
		jsonPayload = json.dumps(payload)
		response = requests.post(api_url, data=jsonPayload, headers={'content-type': 'application/json'})

	resp_time = response.elapsed.total_seconds()
	#print resp_time	
	end_time = time.time()	
	#print "End time %f: "%end_time
	
	if response.status_code == requests.codes.ok:
		if payload is not None:    
			result_json = json.loads(response.text)
		response_time = end_time-start_time
		status = 200
		#print result_json
	else:
		#print "Error in web service (%s) response" %api_url
		response_time = 0.0
		status = 500
    
	print status
	return response_time, status

#-------------------------------------------------    
def compute_resp_time(service_id, service_endpoint, input_settings):
	weighted_resp_time = 0.0

	print "%s, %s"%(service_id, service_endpoint)
	for in_setting in input_settings:
		service_api = service_endpoint+in_setting['path']
		resp_time, status = request_sender(service_api, in_setting['method'], in_setting['input_data'])
		#print resp_time 
		weighted_resp_time = weighted_resp_time + in_setting['weight'] * resp_time
	
	print weighted_resp_time
	record = {}
	record['ws_id'] = service_id
	record['resp_time'] = weighted_resp_time
	
	ts = time.time()
	update_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')	
	record['date'] = update_time

	return record

#------------------------------------------------
def insert_record_db(data_row):
	
	#create a database connection
	db = DatabaseAPI("qos")

	#insert all data rows into database
	db.insert_db_single( "qos_resptime", ["ws_id", "resp_time", "result_updated"], (data_row['ws_id'],data_row['resp_time'], data_row['date']) )

#--------------------------------------------------
def get_configs():
	config_re = re.compile('.py$', re.IGNORECASE)
	config_files = filter(config_re.search, os.listdir(os.path.join(os.path.dirname(__file__), "input_configs")))
	
	input_modules = lambda fp: "." + os.path.splitext(fp)[0]
	module_list = map(input_modules, config_files)	
 
	#print module_list
	return module_list
#-----------------------------------------

if __name__ == "__main__":

	module_list = get_configs()
	importlib.import_module("input_configs")
	for module in module_list:
		if not module.startswith(".__"):  	
			module_instance = importlib.import_module(module, package="input_configs")
			service_endpoint = module_instance.service_endpoint
			input_settings = module_instance.input_settings
			service_id = module_instance.service_id
			#print "Response time of web service %s"%service_id
			data_record = compute_resp_time(service_id, service_endpoint, input_settings)
			#print data_record['resp_time']	
			insert_record_db(data_record)
	
