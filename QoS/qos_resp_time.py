#import ws1_config
import os
import re
import requests
import json
import time
import datetime
import importlib

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
		result_json = json.loads(response.text)
		#print result_json
	else:
		print "Error in web service (%s) response" %api_url

	response_time = end_time-start_time
    
	return response_time

#-------------------------------------------------    
def compute_resp_time(service_api, input_settings):
	weighted_resp_time = 0.0

	for in_setting in input_settings:
		resp_time = request_sender(service_api, in_setting['method'], in_setting['input_data'])
		#print resp_time 
		weighted_resp_time = weighted_resp_time + in_setting['weight'] * resp_time
	
	return weighted_resp_time

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
			service_api = module_instance.service_endpoint
			input_settings = module_instance.input_settings

			print compute_resp_time(service_api, input_settings)	
	
	
