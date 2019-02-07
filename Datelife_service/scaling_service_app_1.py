import json
import os
import cherrypy
import time
import datetime
import datelife_rserve
import otol_scaling_service

import pymongo
from cherrypy import tools
#----------------------------------------------------------

logDbName = "WSLog"
logCollectionName = "log"
conn = None

WebService_Group = "sc"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
HOST = "127.0.0.1"
PORT = "5071"
#PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY = ROOT_FOLDER + "/log/%s_access_log.log" %(PORT+"_"+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY = ROOT_FOLDER + "/log/%s_error_log.log" %(PORT+"_"+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


#-----------------------------------------------------------
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

class CustomException(Exception):
    pass

#-----------------------------------------------------------
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
    insert_status = log_collection.insert_one(log_msg)


#------------------------------------------------------------    
class Datelife_Service_API(object):
    def index(self):
        return "Datelife_Service API : Scales a species tree";

    #-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def scale(self,**request_data):
        http_method = cherrypy.request.method
        if http_method not in ['POST', 'OPTIONS']:
           return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

        scale_method = "median"
        try:
            input_json = cherrypy.request.json
            tree_newick = input_json["newick"]
            if len(tree_newick) == 0: 
               raise CustomException("'newick' parameter must have a valid value")

            if 'method' in input_json: 
               scale_method = input_json["method"] 
               if scale_method not in ["median", "sdm"]:
                  raise CustomException("'%s' is not a valid value for 'method' parameter"%(scale_method))          
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = datelife_rserve.scale_tree_api_1(tree_newick, scale_method)
            #-------------log request------------------   
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'tree_newick': tree_newick}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------           
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====DatelifeScaleError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def metadata_scale(self,**request_data):
        try:
            input_json = cherrypy.request.json
            tree_newick = input_json["newick"]
            if len(tree_newick) == 0: 
               raise CustomException("'newick' parameter must have a valid value")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
           service_result = datelife_service.scale_metadata_api(tree_newick)   
		   #-------------log request------------------   
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'tree_newick': tree_newick}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #------------------------------------------           

           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====MetaDataScaleError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")


 	#------------------------------------------------
    #Public /index
    index.exposed = True
    scale.exposed = True
    #metadata_scale.exposed = True

#----------------------------------------------------------
class OToL_Scaling_Service_API(object):
    def index(self):
        return "OToL Scaling API : Scales a species tree using Open Tree of Life API";

    #-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def scale(self,**request_data):
        http_method = cherrypy.request.method
        if http_method not in ['POST', 'OPTIONS']:
           return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

        try:
            input_json = cherrypy.request.json
            tree_newick = input_json["newick"]
            if len(tree_newick) == 0: 
               raise CustomException("'newick' parameter must have a valid value")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            
            service_result = otol_scaling_service.scale_tree_api(tree_newick)
		    #-------------log request------------------   
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'tree_newick': tree_newick}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------           
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====OToLScaleError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #Public /index
    index.exposed = True
    scale.exposed = True
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def CORS():
    #print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"
    
#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    conn = connect_mongodb() 
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({#'server.socket_host': '0.0.0.0',
                            'server.socket_port': int(PORT),
                            'tools.proxy.on': True,
                            'tools.proxy.base': 'https://phylo.cs.nmsu.edu',
                            'log.error_file':ERROR_LOG_CHERRYPY,
                            'log.access_file':ACCESS_LOG_CHERRYPY
                          })
    
    config = {
             '/':{
                'tools.CORS.on': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'request.show_tracebacks': False
                }
    }
    
    #Starting Server
    cherrypy.tree.mount(Datelife_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group)), config)
    cherrypy.tree.mount(OToL_Scaling_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group), "ot"), config)
    
    cherrypy.engine.start()
    cherrypy.engine.block()
