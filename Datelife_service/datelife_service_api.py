import json
import os
import cherrypy
import time
import datetime
import datelife_service
import pymongo
from cherrypy import tools
#----------------------------------------------------------

logDbName = "WSLog"
logCollectionName = "log"
conn = None

WebService_Group = "sc"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5009"
PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY_5009 = ROOT_FOLDER + "/log/%s_5009_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5009 = ROOT_FOLDER + "/log/%s_5009_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


#-----------------------------------------------------------
def return_response_error(error_code, error_message,response_format="JSON"):
    error_response = {'message': error_message, 'status_code':error_code}
    if (response_format == "JSON"):
        return json.dumps(error_response)
    else:
        return error_response

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
    insert_status = log_collection.insert(log_msg)


#------------------------------------------------------------    
class Datelife_Service_API(object):
    def index(self):
        return "Datelife_Service API : Scales a species tree";

    #-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def scale(self,**request_data):
        try:
            input_json = cherrypy.request.json
            tree_newick = input_json["newick"]
           				 
        except:
            return return_response_error(400,"KeyError: Missing parameter %s"%(str(e)),"NotJSON")
        
        service_result = datelife_service.scale_tree_api(tree_newick)   
		#-------------log request------------------   
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'tree_newick': tree_newick}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
        insert_log(log)
        #------------------------------------------           

        return service_result
 	#------------------------------------------------
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
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5009,
                            'log.error_file':ERROR_LOG_CHERRYPY_5009,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5009
                          })
    
    conf_cors = {
             '/':{
                'tools.CORS.on': True
             }
    }
    
    #Starting Server
    cherrypy.tree.mount(Datelife_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group)), conf_cors)
    #cherrypy.tree.mount(Taxon_Genome_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group1), "ncbi"), conf_thanhnh)
    
    cherrypy.engine.start()
    cherrypy.engine.block()
