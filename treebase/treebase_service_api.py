'''
Phylotastic web services
@author: Abu Saleh
'''

import cherrypy
import time
import datetime
import json
import os
import sys
import collections
import pymongo
import datetime 
import types

from cherrypy import tools
from str2bool import str2bool

import treebase_service

from __builtin__ import True

#==============================================================
logDbName = "WSLog"
logCollectionName = "log"
conn = None

WebService_Group1 = "gt"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5012"
#PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY_5012 = ROOT_FOLDER + "/log/%s_5012_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5012 = ROOT_FOLDER + "/log/%s_5012_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))

#------------------------------------------
#When user requests invalid resource URI
def error_page_404(status, message, traceback, version):
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.response.status = status
    return json.dumps({'message': "Error: Could not find the requested resource URI"})

#When user makes bad request
def error_page_400(status, message, traceback, version):
    cherrypy.response.headers['Content-Type'] = 'application/json'
    cherrypy.response.status = status
    return json.dumps({'message': message})

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


#-------------------------------------------
class CustomException(Exception):
    pass
#--------------------------------------------
def connect_mongodb(host='localhost', port=27017):
 	try:
 		conn=pymongo.MongoClient(host, port)
 		print "Connected to MongoDB successfully!!!"
 	except pymongo.errors.ConnectionFailure, e:
 		print "Could not connect to MongoDB: %s" % e 

 	return conn
#--------------------------------------------
def insert_log(log_msg):
    db = conn[logDbName]
    log_collection = db[logCollectionName]
 	
 	#document = { "client_ip": log_msg['remote_ip'], "date": datetime.datetime.now(), "request": log_msg['path'], "method":  }
    insert_status = log_collection.insert(log_msg)

#===============================Get_Tree_TreeBase_Service==========================
class Get_Tree_TreeBase_Service_API(object):
    def index(self):
        return "Get_Tree_TreeBase_Service API: Get tree from TreeBASE"
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            taxalist = input_json["taxa"]

            if type(taxalist) != types.ListType:
               return return_response_error(400,"Error: 'taxa' parameter must be of list type","JSON")
  	        
            if len(taxalist) == 0: 
               raise CustomException("'taxa' parameter must have a valid value")

            if len(taxalist) > 30: 
               return return_response_error(403,"Error: Currently more than 30 names is not supported","JSON")
   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = treebase_service.get_tree(taxalist)   
            #-------------log request------------------   
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'taxa': taxalist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            #insert_log(log)
            #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====TreebaseTreeError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

#--------------------------------------------------------------------
    #Public /index
    index.exposed = True
    tree.exposed = True


#=========================Prune_SuperTree_Phylomatic_Service---INACTIVE=============================
class Prune_Tree_Phylomatic_Service_API(object):
    def index(self):
        return "Prune_Tree_Phylomatic_Service_API : Get pruned megatree using taxa from phylomatic";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def prune(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            supertree = input_json["supertree"]
            taxa = input_json["taxa"]
 		
            if type(taxa) != types.ListType:
               return return_response_error(400,"Error: 'taxa' parameter must be of list type","JSON")
  	        
            if len(taxa) == 0: 
               raise CustomException("'taxa' parameter must have a valid value")

            if len(taxa) > 1000: 
               return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")
   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = megatree_prune_phylomatic.phylomatic_tree_controller(supertree, taxa)   
            #-------------log request------------------   
            #header = cherrypy.request.headers
            #log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'taxa': taxalist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            #insert_log(log)
            #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====SuperTreePruneError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #--------------------------------------------------------------
    #Public /index
    index.exposed = True
    prune.exposed = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CORS():
    #print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    conn = connect_mongodb() 
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({'server.socket_host': "0.0.0.0", #'127.0.0.1',
                            'server.socket_port': 5012,
                            'log.error_file':ERROR_LOG_CHERRYPY_5012,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5012,
                            'tools.log_tracebacks.on': True
                          })
    #cherrypy.config.update({'error_page.404': error_page_404})
    
    server_config = {
             '/':{
                'tools.CORS.on': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                #'request.show_tracebacks': False,
                'request.show_tracebacks': True,
                'error_page.500': error_page_500
             }
    }
    
    #Starting Server
    cherrypy.tree.mount(Get_Tree_TreeBase_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group1),"tb"), server_config )
    
    cherrypy.engine.start()
    cherrypy.engine.block()
