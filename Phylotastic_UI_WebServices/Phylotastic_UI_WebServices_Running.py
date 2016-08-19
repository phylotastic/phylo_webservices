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
import pymongo
import datetime 

#from bson import json_util
#from bson.json_util import dumps

from cherrypy import tools

from support import taxon_to_species_service_OpenTree
from support import extract_names_service
from support import resolve_names_service
from support import get_tree_service
from support import species_to_image_service_EOL
from support import species_to_url_service_EOL
from support import taxon_genome_species_service_NCBI
#from support import usecase_text, treebase_api

from __builtin__ import True

logDbName = "WSLog"
logCollectionName = "log"
conn = None

WebService_Group1 = "ts"
WebService_Group2 = "fn"
WebService_Group3 = "tnrs"
WebService_Group4 = "gt"
WebService_Group5 = "si"
WebService_Group6 = "sl"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5004"
PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY_5004 = ROOT_FOLDER + "/log/%s_5004_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5004 = ROOT_FOLDER + "/log/%s_5004_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


#Prefix Filename

def return_response_error(error_code, error_message,response_format="JSON"):
    error_response = {'message': error_message, 'status_code':error_code}
    if (response_format == "JSON"):
        #cherrypy.response.headers['Content-Type'] = "application/json"
        #cherrypy.response.headers['Retry-After']=60
        #cherrypy.response.status = error_code    
        return json.dumps(error_response)
    else:
        return error_response

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError, err:
        print err
        return False
    return True
#--------------------------------------------
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


#--------------------------------------------------------------    
class Taxon_Genome_Service_API(object):
    def index(self):
        return "Taxon_Genome_Service_API (Abu Saleh) : Find species (of a taxon) that have genome sequence in NCBI";
    #---------------------------------------------
    def genome_species(self, **request_data):
        try:
            taxonName = str(request_data['taxon']).strip();
            
        except Exception, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)), "JSON")
        
        service_result = taxon_genome_species_service_NCBI.get_genome_species(taxonName)   
        #-------------log request------------------
        result_json = json.loads(service_result)
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
        insert_log(log)
        #------------------------------------------
        return service_result;
 	#------------------------------------------------
    #Public /index
    index.exposed = True
    genome_species.exposed = True

#------------------------------------------------------------
class Taxon_to_Species_Service_API(object):
    def index(self):
        return "Taxon_to_Species_Service API (Abu Saleh) : Get Species from Taxon";
    
    def all_species(self,**request_data):
        try:
            taxon = str(request_data['taxon']).strip();
            
        except Exception, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)), "JSON")
        
        service_result = taxon_to_species_service_OpenTree.get_all_species(taxon)   
        #-------------log request------------------
        result_json = json.loads(service_result)
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
        insert_log(log)
        #------------------------------------------
        return service_result;

    def country_species(self,**request_data):
        try:
            taxon = str(request_data['taxon']).strip();
            country = str(request_data['country']).strip();
            
        except Exception, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)), "JSON")
        
        service_result = taxon_to_species_service_OpenTree.get_country_species(taxon, country)   
        #-------------log request------------------
        result_json = json.loads(service_result)
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
        insert_log(log)
        #------------------------------------------
        return service_result;

        
    #Public /index
    index.exposed = True
    all_species.exposed = True
    country_species.exposed = True

#------------------------------------------------------------
class Species_Image_Service_API(object):
    def index(self):
        return "Species_Image_Service API (Abu Saleh) : Find images of species";

    #---------------------------------------------
    def get_images(self, **request_data):
        try:
            sp_lst = str(request_data['species']).strip();
            specieslist = sp_lst.split('|')
        except Exception, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)), "JSON")
        
        service_result = species_to_image_service_EOL.get_images_species(specieslist)   
        #-------------log request------------------
        result_json = json.loads(service_result)
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
        insert_log(log)
        #------------------------------------------
        return service_result;

 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def images(self,**request_data):
        try:
            input_json = cherrypy.request.json
            #print input_json
            species_list = input_json["species"]
            
        except Exception, e:
            return return_response_error(400,"Error:" + str(e), "NotJSON")
        
        service_result = species_to_image_service_EOL.get_images_species(species_list, True)   
        #-------------log request------------------
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'species':species_list}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
        insert_log(log)
        #------------------------------------------   
        return service_result;
 	#------------------------------------------------
    #Public /index
    index.exposed = True
    get_images.exposed = True
    images.exposed = True

#-------------------------------------------------------------
class Species_Url_Service_API(object):
    def index(self):
        return "Species_Url_Service API (Abu Saleh) : Find EOL links of species";

    #---------------------------------------------
    def get_links(self, **request_data):
        try:
            sp_lst = str(request_data['species']).strip();
            specieslist = sp_lst.split('|')
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = species_to_url_service_EOL.get_eolurls_species(specieslist)   
        
        return service_result;

 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def links(self,**request_data):
        try:
            input_json = cherrypy.request.json
            species_list = input_json["species"]
           				 
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        service_result = species_to_url_service_EOL.get_eolurls_species(species_list, True)   
           
        return service_result;
 	#------------------------------------------------
    #Public /index
    index.exposed = True
    get_links.exposed = True
    links.exposed = True


