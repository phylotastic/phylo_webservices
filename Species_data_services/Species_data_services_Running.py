import cherrypy
import time
import datetime
import json
import os
import sys
import collections
import pymongo
import types

from cherrypy import tools

from support import habitat_conservation_service_EOL

#--------------------------------------------------
logDbName = "WSLog"
logCollectionName = "log"
conn = None


WS_NAME = "phylotastic_ws"
WS_GROUP1 = "sd" #species data service

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5013"


#PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY_5013 = ROOT_FOLDER + "/log/%s_5013_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5013 = ROOT_FOLDER + "/log/%s_5013_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


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
        
#-------------------------------------------
class CustomException(Exception):
    pass

#--------------------------------------------------------------
class ConversionException(Exception):
    pass
    
#-------------------------------------------------------------
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

#=======================================================================
class Habitat_Conservation_EOL_Service_API(object):
    def index(self):
        return "Habitat_Conservation_EOL_Service_API : Get habitat and conservation status of species";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_habitat_conservation(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET','POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET and POST are not allowed","JSON")

            sp_lst = str(request_data['species']).strip()
            sp_lst = sp_lst.split('|')

            if len(sp_lst) == 1 and '' in sp_lst: 
               raise CustomException("'species' parameter must have a valid value")
            
            
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           service_result = habitat_conservation_service_EOL.get_habitat_conservation(sp_lst)
           #-------------------------------------------
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #---------------------------------------------
           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====HabitatConservationError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def habitat_conservation(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            taxalist = input_json["species"]
            if type(taxalist) != types.ListType:
               return return_response_error(400,"Error: 'species' parameter must be of list type","JSON")
    
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            service_result = habitat_conservation_service_EOL.get_habitat_conservation(taxalist) 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'species': taxalist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====HabitatConservationError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_habitat_conservation.exposed = True
    habitat_conservation.exposed = True

#-----------------------------------------------------------
def CORS():
    #print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    conn = connect_mongodb()
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0', #'127.0.0.1',
                            'server.socket_port': 5013,
                            'log.error_file':ERROR_LOG_CHERRYPY_5013,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5013
                          })
    
    conf_CORS = {
             '/':{
                'tools.CORS.on': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'request.show_tracebacks': False,
                #'error_page.500': error_page_500
             }
    }
    
    #Starting Server
    cherrypy.tree.mount(Habitat_Conservation_EOL_Service_API(), '/%s/%s' %(str(WS_NAME),str(WS_GROUP1)), conf_CORS )
    
    cherrypy.engine.start()
    cherrypy.engine.block()
