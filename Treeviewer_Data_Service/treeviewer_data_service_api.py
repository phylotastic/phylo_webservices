import json
import subprocess
import cherrypy

from cherrypy import tools
import data_handler

from distutils.util import strtobool
import types

WS_NAME = "phylotastic_ws"
WS_GROUP1 = "ds" #data service

#===========================================================
def return_response_error(error_code, error_message,response_format="JSON"):
    error_response = {'message': error_message, 'status_code':error_code}
    if (response_format == "JSON"):
        return json.dumps(error_response)
    else:
        return error_response

#---------------------------------------------------------    
class TreeViewer_Data_Service_API(object):
    def index(self):
        return "TreeViewer_Data_Service API : Find info of species for TreeViewer";

    #---------------------------------------------
    def get_image_info(self, species=None, image_id=0, next_image=False):
        if species is None:
            return return_response_error(400,"Error:Missing parameter 'species'")
        if type(next_image) != types.BooleanType:
            next_image = strtobool(next_image)
   
        service_result = data_handler.image_info_controller(species, int(image_id), next_image)   
        
        return json.dumps(service_result)

    #--------------------------------------------------
    def get_link_info(self, species=None):
        if species is None:
            return return_response_error(400,"Error:Missing parameter 'species'")
           
        service_result = data_handler.link_info_controller(species)   
        
        return json.dumps(service_result)

    #--------------------------------------------------------
    def image_info_exists(self, species=None):
        if species is None:
            return return_response_error(400,"Error:Missing parameter 'species'")
           
        service_result = data_handler.images_exists(species)           

        return json.dumps(service_result)

    #---------------------------------------------------------
    def images_download_time(self,newick=None):
        if newick is None:
            return return_response_error(400,"Error:Missing parameter 'newick'")
        
        service_result = data_handler.estimate_image_download(newick)
        #if (service_result['number_species'] != 0):
           #subprocess.Popen(args=['python', 'data_handler.py', '%s' % newick], shell=True)
        
        return json.dumps(service_result) 

    #---------------------------------------------------------
    def download_all_images(self,newick=None):
        if newick is None:
            return return_response_error(400,"Error:Missing parameter 'newick'")
        
        service_result = data_handler.load_all_images(newick)
        if service_result['download_complete']:
           return "<b>Download of images completed. Please click the load images button again</b>" 
       
 	#------------------------------------------------
    #Public /index
    index.exposed = True
    get_image_info.exposed = True
    get_link_info.exposed = True
    image_info_exists.exposed = True
    images_download_time.exposed = True
    download_all_images.exposed = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CORS():
    cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"


#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5008,
                          })
    
    conf_CORS = {
             '/':{
                'tools.CORS.on': True
             }
    }
    
    #Starting Server
    cherrypy.tree.mount(TreeViewer_Data_Service_API(), '/%s/%s' %(str(WS_NAME),str(WS_GROUP1)), conf_CORS )
    
    cherrypy.engine.start()
    cherrypy.engine.block()
