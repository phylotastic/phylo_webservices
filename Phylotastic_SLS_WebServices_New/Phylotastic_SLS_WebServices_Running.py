#Species list services

import cherrypy
import time
import datetime
import json
import os
import sys
import collections
import types
from cherrypy import tools
from str2bool import str2bool

from support import species_list_service
from support import authenticate_user
#from distutils.util import strtobool


WebService_Group1 = "sls"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5005"

#============================================================================
ACCESS_LOG_CHERRYPY_5005 = ROOT_FOLDER + "/log/%s_5005_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5005 = ROOT_FOLDER + "/log/%s_5005_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))

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
#--------------------------------------------
#-------------------------------------------------------
class Species_List_Service_API(object):
    def index(self):
        return "Species_List_Service API : Gives access to user's lists of species"

    #-------------------GET List API--------------------------
    @cherrypy.tools.json_out()
    def get_list(self, **request_data):
          
        try:
           if request_data is not None and 'list_id' in request_data: 
              list_id = str(request_data['list_id']).strip()
              if len(list_id) == 0: 
                 raise CustomException("'list_id' parameter must have a valid value")
           else:
              list_id = -1
           #---------------------------------
           if request_data is not None and 'verbose' in request_data:
              verbose = str(request_data['verbose']).strip() 
              if type(verbose) != types.BooleanType:
                 verbose = str2bool(verbose)
           else:
              verbose = False
           #----------------------------------
           if request_data is not None and 'content' in request_data:
              content = str(request_data['content']).strip() 
              if type(content) != types.BooleanType:
                 content = str2bool(content)
           else:
              content = True
           #---------------------------------
           if request_data is not None and 'user_id' in request_data: 
              user_id = str(request_data['user_id']).strip()
              if len(user_id) == 0: 
                 raise CustomException("'user_id' parameter must have a valid value")
           else:
              user_id = None
           #--------------------------------
           if request_data is not None and 'access_token' in request_data: 
              access_token = str(request_data['access_token']).strip()
              if len(access_token) == 0: 
                 raise CustomException("'access_token' parameter must have a valid value")
           else:
              access_token = None


        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

        try:
            conn = species_list_service.connect_mongodb()
            service_result = species_list_service.get_list(conn, user_id, int(list_id), verbose, content, access_token)   
            conn.close()

            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====GETList=====", traceback=True)

            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
    
    #---------------------REMOVE List API-------------------------
    @cherrypy.tools.json_out()
    def remove_list(self, **request_data):
        try:
            user_id = str(request_data['user_id']).strip()
            list_id = str(request_data['list_id']).strip()
            access_token = str(request_data['access_token']).strip()
            if len(user_id) == 0: 
                 raise CustomException("'user_id' parameter must have a valid value")
            if len(list_id) == 0: 
                 raise CustomException("'list_id' parameter must have a valid value")
            if len(access_token) == 0: 
                 raise CustomException("'access_token' parameter must have a valid value")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON") 
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")       		 
        except Exception, e:
            return return_response_error(400,"Error: " + str(e), "JSON")


        #verify user
        token_verification = authenticate_user.verify_access_token(access_token, user_id)
        if not(token_verification['is_access_token_valid']):
           return return_response_error(401,"Error:"+ token_verification['message'],"JSON")
        #allow access to service for verified user
        try:
           conn = species_list_service.connect_mongodb()
           service_result = species_list_service.remove_user_list(user_id, int(list_id), conn)   
           conn.close()

           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====RemoveList=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

  	#----------------REPLACE Species API------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def replace_species(self,**request_data):
        try:
            input_json = cherrypy.request.json
            access_token = input_json["access_token"]
            user_id =  input_json["user_id"]
            if len(user_id) == 0: 
                 raise CustomException("'user_id' parameter must have a valid value")

            if len(access_token) == 0: 
                 raise CustomException("'access_token' parameter must have a valid value")
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON") 
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")       		 
        except Exception, e:
            return return_response_error(400,"Error: " + str(e), "JSON")

        #verify user
        token_verification = authenticate_user.verify_access_token(access_token, user_id)
        if not(token_verification['is_access_token_valid']):
            return return_response_error(401,"Error:"+ token_verification['message'],"JSON")
        #allow access to service for verified user
        try:
           conn = species_list_service.connect_mongodb()
           service_result = species_list_service.replace_species_in_list(input_json, conn)   
           conn.close()
   
           if service_result['status_code'] == 200:
              return service_result
           else:
              return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====ReplaceSpecies=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")


  	#-------------------UPDATE List Meta-data API----------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def update_list(self,**request_data):
        try:
            input_json = cherrypy.request.json
            access_token = input_json["access_token"]
            user_id =  input_json["user_id"] 
            if len(user_id) == 0: 
               raise CustomException("'user_id' parameter must have a valid value")

            if len(access_token) == 0: 
               raise CustomException("'access_token' parameter must have a valid value")
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON") 
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")       		 
        except Exception, e:
            return return_response_error(400,"Error: " + str(e), "JSON")

        #verify user
        token_verification = authenticate_user.verify_access_token(access_token, user_id)
        if not(token_verification['is_access_token_valid']):
            return return_response_error(401,"Error:"+ token_verification['message'],"JSON")
        try:
            #allow access to service for verified user
            conn = species_list_service.connect_mongodb()
            service_result = species_list_service.update_list_metadata(input_json, conn)   
            conn.close()
   
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====UpdateList=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")


    #-----------------------------------------------
    '''	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def remove_species(self,**request_data):
        try:
            input_json = cherrypy.request.json
            access_token = input_json["access_token"]
            user_id =  input_json["user_id"]
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"NotJSON")     		 
        except Exception, e:
            return return_response_error(400,"Error:" + str(e), "NotJSON")

        #verify user
        token_verification = authenticate_user.verify_access_token(access_token, user_id)
        if not(token_verification['is_access_token_valid']):
            return return_response_error(400,"Error:"+ token_verification['message'],"NotJSON")
        #allow access to service for verified user
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.remove_species_from_list(input_json, conn)   
        conn.close()
   
        return service_result
    ''' 	
 	#---------------------INSERT List API-------------------------- 
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def insert_list(self,**request_data):
        try:
            input_json = cherrypy.request.json
             				 
        except Exception, e:
            return return_response_error(400,"Error: "+ str(e),"JSON")

        try:
            conn = species_list_service.connect_mongodb()
            service_result = species_list_service.insert_user_list(input_json, conn)   
            conn.close()
   
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====InsertList=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
 	#--------------------------------------------------------------------
    '''
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def insert_species(self,**request_data):
        try:
            input_json = cherrypy.request.json
            #if not (is_json(input_json)):
 			#	return return_response_error(400,"error","content-type must be application/json","JSON") 				 
        except Exception, e:
            return return_response_error(400,"Error:" + str(e), "NotJSON")
        
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.insert_species_to_list(input_json, conn)   
        conn.close()   
        return service_result;
    '''

    #Public /index
    index.exposed = True
    get_list.exposed = True
    insert_list.exposed = True
    remove_list.exposed = True
    replace_species.exposed = True
    update_list.exposed = True
    #insert_species.exposed = True
    #remove_species.exposed = True
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',#'127.0.0.1'
                            'server.socket_port': 5005,
                            'log.error_file':ERROR_LOG_CHERRYPY_5005,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5005
                          })
    
    config = {
             '/':{
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'request.show_tracebacks': False
                #'request.show_tracebacks': True,
                #'error_page.500': error_page_500
             }
    } 
    #Starting Server
    
    #cherrypy.tree.mount(Taxon_to_Species_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group1)), conf_user_case_1)
  	#cherrypy.tree.mount(Species_List_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group3),"ot") )   
    cherrypy.tree.mount(Species_List_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group1)), config)
    
    cherrypy.engine.start()
    cherrypy.engine.block()
