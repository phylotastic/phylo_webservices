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

from cherrypy import tools
from str2bool import str2bool

from service import species_to_image_service_EOL
from service import species_to_url_service_EOL

#==============================================================

WebService_Group1 = "si"
WebService_Group2 = "sl"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
HOST = "0.0.0.0"  #"127.0.0.1"
PORT = "5054"

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
        
#------------------------------------------
class CustomException(Exception):
    pass

#-------------------------------------------

#============================Species_Image_Service=============================
class Species_Image_Service_API(object):
    def index(self):
        return "Species_Image_Service API : Find images of species";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_images(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            sp_lst = str(request_data['species']).strip()
            specieslist = sp_lst.split('|')
            
            if len(specieslist) == 1 and '' in specieslist: 
               raise CustomException("'species' parameter must have a valid value")
            if len(specieslist) > 60: 
               return return_response_error(403,"Error: Currently more than 60 species is not supported","JSON")
            
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = species_to_image_service_EOL.get_images_species(specieslist)   
            result_json = service_result

            #------------------------------------------
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====SpeciesGetImageError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #------------------------------------------------
    def get_image(self, species_id=None):
        if species_id is None:
            return return_response_error(400,"Error: Missing parameter 'species_id'", "JSON")
        
        try:
            service_result = species_to_image_service_EOL.get_image_species_id(int(species_id))
            result_json = json.loads(service_result)
            return service_result

        except Exception as e:
            cherrypy.log("=====GetImageError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def images(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            
            species_list = input_json["species"]
            if type(species_list) is not list:
               return return_response_error(400,"Error: 'species' parameter must be of list type","JSON")

            if len(species_list) == 0: 
               raise CustomException("'species' parameter must have a valid value")
            if len(species_list) > 60: 
               return return_response_error(403,"Error: Currently more than 60 species is not supported","JSON")
        
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = species_to_image_service_EOL.get_images_species(species_list, True)
            result_json = service_result   
        
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====SpeciesPostImageError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

 	#------------------------------------------------
    #Public /index
    index.exposed = True
    get_images.exposed = True
    get_image.exposed = True
    images.exposed = True

#============================Species_Url_Service===========================
class Species_Url_Service_API(object):
    def index(self):
        return "Species_Url_Service API: Find EOL links of species";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_links(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            sp_lst = str(request_data['species']).strip();
            species_list = sp_lst.split('|')
            
            if len(species_list) == 1 and '' in species_list: 
               raise CustomException("'species' parameter must have a valid value")
            if len(species_list) > 60: 
               return return_response_error(403,"Error: Currently more than 60 species is not supported","JSON")
            
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = species_to_url_service_EOL.get_eolurls_species(species_list)   
            
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====SpeciesGetLinkError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def links(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            species_list = input_json["species"]
            if type(species_list) is not list:
               return return_response_error(400,"Error: 'species' parameter must be of list type","JSON")

            if len(species_list) == 0: 
               raise CustomException("'species' parameter must have a valid value")
            if len(species_list) > 60: 
               return return_response_error(403,"Error: Currently more than 60 species is not supported","JSON")   				 
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = species_to_url_service_EOL.get_eolurls_species(species_list, True)   
            #------------------------------------------           
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====SpeciesPostLinkError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")   
        
 	#------------------------------------------------
    #Public /index
    index.exposed = True
    get_links.exposed = True
    links.exposed = True


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CORS():
    #print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)

    #Configure Server
    cherrypy.config.update({'server.socket_host': HOST, #'0.0.0.0' "127.0.0.1",
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
                'request.show_tracebacks': True,
                'error_page.500': error_page_500
             }
    }
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

    #Mounting services    
    cherrypy.tree.mount(Species_Image_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group1), "eol"), conf_app)
    cherrypy.tree.mount(Species_Url_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group2), "eol"), conf_app)

    #Starting Server
    cherrypy.engine.start()
    cherrypy.engine.block()