#--------------------------------------------------------------
class Find_ScientificNames_Service_API(object):
    def index(self):
        return "Find_ScientificNames_Service API (Abu Saleh) : Find Scientific names from Url, Text, Files";
    #---------------------------------------------
    def names_url(self,url=None,engine=0):
        try:
            #url = str(request_data['url']).strip();
            if url == None:
               return return_response_error(400,"error","Missing parameter url","JSON")
            else: 
               url = url.strip()
        except Exception, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        
        service_result = extract_names_service.extract_names_URL(url, engine)   
        #-------------log request------------------
        result_json = json.loads(service_result)
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
        insert_log(log)
        #------------------------------------------   

        return service_result;
    #------------------------------------------------
    def names_text(self,text=None,engine=0):
        try:
            #text = str(request_data['text']).strip();
            if text == None:
               return return_response_error(400,"error","Missing parameter text","JSON")
            else: 
               text = text.strip()
        except Exception, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        
        service_result = extract_names_service.extract_names_TEXT(text, engine)
        #-------------log request------------------   
        result_json = json.loads(service_result)
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
        insert_log(log)
        #------------------------------------------
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
        except Exception, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        
        service_result = resolve_names_service.resolve_names_OT(nameslist, False, False, False)   
        #-------------log request------------------   
        result_json = json.loads(service_result)
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
        insert_log(log)
        #------------------------------------------
        return service_result;
    #------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def names(self,**request_data):
        try:
            input_json = cherrypy.request.json
            nameslist = input_json["scientificNames"]
 	    
        except Exception, e:
            return return_response_error(400,"Error:" + str(e), "NotJSON")
        
        service_result = resolve_names_service.resolve_names_OT(nameslist, False, False, True)   
        #-------------log request------------------   
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'scientificNames': nameslist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
        insert_log(log)
        #------------------------------------------
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
        except Exception, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        
        service_result = resolve_names_service.resolve_names_GNR(nameslist)   
        #-------------log request------------------   
        result_json = json.loads(service_result)
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
        insert_log(log)
        #------------------------------------------
        return service_result;
    #------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def names(self,**request_data):
        try:
            input_json = cherrypy.request.json
            nameslist = input_json["scientificNames"]
 	    
        except Exception, e:
            return return_response_error(400,"Error:" + str(e), "NotJSON")
        
        service_result = resolve_names_service.resolve_names_GNR(nameslist, True)   
        #-------------log request------------------
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'scientificNames': nameslist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
        insert_log(log)
        #------------------------------------------
        return service_result;

    #Public /index
    index.exposed = True
    resolve.exposed = True
    names.exposed = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Get_Tree_OpenTree_Service_API(object):
    def index(self):
        return "Get_Tree_OpenTree_Service_API API (Abu Saleh) : Get Induced Subtree from OpenTree";
    #---------------------------------------------
    def get_tree(self,**request_data):
        try:
            taxa = str(request_data['taxa']).strip();
            taxalist = taxa.split('|')
        except Exception, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        
        nameslist_json = resolve_names_service.resolve_names_OT(taxalist, False, False, True)
        nameslist = nameslist_json["resolvedNames"]
        service_result = get_tree_service.get_tree_OT(nameslist)   
        #-------------log request------------------   
        result_json = json.loads(service_result)
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
        insert_log(log)
        #------------------------------------------
        return service_result;
    #------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tree(self,**request_data):
        try:
            input_json = cherrypy.request.json
            nameslist = input_json["resolvedNames"]
 	    
        except Exception, e:
            return return_response_error(400,"Error:" + str(e), "NotJSON")
        
        service_result = get_tree_service.get_tree_OT(nameslist, True)   
        #-------------log request------------------   
        header = cherrypy.request.headers
        log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'resolvedNames': nameslist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
        insert_log(log)
        #------------------------------------------
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
    #print "Thu ran CORS"
    conn = connect_mongodb() 
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
    cherrypy.tree.mount(Taxon_Genome_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group1), "ncbi"), conf_thanhnh)
    cherrypy.tree.mount(Taxon_to_Species_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group1)), conf_thanhnh)
    cherrypy.tree.mount(Species_Image_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group5), "eol"),conf_thanhnh)
    cherrypy.tree.mount(Species_Url_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group6), "eol"),conf_thanhnh)

    cherrypy.tree.mount(Find_ScientificNames_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group2)), conf_thanhnh )
    cherrypy.tree.mount(Resolve_ScientificNames_OpenTree_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group3),"ot"),conf_thanhnh )
    cherrypy.tree.mount(Resolve_ScientificNames_GNR_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group3),"gnr"), conf_thanhnh )
    cherrypy.tree.mount(Get_Tree_OpenTree_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group4),"ot"),conf_thanhnh )

    cherrypy.engine.start()
    cherrypy.engine.block()
