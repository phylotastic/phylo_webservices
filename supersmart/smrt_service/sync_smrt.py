from .celery import app
from .tasks import get_species_tree
import sys
import time
import requests
import json

# Add the smrt_service package folder path to the sys.path list
sys.path.append('/home/abusaleh/supersmart-test/smrt_service/')
import db_task

#============================================================
def get_tree_resource(tree_id):
	tree_url = "http://phylo.cs.nmsu.edu:5011/phylotastic_ws/smrt/trees/"+str(tree_id)
	resp = requests.get(tree_url)

	msg = None
	if resp.status_code == requests.codes.ok:
		resp_json = json.loads(resp.text)
		tree_resource = resp_json['newick_tree']
	else:
		tree_resource = None

	msg = resp_json['message']
	
	return msg, tree_resource

#----------------------------------------------------------
def initiate_async_tree_service(species_list):
	smrt_tree_service_url = 'http://phylo.cs.nmsu.edu:5011/phylotastic_ws/gt/smrt/tree'
	payload = {'species': species_list}
	job_ID = None

	resp = requests.post(smrt_tree_service_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})  
	if resp.status_code == 202:
		resp_json = json.loads(resp.text)
		job_ID = resp_json['job_id']
	
	print job_ID
	return job_ID

#---------------------------------------------------------
def get_tree_status(job_id):
	smrt_tree_status_url = 'http://phylo.cs.nmsu.edu:5011/phylotastic_ws/gt/smrt/status'
	payload = {'job_id': job_id}
	
	response = {}

	while(True):
		resp = requests.get(smrt_tree_status_url, params=payload)  
		if resp.status_code == requests.codes.ok:
			resp_json = json.loads(resp.text)
			if 'job_state' in resp_json and resp_json['job_state'] == "PROGRESS":
				print "sleeping..."
				time.sleep(15)	 
			elif 'job_state' in resp_json and resp_json['job_state'] == "FAILURE":
				response['status_code'] = 500
				response['message'] = resp_json['job_status']
				return response
			elif 'job_state' not in resp_json:
				return resp_json
			
#-------------------------------------------------------------
def get_smrt_tree(species_list):
	
	response = {}

	job_id = initiate_async_tree_service(species_list)
	if job_id is None:
		response['message'] = "Error: job submission failed"
		response['status_code'] = 500
	else:
		response = get_tree_status(job_id)

	return response

#----------------------------------------------------------------

