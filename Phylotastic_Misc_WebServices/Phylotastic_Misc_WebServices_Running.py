'''
Created on June 23, 2016
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

from support import compare_trees_service
from support import tree_studies_service

WS_NAME = "phylotastic_ws"
WS_GROUP1 = "md" #metadata service

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5006"
PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY_5006 = ROOT_FOLDER + "/log/%s_5006_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5006 = ROOT_FOLDER + "/log/%s_5006_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


def return_response_error(error_code, error_message,response_format="JSON"):
    error_response = {'message': error_message, 'status_code':error_code}
    if (response_format == "JSON"):
        return json.dumps(error_response)
    else:
        return error_response
#--------------------------------------------------------------
class ConversionException(Exception):
    pass
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Compare_Trees_Service_API(object):

 	def index(self):
 		return "Compare_Trees_Service API: Compare two phylogenetic trees"

 	@cherrypy.tools.json_out()
 	@cherrypy.tools.json_in()
 	def compare_trees(self,**request_data):
 		try:
 			input_json = cherrypy.request.json
 			tree1_str = input_json["tree1_nwk"]
 			tree2_str = input_json["tree2_nwk"]
 		except KeyError, e:
 			return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"NotJSON")
 		except Exception, e:
 			return return_response_error(400,"Error:" + str(e), "NotJSON")
 
 		service_result = compare_trees_service.compare_trees(tree1_str, tree2_str)
 		return service_result;
 	
 	#------------------------------------------------
 	index.exposed = True	
 	compare_trees.exposed = True


class Tree_Studies_Service_API(object):
    def index(self):
        return "Tree_Studies_Service API : Find supported studies of an induced tree from OpenTreeOfLife";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_studies(self, **request_data):
        try:
            lst = str(request_data['list']).strip()
            list_type = str(request_data['list_type']).strip()  
            if list_type.lower() == "ottids":
               ottid_lst = []
               for s in lst.split('|'):
                   s = s.strip()
                   if s.isdigit():
                      ottid_lst.append(int(s))
                   else:
                      raise ConversionException("ottids are not numeric. If list_type parameter is 'ottids', then the list parameter must contain numeric values")
               service_result = tree_studies_service.get_studies_from_ids(ottid_lst) 
            elif list_type.lower() == "taxa":
                 taxa_lst = [s.strip() for s in lst.split('|')]
                 service_result = tree_studies_service.get_studies_from_names(taxa_lst) 
            else:
                 raise ConversionException("'%s' is not a valid value for 'list_type' parameter"%(list_type))          
        except KeyError, e:
            return return_response_error(400,"KeyError: Missing parameter %s"%(str(e)),"NotJSON")
        except ConversionException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"NotJSON")
        
        return service_result
    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def studies(self,**request_data):
        try:
            input_json = cherrypy.request.json
            lst = input_json["list"]
            list_type = input_json["list_type"]
            if list_type.lower() == "ottids":
               ottid_lst = lst
               service_result = tree_studies_service.get_studies_from_ids(ottid_lst, post=True) 
            elif list_type.lower() == "taxa":
               taxa_lst = lst
               service_result = tree_studies_service.get_studies_from_names(taxa_lst, post=True) 
            else:
               raise ConversionException("'%s' is not a valid value for 'list_type' parameter"%(list_type))          
        except KeyError, e:
            return return_response_error(400,"KeyError: Missing parameter %s"%(str(e)),"NotJSON")
        except ConversionException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"NotJSON")
        
        return service_result

    #Public /index
    index.exposed = True
    get_studies.exposed = True
    studies.exposed = True

#-----------------------------------------------------------
def CORS():
    print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5006,
                            'log.error_file':ERROR_LOG_CHERRYPY_5006,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5006
                          })
    
    conf_CORS = {
             '/':{
                'tools.CORS.on': True
             }
    }
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

    #Starting Server
    cherrypy.tree.mount(Tree_Studies_Service_API(), '/%s/%s' %(str(WS_NAME),str(WS_GROUP1)), conf_CORS )
    cherrypy.tree.mount(Compare_Trees_Service_API(), '/%s' %(str(WS_NAME)), conf_CORS )
    
    cherrypy.engine.start()
    cherrypy.engine.block()
