'''
Created on Feb 8, 2016
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

from support import species_list_service
#from support import extract_names_service

from __builtin__ import True

WebService_Group1 = "sls"
#WebService_Group2 = "fn"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5005"
PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY_5005 = ROOT_FOLDER + "/log/%s_5005_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5005 = ROOT_FOLDER + "/log/%s_5005_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


#Prefix Filename

class MultipleLevelsOfDictionary(collections.OrderedDict):
    def __getitem__(self,item):
        try:
            return collections.OrderedDict.__getitem__(self,item)
        except:
            value = self[item] = type(self)()
            return value

def return_response_error(code,type,mess,format="JSON"):
    if (format=="JSON"):
        cherrypy.response.headers['Content-Type'] = "application/json"
        cherrypy.response.headers['Retry-After']=60
        cherrypy.response.status = code
        message = {type:mess}
        return json.dumps(message)
    else:
        return "Not support yet"
    
def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError, err:
        print err
        return False
    return True


class Species_List_Service_API(object):
    def index(self):
        return "Species_List_Service API (Abu Saleh) : Gives access to user's lists of species";
    #---------------------------------------------
    #---------------------------------------------
    def get_user_lists(self, include_all=False, **request_data):
        try:
 			user_id = str(request_data['user_id']).strip();
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.get_user_lists(user_id, conn, include_all)   
        
        return service_result;

 	#------------------------------------------------
    def get_public_lists(self, include_all=False):
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.get_public_lists(conn, include_all)   
        
        return service_result;

    #------------------------------------------------
    def get_list(self, include_all=False, **request_data):
        try:
 			list_id = str(request_data['list_id']).strip();
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.get_list(int(list_id), conn, include_all)   
        
        return service_result;

    #------------------------------------------------
    def get_species(self, include_all=False, **request_data):
        try:
 			list_id = str(request_data['list_id']).strip();
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.get_list_species(int(list_id), conn, include_all)   
        
        return service_result;

    #-----------------------------------------------------
    def find_lists(self, include_all=False, user_id=-1, **request_data):
        try:
 			search_query = str(request_data['keyword']).strip();
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.find_lists(conn, search_query, user_id, include_all)   
        
        return service_result;

 	#--------------------------------------------
    def remove_list(self, **request_data):
        try:
 			user_id = str(request_data['user_id']).strip();
 			list_id = str(request_data['list_id']).strip();
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.remove_user_list(user_id, int(list_id), conn)   
        
        return service_result;

  	#---------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def replace_species(self,**request_data):
        try:
            input_json = cherrypy.request.json
            #if not (is_json(input_json)):
 			#	return return_response_error(400,"error","content-type must be application/json","JSON") 				 
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.replace_species_in_list(input_json, conn)   
           
        return service_result;

  	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def remove_species(self,**request_data):
        try:
            input_json = cherrypy.request.json
             
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.remove_species_from_list(input_json, conn)   
           
        return service_result;
 	#------------------------------------------------
    
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def insert_list(self,**request_data):
        try:
            input_json = cherrypy.request.json
            	 
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.insert_user_list(input_json, conn)   
           
        return service_result;
 	#-----------------------------------------------

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def insert_species(self,**request_data):
        try:
            input_json = cherrypy.request.json
            #if not (is_json(input_json)):
 			#	return return_response_error(400,"error","content-type must be application/json","JSON") 				 
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        conn = species_list_service.connect_mongodb()
        service_result = species_list_service.insert_species_to_list(input_json, conn)   
           
        return service_result;


    #Public /index
    index.exposed = True
    get_user_lists.exposed = True
    get_public_lists.exposed = True
    get_list.exposed = True
    find_lists.exposed = True
    get_species.exposed = True
    insert_list.exposed = True
    remove_list.exposed = True
    insert_species.exposed = True
    replace_species.exposed = True
    remove_species.exposed = True
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5005,
                            'log.error_file':ERROR_LOG_CHERRYPY_5005,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5005
                          })
    
    conf_user_case_1 = {
              '/static' : {
                           'tools.staticdir.on' : True,
                           'tools.staticdir.dir' : os.path.join(ROOT_FOLDER, 'files'),
                           'tools.staticdir.content_types' : {'xml': 'application/xml'}
               }
               
    }
    #Starting Server
    
    #cherrypy.tree.mount(Taxon_to_Species_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group1)), conf_user_case_1)
  	#cherrypy.tree.mount(Species_List_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group3),"ot") )   
    cherrypy.tree.mount(Species_List_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group1)) )
    
    cherrypy.engine.start()
    cherrypy.engine.block()
