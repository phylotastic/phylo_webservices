'''
Phylotastic Web Services
@author: Abu Saleh
'''

import cherrypy
import time
import datetime
import json
import os
import sys
import collections
import datetime 
import types

from cherrypy import tools
from str2bool import str2bool

from service import resolve_names_service

#from __builtin__ import True

#==============================================================

WebService_Group = "tnrs"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
HOST = "0.0.0.0" #"127.0.0.1" "phylo.cs.nmsu.edu"
PORT = "5051"

#============================================================================
ACCESS_LOG_CHERRYPY = ROOT_FOLDER + "/log/%s_access_log.log" %(PORT+"_"+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY = ROOT_FOLDER + "/log/%s_error_log.log" %(PORT+"_"+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))

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
       
#-------------------------------------------
class CustomException(Exception):
    pass


#=======================Resolve_ScientificNames_OpenTree_Service===========================
class Resolve_ScientificNames_OpenTree_Service_API(object):
    def index(self):
        return "Resolve_ScientificNames_OpenTree_Service API: Resolve Scientific names from OpenTree";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def resolve(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            names = str(request_data['names']).strip()
            nameslist = names.split('|')

            if len(nameslist) == 1 and '' in nameslist: 
               raise CustomException("'names' parameter must have a valid value")

            match_type = False
            if request_data is not None and 'fuzzy_match' in request_data:
               match_type = str(request_data['fuzzy_match']).strip()
               if type(match_type) != types.BooleanType:
                  match_type = str2bool(match_type)
               
            multi_match = False
            if request_data is not None and 'multiple_match' in request_data:
               multi_match = str(request_data['multiple_match']).strip()
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
            
            if len(nameslist) > 3000: 
               return return_response_error(403,"Error: Currently more than 3000 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = resolve_names_service.resolve_names_OT(nameslist, match_type, multi_match)   
            result_json = service_result
            #------------------------------------------
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====ResolveNamesOTGetError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            nameslist = input_json["scientificNames"]
            if type(nameslist) != types.ListType:
               return return_response_error(400,"Error: 'scientificNames' parameter must be of list type","JSON")    
     
            if len(nameslist) == 0: 
               raise CustomException("'scientificNames' parameter must have a valid value")

            match_type = False
            if 'fuzzy_match' in input_json:
               match_type = input_json['fuzzy_match']
               if type(match_type) != types.BooleanType:
                  match_type = str2bool(match_type)
                  
            multi_match = False
            if 'multiple_match' in input_json:
               multi_match = input_json['multiple_match']
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)

            if len(nameslist) > 3000: 
               return return_response_error(403,"Error: Currently more than 3000 names is not supported","JSON")
   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = resolve_names_service.resolve_names_OT(nameslist, match_type, multi_match)   
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====ResolveNamesOTPostError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------
    #Public /index
    index.exposed = True
    resolve.exposed = True
    names.exposed = True

#==============================Resolve_ScientificNames_GNR_Service======================
class Resolve_ScientificNames_GNR_Service_API(object):
    def index(self):
        return "Resolve_ScientificNames_GNR_Service API: Resolve Scientific names from Global Names Resolver";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def resolve(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            names = str(request_data['names']).strip();
            nameslist = names.split('|')

            if len(nameslist) == 1 and '' in nameslist: 
               raise CustomException("'names' parameter must have a valid value")

            match_type = False
            if request_data is not None and 'fuzzy_match' in request_data:
               match_type = str(request_data['fuzzy_match']).strip()
               if type(match_type) != types.BooleanType:
                  match_type = str2bool(match_type)

            multi_match = False
            if request_data is not None and 'multiple_match' in request_data:
               multi_match = str(request_data['multiple_match']).strip()
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)   
            
            if len(nameslist) > 3000: 
               return return_response_error(403,"Error: Currently more than 3000 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = resolve_names_service.resolve_names_GNR(nameslist, match_type, multi_match)   
            
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====ResolveNamesGNRGetError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            nameslist = input_json["scientificNames"]
            if type(nameslist) != types.ListType:
               return return_response_error(400,"Error: 'scientificNames' parameter must be of list type","JSON")

            if len(nameslist) == 0: 
               raise CustomException("'scientificNames' parameter must have a valid value")

            match_type = False
            if 'fuzzy_match' in input_json:
               match_type = input_json['fuzzy_match']
               if type(match_type) != types.BooleanType:
                  match_type = str2bool(match_type)

            multi_match = False      
            if 'multiple_match' in input_json:
               multi_match = input_json['multiple_match']
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
               
            if len(nameslist) > 3000: 
               return return_response_error(403,"Error: Currently more than 3000 names is not supported","JSON")
   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = resolve_names_service.resolve_names_GNR(nameslist, match_type, multi_match)   
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====ResolveNamesGNRPostError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------
    #Public /index
    index.exposed = True
    resolve.exposed = True
    names.exposed = True

#==============================Resolve_ScientificNames_iPlant_Collaborative_Service======================
class Resolve_ScientificNames_iPLant_Service_API(object):
    def index(self):
        return "Resolve_ScientificNames_iPlant_Service API: Resolve plant Scientific names from iPlant Collaborative";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def resolve(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            names = str(request_data['names']).strip();
            nameslist = names.split('|')

            if len(nameslist) == 1 and '' in nameslist: 
               raise CustomException("'names' parameter must have a valid value")

            match_type = False
            if request_data is not None and 'fuzzy_match' in request_data:
               match_type = str(request_data['fuzzy_match']).strip()
               if type(match_type) != types.BooleanType:
                  match_type = str2bool(match_type)

            multi_match = False
            if request_data is not None and 'multiple_match' in request_data:
               multi_match = str(request_data['multiple_match']).strip()
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)   
            
            if len(nameslist) > 500: 
               return return_response_error(403,"Error: Currently more than 500 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = resolve_names_service.resolve_names_iPlant(nameslist, match_type, multi_match)   
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====ResolveNamesiPlantGetError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            nameslist = input_json["scientificNames"]
            if type(nameslist) != types.ListType:
               return return_response_error(400,"Error: 'scientificNames' parameter must be of list type","JSON")

            if len(nameslist) == 0: 
               raise CustomException("'scientificNames' parameter must have a valid value")

            match_type = False
            if 'fuzzy_match' in input_json:
               match_type = input_json['fuzzy_match']
               if type(match_type) != types.BooleanType:
                  match_type = str2bool(match_type)

            multi_match = False      
            if 'multiple_match' in input_json:
               multi_match = input_json['multiple_match']
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
               
            if len(nameslist) > 1000: 
               return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")
   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = resolve_names_service.resolve_names_iPlant(nameslist, match_type, multi_match)   
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====ResolveNamesiPlantPostError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------
    #Public /index
    index.exposed = True
    resolve.exposed = True
    names.exposed = True


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
                            'log.access_file':ACCESS_LOG_CHERRYPY,
                            'tools.log_tracebacks.on': True
                          })
    
    conf_app = {
             '/':{
                'tools.CORS.on': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'error_page.500': error_page_500,
                'request.show_tracebacks': True
             }
    }
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

    #Mounting Services
    cherrypy.tree.mount(Resolve_ScientificNames_OpenTree_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group),"ot"), conf_app)
    cherrypy.tree.mount(Resolve_ScientificNames_GNR_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group),"gnr"), conf_app)
    cherrypy.tree.mount(Resolve_ScientificNames_iPLant_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group),"ip"), conf_app)
    #Starting Server
    cherrypy.engine.start()
    cherrypy.engine.block()
