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
import pymongo
import datetime 
import types

from cherrypy import tools
from str2bool import str2bool

from support import taxon_to_species_service_OpenTree
from support import extract_names_service
from support import resolve_names_service
from support import opentree_tree_service
from support import phylomatic_tree_service
from support import phyloT_tree_service
from support import species_to_image_service_EOL
from support import species_to_url_service_EOL
from support import taxon_genome_species_service_NCBI
from support import services_helper

from __builtin__ import True

#==============================================================
logDbName = "WSLog"
logCollectionName = "log"
conn = None

WebService_Group1 = "ts"
WebService_Group2 = "fn"
WebService_Group3 = "tnrs"
WebService_Group4 = "gt"
WebService_Group5 = "si"
WebService_Group6 = "sl"
WebService_Group7 = "cs"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
HOST = "phylo.cs.nmsu.edu"  #"127.0.0.1"
PORT = "5051"
#PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
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


#-------------------------------------------
class CustomException(Exception):
    pass
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

#===============================Taxon_Genome_Service=================================    
class Taxon_Genome_Service_API(object):
    def index(self):
        return "Taxon_Genome_Service_API: Find species (of a taxon) that have genome sequence in NCBI";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def genome_species(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            taxonName = str(request_data['taxon']).strip()
            if len(request_data) > 1:
               raise CustomException("extra unknown parameter is not supported")

            if len(taxonName) == 0: 
               raise CustomException("'taxon' parameter must have a valid value")
            
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")    
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = taxon_genome_species_service_NCBI.get_genome_species(taxonName)   
            #-------------log request------------------
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("====TaxonGenomeError=====", traceback=True)

            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

 	#------------------------------------------------
    #Public /index
    index.exposed = True
    genome_species.exposed = True

#===========================Taxon_to_Species_Service===============================
class Taxon_to_Species_Service_API(object):
    def index(self):
        return "Taxon_to_Species_Service API: Get Species from Taxon";
    
    #----------------------------------------------
    @cherrypy.tools.json_out()
    def all_species(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            taxon = str(request_data['taxon']).strip()
            if len(request_data) > 1:
               raise CustomException("extra unknown parameter is not supported")
            if len(taxon) == 0: 
               raise CustomException("'taxon' parameter must have a valid value")
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = taxon_to_species_service_OpenTree.get_all_species(taxon)   
            #-------------log request------------------
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====TaxonAllSpeciesError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @cherrypy.tools.json_out()
    def country_species(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            taxon = str(request_data['taxon']).strip()
            country = str(request_data['country']).strip()
            if len(request_data) > 2:
               raise CustomException("extra unknown parameter is not supported")

            if len(taxon) == 0: 
               raise CustomException("'taxon' parameter must have a valid value")
            if len(country) == 0: 
               raise CustomException("'country' parameter must have a valid value")
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

        try:
            service_result = taxon_to_species_service_OpenTree.get_country_species(taxon, country)   
            #-------------log request------------------
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====TaxonCountrySpeciesError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
    #-------------------------------------------------------------    
    #Public /index
    index.exposed = True
    all_species.exposed = True
    country_species.exposed = True

#============================Species_Image_Service=============================
class Species_Image_Service_API(object):
    def index(self):
        return "Species_Image_Service API : Find images of species";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_images(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            sp_lst = str(request_data['species']).strip()
            specieslist = sp_lst.split('|')
            
            if len(specieslist) == 1 and '' in specieslist: 
               raise CustomException("'species' parameter must have a valid value")
            if len(specieslist) > 30: 
               return return_response_error(403,"Error: Currently more than 30 species is not supported","JSON")
            
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = species_to_image_service_EOL.get_images_species(specieslist)   
            #-------------log request------------------
            #result_json = json.loads(service_result)
            result_json = service_result

            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====SpeciesGetImageError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #------------------------------------------------
    def get_image(self, species_id=None):
        if species_id is None:
            return return_response_error(400,"Error: Missing parameter 'species_id'", "JSON")
        
        try:
            service_result = species_to_image_service_EOL.get_image_species_id(int(species_id))
            result_json = json.loads(service_result)
            #-------------log request------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
        #------------------------------------------
            return service_result

        except Exception, e:
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
            if type(species_list) != types.ListType:
               return return_response_error(400,"Error: 'species' parameter must be of list type","JSON")

            if len(species_list) == 0: 
               raise CustomException("'species' parameter must have a valid value")
            if len(species_list) > 30: 
               return return_response_error(403,"Error: Currently more than 30 species is not supported","JSON")
        
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = species_to_image_service_EOL.get_images_species(species_list, True)
            result_json = service_result   
            #-------------log request------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'species':species_list}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------   
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
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
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            sp_lst = str(request_data['species']).strip();
            species_list = sp_lst.split('|')
            
            if len(species_list) == 1 and '' in species_list: 
               raise CustomException("'species' parameter must have a valid value")
            if len(species_list) > 50: 
               return return_response_error(403,"Error: Currently more than 50 species is not supported","JSON")
            
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = species_to_url_service_EOL.get_eolurls_species(species_list)   
            #-------------log request------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'species':species_list}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------   
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
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
            if type(species_list) != types.ListType:
               return return_response_error(400,"Error: 'species' parameter must be of list type","JSON")

            if len(species_list) == 0: 
               raise CustomException("'species' parameter must have a valid value")
            if len(species_list) > 30: 
               return return_response_error(403,"Error: Currently more than 30 species is not supported","JSON")   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = species_to_url_service_EOL.get_eolurls_species(species_list, True)   
            #-------------log request------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'species':species_list}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------           
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====SpeciesPostLinkError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")   
        
 	#------------------------------------------------
    #Public /index
    index.exposed = True
    get_links.exposed = True
    links.exposed = True


#===========================Find_ScientificNames_Service_GNRD=============================
class Find_ScientificNames_Service_API(object):
    def index(self):
        return "Find_ScientificNames_GNRD_Service API: Find Scientific names from Url, Text, Files using GNRD";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def names_url(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            url = str(request_data['url']).strip()
            if len(url) == 0:
               raise CustomException("'url' parameter must have a valid value")
            if request_data is not None and 'engine' in request_data:
               engine = str(request_data['engine']).strip()
               if engine not in ['0', '1', '2']:
                  return return_response_error(400,"Error: 'engine' parameter must have a valid value","JSON") 
            else:
               engine = '0'
            if not services_helper.is_http_url(url):
               raise CustomException("'url' parameter must have a valid value")
            if not services_helper.does_url_exist(url):
               raise CustomException("'url' parameter must have a valid value")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = extract_names_service.extract_names_URL(url, int(engine))   
            #-------------log request------------------
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------   
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====NamesURLError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #------------------------------------------------
    @cherrypy.tools.json_out()
    def names_text(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            text = str(request_data['text']).strip()
            
            if len(text) == 0:
               raise CustomException("'text' parameter must have a valid value")
            if request_data is not None and 'engine' in request_data:
               engine = str(request_data['engine']).strip()
               if engine not in ['0', '1', '2']:
                  return return_response_error(400,"Error: 'engine' parameter must have a valid value","JSON") 
            else:
               engine = '0'

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = extract_names_service.extract_names_TEXT(text, int(engine))
            #-------------log request------------------   
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====NamesTextError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")   

    #------------------------------------------------
    @cherrypy.tools.json_out()
    def names_file(self, inputFile=None, engine='0'):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")
            
            file_size = 0
            allData = ''
            while True:
                data = inputFile.file.read(8192)
                allData += data
                if not data:
                   break
                file_size += len(data)
            if file_size == 0:
               raise CustomException("Input file cannot be empty")

            saved_dir_loc = "/var/www/upload/html/"
            file_loc = saved_dir_loc+inputFile.filename
            savedFile=open(file_loc, 'wb')
            savedFile.write(allData)
            savedFile.close()
            file_url = "http://phylo.cs.nmsu.edu:8888/"+inputFile.filename
            content_type = inputFile.content_type
            #print content_type
            new_filename = inputFile.filename
            contype = cherrypy.request.headers.get("Content-Encoding")
            
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = extract_names_service.extract_names_URL(file_url, int(engine))   
            #-------------log request------------------
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'engine': engine, 'file_name': new_filename}, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------   
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====NamesFileError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
    #------------------------------------------------
    #Public /index
    index.exposed = True
    names_url.exposed = True
    names_text.exposed = True
    names_file.exposed = True


#===========================Find_ScientificNames_Service_TaxonFinder=============================
class Find_ScientificNames_TaxonFinder_Service_API(object):
    def index(self):
        return "Find_ScientificNames_TaxonFinder_Service API: Find Scientific names from Url, Text using TaxonFinder";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def names_url(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            url = str(request_data['url']).strip()
            if len(url) == 0:
               raise CustomException("'url' parameter must have a valid value")

            if not services_helper.is_http_url(url):
               raise CustomException("'url' parameter must have a valid value")
            if not services_helper.does_url_exist(url):
               raise CustomException("'url' parameter must have a valid value")

            
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = extract_names_service.extract_names_taxonfinder(url, 'url')   
            #-------------log request------------------
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------   
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====TaxonFinderNamesURLError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #------------------------------------------------
    @cherrypy.tools.json_out()
    def names_text(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            text = str(request_data['text']).strip()
            
            if len(text) == 0:
               raise CustomException("'text' parameter must have a valid value")
            
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = extract_names_service.extract_names_taxonfinder(text, 'text')
            #-------------log request------------------   
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====TaxonFinderNamesTextError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")   
       
    #------------------------------------------------------
    #Public /index
    index.exposed = True
    names_url.exposed = True
    names_text.exposed = True


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
            
            if len(nameslist) > 1000: 
               return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = resolve_names_service.resolve_names_OT(nameslist, match_type, multi_match)   
            #-------------log request------------------   
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
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

            if len(nameslist) > 1000: 
               return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")
   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = resolve_names_service.resolve_names_OT(nameslist, match_type, multi_match)   
            #-------------log request------------------   
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'scientific_names': nameslist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------
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
            
            if len(nameslist) > 1000: 
               return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            service_result = resolve_names_service.resolve_names_GNR(nameslist, match_type, multi_match)   
            #-------------log request------------------   
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
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
               
            if len(nameslist) > 1000: 
               return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")
   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = resolve_names_service.resolve_names_GNR(nameslist, match_type, multi_match)   
            #-------------log request------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'scientific_names': nameslist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------
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
            #-------------log request------------------   
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
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
            #-------------log request------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'scientific_names': nameslist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------
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


#===============================Get_Tree_OpenTree_Service==========================
class Get_Tree_OpenTree_Service_API(object):
    def index(self):
        return "Get_Tree_OpenTree_Service API: Get Induced Subtree from Open Tree of Life";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            taxa = str(request_data['taxa']).strip();
            taxalist = taxa.split('|')

            if len(taxalist) == 1 and '' in taxalist: 
               raise CustomException("'taxa' parameter must have a valid value")

            if len(taxalist) > 1000: 
               return return_response_error(403,"Error: Currently more than 1000 taxa is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")
        
        try:
            nameslist_json = resolve_names_service.resolve_names_OT(taxalist, False, False)
            nameslist = nameslist_json["resolvedNames"]
            service_result = opentree_tree_service.get_tree_OT(nameslist)   
            #-------------log request------------------   
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====OToLTreeGetError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            
            if 'taxa' not in input_json and 'resolvedNames' not in input_json:
                raise KeyError("taxa")
            elif 'taxa' in input_json and 'resolvedNames' not in input_json:
                taxalist = input_json["taxa"]
                if type(taxalist) != types.ListType:
                   return return_response_error(400,"Error: 'taxa' parameter must be of list type","JSON")

                if len(taxalist) == 0 and 'resolvedNames' not in input_json: 
                   raise CustomException("'taxa' parameter must have a valid value")

                if len(taxalist) > 1000: 
                   return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")
   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            if 'resolvedNames' not in input_json: 
                nameslist_json = resolve_names_service.resolve_names_OT(taxalist, False, False)
                nameslist = nameslist_json['resolvedNames']
                if len(nameslist) > 1000: 
                   return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")
            else:
                nameslist = input_json['resolvedNames']
                taxalist = nameslist

            service_result = opentree_tree_service.get_tree_OT(nameslist)   
            #-------------log request------------------   
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'taxa': taxalist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====OToLTreePostError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

#--------------------------------------------------------------------
    #Public /index
    index.exposed = True
    get_tree.exposed = True
    tree.exposed = True

#=========================Get_Tree_Phylomatic_Service=============================
class Get_Tree_Phylomatic_Service_API(object):
    def index(self):
        return "Get_Tree_Phylomatic_Service_API : Get subtree from phylomatic";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            taxa = str(request_data['taxa']).strip();
            taxalist = taxa.split('|')

            if len(taxalist) == 1 and '' in taxalist: 
               raise CustomException("'taxa' parameter must have a valid value")

            if len(taxalist) > 1000: 
               return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")

        try:                
            service_result = phylomatic_tree_service.tree_controller(taxalist)   
            #-------------log request------------------   
            #result_json = json.loads(service_result)
            result_json = service_result

            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====PhylomaticTreeGetError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            if 'taxa' not in input_json and 'resolvedNames' not in input_json:
                raise KeyError("taxa")
            elif 'taxa' in input_json and 'resolvedNames' not in input_json:
                taxalist = input_json["taxa"]
                if type(taxalist) != types.ListType:
                   return return_response_error(400,"Error: 'taxa' parameter must be of list type","JSON")

                if len(taxalist) == 0 and 'resolvedNames' not in input_json: 
                   raise CustomException("'taxa' parameter must have a valid value")

                if len(taxalist) > 1000: 
                   return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON") 
  				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            if 'resolvedNames' not in input_json: 
                nameslist_json = resolve_names_service.resolve_names_OT(taxalist, False, False)
                nameslist = nameslist_json['resolvedNames']
                if len(nameslist) > 1000: 
                   return return_response_error(403,"Error: Currently more than 1000 names is not supported","JSON")
            else:
                nameslist = input_json['resolvedNames']
                taxalist = phylomatic_tree_service.retrieve_taxa(nameslist)

            service_result = phylomatic_tree_service.tree_controller(taxalist)   
            #-------------log request------------------   
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'taxa': taxalist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====PhylomaticTreePostError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #--------------------------------------------------------------

    #Public /index
    index.exposed = True
    get_tree.exposed = True
    tree.exposed = True


#===========================Get_Tree_PhyloT_Service (Currently Obsolete)================================
'''
class Get_Tree_PhyloT_Service_API(object):
    def index(self):
        return "Get_Tree_PhyloT_Service_API : Get tree from phyloT";
    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET', 'POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET or POST are not allowed","JSON")

            taxa = str(request_data['taxa']).strip();
            taxalist = taxa.split('|')

            if len(taxalist) == 1 and '' in taxalist: 
               raise CustomException("'taxa' parameter must have a valid value")

            if len(taxalist) > 30: 
               return return_response_error(403,"Error: Currently more than 30 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)),"JSON")

        try:
            service_result = phyloT_tree_service.service_controller(taxalist)   
            #-------------log request------------------   
            #result_json = json.loads(service_result)
            result_json = service_result
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': result_json['status_code']}
            insert_log(log)
            #------------------------------------------
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====PhyloTTreeError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            taxalist = input_json["taxa"]
            if type(taxalist) != types.ListType:
               return return_response_error(400,"Error: 'taxa' parameter must be of list type","JSON")
 	    
            if len(taxalist) == 0: 
               raise CustomException("'taxa' parameter must have a valid value")

            if len(taxalist) > 30: 
               return return_response_error(403,"Error: Currently more than 30 names is not supported","JSON")
   				 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")     
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

        try:
            service_result = phyloT_tree_service.service_controller(taxalist)   
            #-------------log request------------------   
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'taxa': taxalist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
        #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("=====PhyloTTreeError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------------------
    #Public /index
    index.exposed = True
    get_tree.exposed = True
    tree.exposed = True

'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CORS():
    #print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    conn = connect_mongodb() 
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({#'server.socket_host': HOST, #'0.0.0.0' "127.0.0.1",
                            'server.socket_port': int(PORT),
                            'tools.proxy.on': True,
                            'tools.proxy.base': 'http://'+HOST,
                            'log.error_file':ERROR_LOG_CHERRYPY,
                            'log.access_file':ACCESS_LOG_CHERRYPY,
                            'tools.log_tracebacks.on': True
                          })
    #cherrypy.config.update({'error_page.404': error_page_404})
    conf_app = {
             '/':{
                'tools.CORS.on': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'request.show_tracebacks': False
                #'request.show_tracebacks': True,
                #'error_page.500': error_page_500
             }
    }
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

    #Starting Server
    cherrypy.tree.mount(Taxon_Genome_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group1), "ncbi"), conf_app)
    cherrypy.tree.mount(Taxon_to_Species_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group1)), conf_app)
    cherrypy.tree.mount(Species_Image_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group5), "eol"), conf_app)
    cherrypy.tree.mount(Species_Url_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group6), "eol"), conf_app)

    cherrypy.tree.mount(Find_ScientificNames_Service_API(), '/%s/%s' %(str(WS_NAME),str(WebService_Group2)), conf_app)
    cherrypy.tree.mount(Find_ScientificNames_TaxonFinder_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group2), "tf"), conf_app)

    cherrypy.tree.mount(Resolve_ScientificNames_OpenTree_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group3),"ot"), conf_app)
    cherrypy.tree.mount(Resolve_ScientificNames_GNR_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group3),"gnr"), conf_app)
    cherrypy.tree.mount(Resolve_ScientificNames_iPLant_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group3),"ip"), conf_app)

    cherrypy.tree.mount(Get_Tree_OpenTree_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group4),"ot"), conf_app)
    cherrypy.tree.mount(Get_Tree_Phylomatic_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group4),"pm"), conf_app)
    
    #cherrypy.tree.mount(Get_Tree_PhyloT_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group4),"pt"), conf_app)

    
    cherrypy.engine.start()
    cherrypy.engine.block()
