import cherrypy
import time
import datetime
import json
import os
import sys
import collections
import pymongo
import types

from cherrypy import tools
from str2bool import str2bool

from support import habitat_conservation_service_EOL
from support import conservation_service_ECOS
from support import common_name_species_service_NCBI
from support import common_name_species_service_ITIS
from support import common_name_species_service_TROPICOS
from support import common_name_species_service_EBI

from support import scientific_to_common_name_NCBI
from support import scientific_to_common_name_EOL
from support import scientific_to_common_name_GNR
from support import tree_common_names
#----------------------------------------------------------

logDbName = "WSLog"
logCollectionName = "log"
conn = None


WS_NAME = "phylotastic_ws"
WS_GROUP1 = "sd" #species data service
WS_GROUP2 = "cs" #common name service
WS_GROUP3 = "ss"  #scientific name service
WS_GROUP4 = "tc"  #tree to scientific name service

ROOT_FOLDER = os.getcwd()
HOST = "phylo.cs.nmsu.edu"  #"127.0.0.1"
PORT = "5013"


#PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
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

#-----------------------------------------------------------
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
    insert_status = log_collection.insert_one(log_msg)


#=======================================================================
class Habitat_Conservation_EOL_Service_API(object):
    def index(self):
        return "Habitat_Conservation_EOL_Service_API : Get habitat and conservation status of species using EOL API"

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_habitat_conservation(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET and POST are not allowed","JSON")

            sp_lst = str(request_data['species']).strip()
            sp_lst = sp_lst.split('|')

            if len(sp_lst) == 1 and '' in sp_lst: 
               raise CustomException("'species' parameter must have a valid value")

            if len(sp_lst) > 30: 
               return return_response_error(403, "Error: Currently more than 30 names is not supported","JSON")            

            
            
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           service_result = habitat_conservation_service_EOL.get_habitat_conservation(sp_lst)
           #-------------------------------------------
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #---------------------------------------------
           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====HabitatConservation_EOL_GET_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def habitat_conservation(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            taxalist = input_json["species"]
            if type(taxalist) != types.ListType:
               return return_response_error(400,"Error: 'species' parameter must be of list type","JSON")
            if len(taxalist) > 30: 
               return return_response_error(403, "Error: Currently more than 30 names is not supported","JSON")            

    
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            service_result = habitat_conservation_service_EOL.get_habitat_conservation(taxalist) 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'species': taxalist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====HabitatConservation_EOL_POST_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_habitat_conservation.exposed = True
    habitat_conservation.exposed = True

#==================================Conservation status Service: ECOS===============================
class Conservation_ECOS_Service_API(object):
    def index(self):
        return "Conservation_ECOS_Service_API : Get conservation status of species using ECOS services"

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_conservation(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET and POST are not allowed","JSON")

            sp_lst = str(request_data['species']).strip()
            sp_lst = sp_lst.split('|')

            if len(sp_lst) == 1 and '' in sp_lst: 
               raise CustomException("'species' parameter must have a valid value")
            
            if len(sp_lst) > 30: 
               return return_response_error(403, "Error: Currently more than 30 names is not supported","JSON")            

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           service_result = conservation_service_ECOS.get_conservation(sp_lst)
           #-------------------------------------------
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #---------------------------------------------
           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====Conservation_ECOS_GET_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def conservation(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            taxalist = input_json["species"]
            if type(taxalist) != types.ListType:
               return return_response_error(400,"Error: 'species' parameter must be of list type","JSON")

            if len(taxalist) > 30: 
               return return_response_error(403,"Error: Currently more than 30 names is not supported","JSON")
    
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            service_result = conservation_service_ECOS.get_conservation(taxalist) 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'species': taxalist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====HabitatConservation_ECOS_POST_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_conservation.exposed = True
    conservation.exposed = True



#====================================Common Name Service: NCBI===================================
class Common_Name_Species_Service_NCBI_API(object):
    def index(self):
        return "Common_Name_Species_Service_NCBI_API : Get scientific names from common names using NCBI source";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_scientific_names(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET and POST are not allowed","JSON")

            name_lst = str(request_data['commonnames']).strip()
            name_lst = name_lst.split('|')

            if len(name_lst) == 1 and '' in name_lst: 
               raise CustomException("'commonnames' parameter must have a valid value")
            
            multi_match = False
            if request_data is not None and 'multiple_match' in request_data:
               multi_match = str(request_data['multiple_match']).strip()
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
            
            if len(name_lst) > 30: 
               return return_response_error(403,"Error: Currently more than 30 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           service_result = common_name_species_service_NCBI.get_scientific_names(name_lst, not multi_match)
           #-------------------------------------------
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #---------------------------------------------
           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====CommonName_NCBI_GET_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def scientific_names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            namelist = input_json["commonnames"]
            if type(namelist) != types.ListType:
               return return_response_error(400,"Error: 'commonnames' parameter must be of list type","JSON")

            multi_match = False
            if 'multiple_match' in input_json:
               multi_match = input_json['multiple_match']
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
    
            if len(namelist) > 30: 
               return return_response_error(403,"Error: Currently more than 30 names is not supported","JSON")
 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            service_result = common_name_species_service_NCBI.get_scientific_names(namelist, not multi_match) 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'commonnames': namelist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====CommonName_NCBI_POST_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_scientific_names.exposed = True
    scientific_names.exposed = True

#===================================Common Name Service: ITIS====================================
class Common_Name_Species_Service_ITIS_API(object):
    def index(self):
        return "Common_Name_Species_Service_ITIS_API : Get scientific names from common names using ITIS source";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_scientific_names(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET and POST are not allowed","JSON")

            name_lst = str(request_data['commonnames']).strip()
            name_lst = name_lst.split('|')

            if len(name_lst) == 1 and '' in name_lst: 
               raise CustomException("'commonnames' parameter must have a valid value")
            
            multi_match = False
            if request_data is not None and 'multiple_match' in request_data:
               multi_match = str(request_data['multiple_match']).strip()
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
            
            if len(name_lst) > 30: 
               return return_response_error(403,"Error: Currently more than 30 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           service_result = common_name_species_service_ITIS.get_scientific_names(name_lst, not multi_match)
           #-------------------------------------------
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #---------------------------------------------
           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====CommonName_ITIS_GET_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def scientific_names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            namelist = input_json["commonnames"]
            if type(namelist) != types.ListType:
               return return_response_error(400,"Error: 'commonnames' parameter must be of list type","JSON")

            multi_match = False
            if 'multiple_match' in input_json:
               multi_match = input_json['multiple_match']
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
    
            if len(namelist) > 30: 
               return return_response_error(403,"Error: Currently more than 30 names is not supported","JSON")
 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            service_result = common_name_species_service_ITIS.get_scientific_names(namelist, not multi_match) 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'commonnames': namelist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====CommonName_ITIS_POST_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_scientific_names.exposed = True
    scientific_names.exposed = True

#==================================Common Name Service: TROPICOS=======================================
class Common_Name_Species_Service_TROPICOS_API(object):
    def index(self):
        return "Common_Name_Species_Service_TROPICOS_API : Get scientific names from common names using TROPICOS source";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_scientific_names(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET and POST are not allowed","JSON")

            name_lst = str(request_data['commonnames']).strip()
            name_lst = name_lst.split('|')

            if len(name_lst) == 1 and '' in name_lst: 
               raise CustomException("'commonnames' parameter must have a valid value")
            
            multi_match = False
            if request_data is not None and 'multiple_match' in request_data:
               multi_match = str(request_data['multiple_match']).strip()
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
            
            if len(name_lst) > 30: 
               return return_response_error(403,"Error: Currently more than 30 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           service_result = common_name_species_service_TROPICOS.get_scientific_names(name_lst, not multi_match)
           #-------------------------------------------
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #---------------------------------------------
           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====CommonName_TROPICOS_GET_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def scientific_names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            namelist = input_json["commonnames"]
            if type(namelist) != types.ListType:
               return return_response_error(400,"Error: 'commonnames' parameter must be of list type","JSON")

            multi_match = False
            if 'multiple_match' in input_json:
               multi_match = input_json['multiple_match']
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
    
            if len(namelist) > 30: 
               return return_response_error(403,"Error: Currently more than 30 names is not supported","JSON")
 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            service_result = common_name_species_service_TROPICOS.get_scientific_names(namelist, not multi_match) 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'commonnames': namelist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====CommonName_TROPICOS_POST_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_scientific_names.exposed = True
    scientific_names.exposed = True

#==================================Common Name Service: EBI=======================================
class Common_Name_Species_Service_EBI_API(object):
    def index(self):
        return "Common_Name_Species_Service_EBI_API : Get scientific names from common names using EBI source";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_scientific_names(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            name_lst = str(request_data['commonnames']).strip()
            name_lst = name_lst.split('|')

            if len(name_lst) == 1 and '' in name_lst: 
               raise CustomException("'commonnames' parameter must have a valid value")
            
            multi_match = False
            if request_data is not None and 'multiple_match' in request_data:
               multi_match = str(request_data['multiple_match']).strip()
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
            
            if len(name_lst) > 20: 
               return return_response_error(403,"Error: Currently more than 20 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           service_result = common_name_species_service_EBI.get_scientific_names(name_lst, not multi_match)
           #-------------------------------------------
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #---------------------------------------------
           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====CommonName_EBI_GET_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def scientific_names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            namelist = input_json["commonnames"]
            if type(namelist) != types.ListType:
               return return_response_error(400,"Error: 'commonnames' parameter must be of list type","JSON")

            multi_match = False
            if 'multiple_match' in input_json:
               multi_match = input_json['multiple_match']
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
    
            if len(namelist) > 20: 
               return return_response_error(403,"Error: Currently more than 20 names is not supported","JSON")
 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            service_result = common_name_species_service_EBI.get_scientific_names(namelist, not multi_match) 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'commonnames': namelist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====CommonName_EBI_POST_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_scientific_names.exposed = True
    scientific_names.exposed = True


#===================================Scientific Name Service: NCBI====================================
class Scientific_Name_Service_NCBI_API(object):
    def index(self):
        return "Scientific_Name_Service_NCBI_API : Get common names from scientific names using NCBI source";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_common_names(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            name_lst = str(request_data['scientific_names']).strip()
            name_lst = name_lst.split('|')

            if len(name_lst) == 1 and '' in name_lst: 
               raise CustomException("'scientific_names' parameter must have a valid value")
            
            multi_match = False
            if request_data is not None and 'multiple_match' in request_data:
               multi_match = str(request_data['multiple_match']).strip()
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
            
            if len(name_lst) > 50: 
               return return_response_error(403,"Error: Currently more than 50 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           service_result = scientific_to_common_name_NCBI.get_sci_to_comm_names(name_lst, not multi_match)
           #-------------------------------------------
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #---------------------------------------------
           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====ScientificName_NCBI_GET_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def common_names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            namelist = input_json["scientific_names"]
            if type(namelist) != types.ListType:
               return return_response_error(400,"Error: 'scientific_names' parameter must be of list type","JSON")

            multi_match = False
            if 'multiple_match' in input_json:
               multi_match = input_json['multiple_match']
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
    
            if len(namelist) > 50: 
               return return_response_error(403,"Error: Currently more than 50 names is not supported","JSON")
 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            service_result = scientific_to_common_name_NCBI.get_sci_to_comm_names(namelist, not multi_match) 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'scientific_names': namelist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====ScientificName_NCBI_POST_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_common_names.exposed = True
    common_names.exposed = True

#===================================Scientific Name Service: EOL====================================
class Scientific_Name_Service_EOL_API(object):
    def index(self):
        return "Scientific_Name_Service_EOL_API : Get common names from scientific names using EOL source";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_common_names(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            name_lst = str(request_data['scientific_names']).strip()
            name_lst = name_lst.split('|')

            if len(name_lst) == 1 and '' in name_lst: 
               raise CustomException("'scientific_names' parameter must have a valid value")
            
            multi_match = False
            if request_data is not None and 'multiple_match' in request_data:
               multi_match = str(request_data['multiple_match']).strip()
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
            
            if len(name_lst) > 50: 
               return return_response_error(403,"Error: Currently more than 50 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           #service_result = scientific_to_common_name_EOL.get_sci_to_comm_names(name_lst, not multi_match)
           service_result = scientific_to_common_name_EOL.get_sci_to_comm_names(name_lst)
           #-------------------------------------------
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #---------------------------------------------
           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====ScientificName_EOL_GET_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def common_names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            namelist = input_json["scientific_names"]
            if type(namelist) != types.ListType:
               return return_response_error(400,"Error: 'scientific_names' parameter must be of list type","JSON")

            multi_match = False
            if 'multiple_match' in input_json:
               multi_match = input_json['multiple_match']
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
    
            if len(namelist) > 50: 
               return return_response_error(403,"Error: Currently more than 50 names is not supported","JSON")
 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            #service_result = scientific_to_common_name_EOL.get_sci_to_comm_names(namelist, not multi_match) 
            service_result = scientific_to_common_name_EOL.get_sci_to_comm_names(namelist) 
 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'scientific_names': namelist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====ScientificName_EOL_POST_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_common_names.exposed = True
    common_names.exposed = True

#===================================Scientific Name Service: GNR====================================
class Scientific_Name_Service_GNR_API(object):
    def index(self):
        return "Scientific_Name_Service_GNR_API : Get common names from scientific names using GNR source";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_common_names(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            name_lst = str(request_data['scientific_names']).strip()
            name_lst = name_lst.split('|')

            if len(name_lst) == 1 and '' in name_lst: 
               raise CustomException("'scientific_names' parameter must have a valid value")
            
            multi_match = False
            if request_data is not None and 'multiple_match' in request_data:
               multi_match = str(request_data['multiple_match']).strip()
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
            
            if len(name_lst) > 100: 
               return return_response_error(403,"Error: Currently more than 100 names is not supported","JSON")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           #service_result = scientific_to_common_name_EOL.get_sci_to_comm_names(name_lst, not multi_match)
           service_result = scientific_to_common_name_GNR.get_sci_to_comm_names(name_lst)
           #-------------------------------------------
           header = cherrypy.request.headers
           log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': cherrypy.request.params, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
           insert_log(log)
           #---------------------------------------------
           if service_result['status_code'] == 200:
               return service_result
           else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====ScientificName_GNR_GET_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def common_names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            namelist = input_json["scientific_names"]
            if type(namelist) != types.ListType:
               return return_response_error(400,"Error: 'scientific_names' parameter must be of list type","JSON")

            multi_match = False
            if 'multiple_match' in input_json:
               multi_match = input_json['multiple_match']
               if type(multi_match) != types.BooleanType:
                  multi_match = str2bool(multi_match)
    
            if len(namelist) > 100: 
               return return_response_error(403,"Error: Currently more than 100 names is not supported","JSON")
 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            #service_result = scientific_to_common_name_EOL.get_sci_to_comm_names(namelist, not multi_match) 
            service_result = scientific_to_common_name_GNR.get_sci_to_comm_names(namelist) 
 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'scientific_names': namelist}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====ScientificName_GNR_POST_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_common_names.exposed = True
    common_names.exposed = True

#===================================Tree to Common Name Service====================================
class Tree_Common_Name_Service_API(object):
    def index(self):
        return "Tree_Common_Name_Service_API : Get common names from tips (species) of input tree";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def common_names(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            newick_str = input_json["newick_tree"]
            
            source = "GNR"
            if 'source' in input_json:
               source = input_json['source']
               if source not in ["NCBI", "EOL", "GNR"]:
                  return return_response_error(403,"Error: Invalid source parameter value","JSON")

            multiple = False
            if 'multiple' in input_json:
               multiple = input_json['multiple']
               if type(multiple) != types.BooleanType:
                  multiple = str2bool(multiple)
 
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            service_result = tree_common_names.get_common_name_tree(newick_str, source, multiple) 
 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'newick': newick_str}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====TreeCommonName_POST_Error====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    common_names.exposed = True
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def CORS():
    #print "Run CORS"
    #https://stackoverflow.com/questions/28049898/415-exception-cherrypy-webservice
    if cherrypy.request.method == 'OPTIONS':
       # preflight request 
       # see http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0
       cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
       cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
       cherrypy.response.headers['Access-Control-Allow-Origin']  = '*'
       # tell CherryPy no avoid normal handler
       return True
    else:
       cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
       cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    conn = connect_mongodb() 
    #cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    cherrypy.tools.CORS = cherrypy._cptools.HandlerTool(CORS)
    #Configure Server
    cherrypy.config.update({#'server.socket_host': '0.0.0.0',
                            'server.socket_port': int(PORT),
                            'tools.proxy.on': True,
                            'tools.proxy.base': 'https://'+HOST,
                            'log.error_file':ERROR_LOG_CHERRYPY,
                            'log.access_file':ACCESS_LOG_CHERRYPY,
                            'tools.log_tracebacks.on': True
                          })
    
    conf_CORS = {
             '/':{
                'tools.CORS.on': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'request.show_tracebacks': False
                }
    }
    
    #Starting Server
    #cherrypy.tree.mount(Habitat_Conservation_EOL_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP1), "eol"), conf_CORS )
    cherrypy.tree.mount(Conservation_ECOS_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP1), "ecos"), conf_CORS)
    cherrypy.tree.mount(Common_Name_Species_Service_NCBI_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP2),"ncbi"),conf_CORS )
    cherrypy.tree.mount(Common_Name_Species_Service_ITIS_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP2),"itis"),conf_CORS )
    cherrypy.tree.mount(Common_Name_Species_Service_TROPICOS_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP2),"tpcs"),conf_CORS )
    cherrypy.tree.mount(Common_Name_Species_Service_EBI_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP2),"ebi"),conf_CORS )

    cherrypy.tree.mount(Scientific_Name_Service_NCBI_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP3),"ncbi"),conf_CORS )
    cherrypy.tree.mount(Scientific_Name_Service_EOL_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP3),"eol"),conf_CORS )	
    cherrypy.tree.mount(Scientific_Name_Service_GNR_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP3),"gnr"),conf_CORS )		
    cherrypy.tree.mount(Tree_Common_Name_Service_API(), '/%s/%s' %(str(WS_NAME),str(WS_GROUP4)),conf_CORS )	       
    
    cherrypy.engine.start()
    cherrypy.engine.block()
