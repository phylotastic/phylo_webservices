'''
Created on Feb 1, 2016
@author: Abu Saleh
'''

import cherrypy
import time
import datetime
import json
import os
import sys
import collections
import subprocess
from cherrypy import tools

from support import taxon_to_species_service_OpenTree
from support import extract_names_service
from support import resolve_names_service
from support import get_tree_service
#from support import usecase_text, treebase_api

from __builtin__ import True

WebService_Group1 = "ts"
WebService_Group2 = "fn"
WebService_Group3 = "tnrs"
WebService_Group4 = "gt"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5004"
PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY_5004 = ROOT_FOLDER + "/log/%s_5004_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5004 = ROOT_FOLDER + "/log/%s_5004_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


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
    
def return_success_get(forester_object):
    cherrypy.response.headers['Content-Type'] = "application/json"
    cherrypy.response.headers['Retry-After']=60
    cherrypy.response.status = 200
    return json.dumps(forester_object)

def run_command(command):
    try:
        from subprocess import Popen, PIPE, STDOUT
        p = Popen(command, stdout=PIPE, stderr=STDOUT)
        for line in p.stdout:
            if (str(line).strip().upper()[:25] == "FINAL_RESULT_JSON_OUTPUT:"):
                return line[25:]
        return None
    except Exception,err:
        print err
        return None
def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError, err:
        print err
        return False
    return True

def readContent(url):
    import urllib2
    data = []
    if (url[:7] == "http://"):
        data = urllib2.urlopen(url)
        return data
    else:
        return url

def runWebServiceFunction(FUNCTION_NAME,WSDL_URL,PARAMS,TYPE_RUNNING):
    try:
        shellCall = []
        shellCall.append("java")
        shellCall.append("-jar")
        shellCall.append("%s" %(os.path.join(ROOT_FOLDER,"model/WSClient.jar")))
        shellCall.append("%s" %(str(WSDL_URL)))
        shellCall.append("%s" %(TYPE_RUNNING))
        shellCall.append("%s" %(FUNCTION_NAME))
        for param in PARAMS:
            shellCall.append(param)
        print shellCall
        return run_command(shellCall)
    except:
        return None

    
class Taxon_to_Species_Service_API(object):
    def index(self):
        return "Taxon_to_Species_Service API (Abu Saleh) : Get Species from Taxon";
    
    def all_species(self,**request_data):
        try:
            taxon = str(request_data['taxon']).strip();
            
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = taxon_to_species_service_OpenTree.get_all_species(taxon)   
        
        return service_result;

    def country_species(self,**request_data):
        try:
            taxon = str(request_data['taxon']).strip();
            country = str(request_data['country']).strip();
            
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = taxon_to_species_service_OpenTree.get_country_species(taxon, country)   
        
        return service_result;

        
    #Public /index
    index.exposed = True
    all_species.exposed = True
    country_species.exposed = True


class Find_ScientificNames_Service_API(object):
    def index(self):
        return "Find_ScientificNames_Service API (Abu Saleh) : Find Scientific names from Url, Text, Files";
    #---------------------------------------------
    def names_url(self,**request_data):
        try:
            url = str(request_data['url']).strip();
            
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = extract_names_service.extract_names_URL(url)   
        
        return service_result;
    #------------------------------------------------
    def names_text(self,**request_data):
        try:
            text = str(request_data['text']).strip();
            
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = extract_names_service.extract_names_TEXT(text)   
        
        return service_result;

    #Public /index
    index.exposed = True
    names_url.exposed = True
    names_text.exposed = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Resolve_ScientificNames_OpenTree_Service_API(object):
    def index(self):
        return "Resolve_ScientificNames_OpenTree_Service API (Abu Saleh) : Resolve Scientific names from OpenTree";
    #---------------------------------------------
    def resolve(self,**request_data):
        try:
            names = str(request_data['names']).strip();
            nameslist = names.split('|')
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = resolve_names_service.resolve_names_OT(nameslist)   
        
        return service_result;
    #------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def names(self,**request_data):
        try:
            input_json = cherrypy.request.json
            nameslist = input_json["scientificNames"]
 	    
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = resolve_names_service.resolve_names_OT(nameslist, True)   
        
        return service_result;

    #Public /index
    index.exposed = True
    resolve.exposed = True
    names.exposed = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Resolve_ScientificNames_GNR_Service_API(object):
    def index(self):
        return "Resolve_ScientificNames_GNR_Service API (Abu Saleh) : Resolve Scientific names from Global Names Resolver";
    #---------------------------------------------
    def resolve(self,**request_data):
        try:
            names = str(request_data['names']).strip();
            nameslist = names.split('|')
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = resolve_names_service.resolve_names_GNR(nameslist)   
        
        return service_result;
    #------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def names(self,**request_data):
        try:
            input_json = cherrypy.request.json
            nameslist = input_json["scientificNames"]
 	    
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = resolve_names_service.resolve_names_GNR(nameslist, True)   
        
        return service_result;

    #Public /index
    index.exposed = True
    resolve.exposed = True
    names.exposed = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Get_Tree_OpenTree_Service_API(object):
    def index(self):
        return "Get_Tree_OpenTree_Service_API API (Abu Saleh) : Get Subtree or Induced Subtree from OpenTree";
    #---------------------------------------------
    def get_tree(self,**request_data):
        try:
            taxa = str(request_data['taxa']).strip();
            taxalist = taxa.split('|')
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
 	nameslist_json = resolve_names_service.resolve_names_OT(taxalist, True)
 	nameslist = nameslist_json["resolvedNames"]
        service_result = get_tree_service.get_tree_OT(nameslist)   
        
        return service_result;
    #------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tree(self,**request_data):
        try:
            input_json = cherrypy.request.json
            nameslist = input_json["resolvedNames"]
 	    
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = get_tree_service.get_tree_OT(nameslist, True)   
        
        return service_result;

    #Public /index
    index.exposed = True
    get_tree.exposed = True
    tree.exposed = True

def CORS():
    print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print "Thu ran CORS"
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5004,
                            'log.error_file':ERROR_LOG_CHERRYPY_5004,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5004
                          })
    
    conf_user_case_1 = {
              '/static' : {
                           'tools.staticdir.on' : True,
                           'tools.staticdir.dir' : os.path.join(ROOT_FOLDER, 'files'),
                           'tools.staticdir.content_types' : {'xml': 'application/xml'}
               }
               
    }
    conf_thanhnh = {
             '/':{
                'tools.CORS.on': True
             }
    }
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

    #Starting Server
    #cherrypy.tree.mount(Phylotastic_UserCase_2_GenerateTreesFromText(), '/%s/%s' %(str(WS_NAME),str(USER_CASE_2_2)), conf_user_case_1)
    cherrypy.tree.mount(Taxon_to_Species_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group1)), conf_user_case_1)
    cherrypy.tree.mount(Find_ScientificNames_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group2)), conf_thanhnh )
    cherrypy.tree.mount(Resolve_ScientificNames_OpenTree_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group3),"ot"),conf_thanhnh )
    cherrypy.tree.mount(Resolve_ScientificNames_GNR_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group3),"gnr"), conf_thanhnh )
    cherrypy.tree.mount(Get_Tree_OpenTree_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group4),"ot"),conf_thanhnh )

    cherrypy.engine.start()
    cherrypy.engine.block()
