'''
Supersmart Web Services
@developer: Abu Saleh
'''
import os
import sys
import random
import cherrypy
import time
import datetime
import json
import collections
import types
#import pymongo

from cherrypy import tools
from str2bool import str2bool

from smrt_service import db_task
from smrt_service import sync_smrt
from smrt_service import task_status
from smrt_service import smrt_tree_model
from smrt_service.celery import app as smrt_app
from smrt_service.tasks import get_species_tree


#====================================================================
WebService_Group = "gt"
WS_NAME = "phylotastic_ws"
HOST_NAME = "phylo.cs.nmsu.edu" #"127.0.0.1"
SERVICE_PORT = 5011
ROOT_FOLDER = os.getcwd()

ACCESS_LOG_CHERRYPY_5011 = ROOT_FOLDER + "/log/%s_5011_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5011 = ROOT_FOLDER + "/log/%s_5011_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))

#====================================================================

#When user requests invalid resource URI
def error_page_404(status, message, traceback, version):
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.response.status = status
    return json.dumps({'message': "Error: Could not find the requested resource URI", 'status_code': 404})

#When user makes bad request
def error_page_400(status, message, traceback, version):
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.response.status = status
    return json.dumps({'message': message, 'status_code': 400})

#When internal server error occurs
def error_page_500(status, message, traceback, version):
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.response.status = status
    return json.dumps({'message': message, 'traceback': traceback, 'status_code': 500})

#--------------------------------------------
def return_response_error(error_code, error_message, response_format="JSON"):
    #error_response = {'message': error_message, 'status_code':error_code}
    error_response = {'message': error_message}
    if (response_format == "JSON"):
        cherrypy.response.headers['Content-Type'] = "application/json"
        cherrypy.response.status = error_code
        cherrypy.response.body = error_response
        return error_response
    else:
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.body = error_message
        return json.dumps(error_response)

#------------------------------------------
def return_accepted_response(status_code, response_body, status_url):
    cherrypy.response.headers['Content-Type'] = "application/json"
    cherrypy.response.headers['Location'] = status_url
    cherrypy.response.status = status_code
    cherrypy.response.body = response_body
    return response_body
    
#----------------------------------------
class CustomException(Exception):
    pass
        
#-------------------------------------
class Get_Tree_Supersmart_Service_API(object):
    def index(self):
        return "Get_Tree_Supersmart_Service_API: Get tree using Supersmart"

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tree(self,**request_data):
        try:
            input_json = cherrypy.request.json
            species_list = input_json["species"]
 	    
            if len(species_list) == 0: 
               raise CustomException("'species' parameter must have a valid value")

            if len(species_list) > 30: 
               return return_response_error(403,"Error: Currently more than 30 species is not supported","JSON")
   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

        try:
            sm_tree_task = get_species_tree.apply_async((species_list,))
            sm_tree_task_ID = sm_tree_task.id
            task_creation_time = datetime.datetime.now().isoformat()
            job_location = "/"+"smrt"+"/"+"status"+"?job_id="+str(sm_tree_task_ID)
            task_status_url = "http://"+HOST_NAME+":"+str(SERVICE_PORT)+"/"+str(WS_NAME)+"/"+str(WebService_Group)+job_location
            service_result = {"job_id": sm_tree_task_ID, "status_code": 202, 'job_submission_time': task_creation_time, 'job_status_url':  task_status_url}
            #-------------log request------------------   
            #header = cherrypy.request.headers
            #log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'taxa': taxalist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            #insert_log(log)
            #------------------------------------------
            return return_accepted_response(202, service_result, job_location)

        except Exception, e:
            #raise cherrypy.HTTPError(500, "Error: %s"%(str(e))
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------------------
    @cherrypy.tools.json_out()
    def status(self,**request_data):
        try:
            task_ID = str(request_data['job_id']).strip()
            if len(task_ID) == 0: 
               raise CustomException("'job_id' parameter must have a valid value")
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")    
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

        #try:
        service_result = task_status.get_task_status(task_ID)
        
        if service_result['job_state'] == "SUCCESS":
           tree_id = service_result['tree_id']
           tree_location = "/"+"smrt"+"/"+"trees"+"/"+str(tree_id)
           tree_url = "http://"+HOST_NAME+":"+str(SERVICE_PORT)+"/"+str(WS_NAME)+tree_location  
           service_result['tree_url'] = tree_url
           return return_accepted_response(303, service_result, tree_url)
        else:
           return service_result

        #except Exception, e:
            #raise cherrypy.HTTPError(500, "Error: %s"%(str(e))
        #    return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #----------------------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def get_tree(self,**request_data):
        try:
            input_json = cherrypy.request.json
            species_list = input_json["species"]
 	    
            if len(species_list) == 0: 
               raise CustomException("'species' parameter must have a valid value")

            if len(species_list) > 30: 
               return return_response_error(403,"Error: Currently more than 30 species is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")    
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

        service_result = sync_smrt.get_smrt_tree(species_list)
        
        return service_result
    
    #-----------------------------------------------------------------
    #Public /index
    index.exposed = True
    tree.exposed = True
    status.exposed = True
    get_tree.exposed = True

#===================================================================
class Supersmart_Tree(object):
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, tree_id=None):
        try:
           tree_ids = smrt_tree_model.load_tree_ids() 
           if tree_id is None:
              return return_response_error(400,"Error: Missing tree id in the URL /smrt/trees/<treeid>", "JSON")
           elif tree_id in tree_ids:
              tree_nwk, tree_nxs = smrt_tree_model.get_tree(tree_id)
              input_species = smrt_tree_model.get_tree_input(tree_id)
              treeid, job_id, job_status, cur_step, ex_time = db_task.query_tid_db(tree_id)
              return {'newick_tree': tree_nwk, 'input_species': input_species, 'execution_time': ex_time, 'job_id': job_id, 'tree_id': treeid, 'message': "Success", 'status_code': 200}
           else:
              return return_response_error(404,"Error: No tree with ID %s is available."%tree_id,"JSON")

        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

#-------------------------------------
def CORS():
    #print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#=====================================
if __name__ == '__main__':
	cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
	#Configure Server
	cherrypy.config.update({'server.socket_host': '0.0.0.0', #'127.0.0.1'
                            'server.socket_port': SERVICE_PORT,
                            'log.error_file':ERROR_LOG_CHERRYPY_5011,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5011,
                            'tools.log_tracebacks.on': True
                          })

	conf_cherry = {
             '/':{
                'tools.CORS.on': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'error_page.500': error_page_500, 
                'request.show_tracebacks': True,
                'response.timeout' : 3600
                #'request.show_tracebacks': True,
                
             }
    }
   
    #Starting Server
    
	cherrypy.tree.mount(Get_Tree_Supersmart_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group), "smrt"), conf_cherry)
	cherrypy.tree.mount(Supersmart_Tree(), '/%s/%s/%s'%(str(WS_NAME),"smrt", "trees"), {
        '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    })
	cherrypy.engine.start()
	cherrypy.engine.block()


