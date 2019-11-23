import json
import os
import cherrypy
import time
import datetime

from service import datelife_scaling_service
from service import otol_scaling_service

from cherrypy import tools
#----------------------------------------------------------

logDbName = "WSLog"
logCollectionName = "log"
conn = None

WebService_Group = "sc"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
HOST = "0.0.0.0"
PORT = "5056"

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
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = datelife_scaling_service.scale_tree_api(tree_newick, scale_method)
            #------------------------------------------           
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception as e:
            cherrypy.log("====DatelifeScaleError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------
    #Public /index
    index.exposed = True
    scale.exposed = True
    
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

        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            
            service_result = otol_scaling_service.scale_tree_api(tree_newick)
		    
            #------------------------------------------           
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception as e:
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
    
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    
     #Configure Server
    cherrypy.config.update({'server.socket_host': HOST,
                            'server.socket_port': int(PORT),
                            'log.error_file':ERROR_LOG_CHERRYPY,
                            'log.access_file':ACCESS_LOG_CHERRYPY
                          })
    
    config = {
             '/':{
                'tools.CORS.on': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'request.show_tracebacks': True,
                'error_page.500': error_page_500
                }
    }
    
    #Mounting services
    cherrypy.tree.mount(Datelife_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group)), config)
    cherrypy.tree.mount(OToL_Scaling_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group), "ot"), config)
    
    #Starting Server
    cherrypy.engine.start()
    cherrypy.engine.block()
