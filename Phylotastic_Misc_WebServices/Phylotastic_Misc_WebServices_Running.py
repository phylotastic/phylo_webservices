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

from support import compare_trees_service
from support import tree_studies_service
from support import compound_service_tree
#--------------------------------------------------
logDbName = "WSLog"
logCollectionName = "log"
conn = None


WS_NAME = "phylotastic_ws"
WS_GROUP1 = "md" #metadata service
WS_GROUP2 = "ts" #taxon_to_species service
WS_GROUP3 = "cp" #compound service

ROOT_FOLDER = os.getcwd()
HOST = "phylo.cs.nmsu.edu"  #"127.0.0.1"
PORT = "5006"

#PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY = ROOT_FOLDER + "/log/%s_access_log.log" %(PORT+"_"+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY = ROOT_FOLDER + "/log/%s_error_log.log" %(PORT+"_"+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


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

#--------------------------------------------------------------
class ConversionException(Exception):
    pass
    
#-------------------------------------------------------------
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

#=======================================================================
class Tree_Studies_Service_API(object):
    def index(self):
        return "Tree_Studies_Service API : Find supported studies of an induced tree from OpenTreeOfLife";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_studies(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET','POST']:
               return return_response_error(405,"Error: HTTP Methods other than GET and POST are not allowed","JSON")

            lst = str(request_data['list']).strip()
            list_type = str(request_data['list_type']).strip()
            lst = lst.split('|')

            if len(lst) == 1 and '' in lst: 
               raise CustomException("'list' parameter must have a valid value")
            if len(list_type) == 0: 
               raise CustomException("'list_type' parameter must have a valid value")
  
            if list_type.lower() == "ottids":
               ottid_lst = []
               for s in lst:
                   s = s.strip()
                   if s.isdigit():
                      ottid_lst.append(int(s))
                   else:
                      raise ConversionException("ottids are not numeric. If list_type parameter is 'ottids', then the list parameter must contain numeric values")
               
            elif list_type.lower() == "taxa":
                 taxa_lst = [s.strip() for s in lst] 
            else:
                 raise ConversionException("'%s' is not a valid value for 'list_type' parameter"%(list_type))
          
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except ConversionException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           if list_type.lower() == "ottids":
              service_result = tree_studies_service.get_studies_from_ids(ottid_lst) 
           elif list_type.lower() == "taxa":
              service_result = tree_studies_service.get_studies_from_names(taxa_lst)
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
            cherrypy.log("====TreeStudiesError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def studies(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            lst = input_json["list"]
            list_type = input_json["list_type"]
            if list_type.lower() == "ottids":
               ott_id_lst = lst
            elif list_type.lower() == "studyids":
               study_id_lst = lst
            elif list_type.lower() == "taxa":
               taxa_lst = lst 
            else:
               raise ConversionException("'%s' is not a valid value for 'list_type' parameter"%(list_type))
          
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except ConversionException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            if list_type.lower() == "ottids":
               service_result = tree_studies_service.get_studies_from_ids(ott_id_lst)
            elif list_type.lower() == "studyids":
               service_result = tree_studies_service.get_studies_from_ids(study_id_lst, False)  
            elif list_type.lower() == "taxa":
               service_result = tree_studies_service.get_studies_from_names(taxa_lst) 
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'list_type': list_type, 'list': lst}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====TreeStudiesError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_study_info(self, **request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET and POST are not allowed","JSON")

            study_id_lst = str(request_data['study_ids']).strip()
            study_id_lst = study_id_lst.split('|')

            if len(study_id_lst) == 1 and '' in study_id_lst: 
               raise CustomException("'study_ids' parameter must have a valid value")
            
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except ConversionException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
           service_result = tree_studies_service.get_studies(study_id_lst) 
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
            cherrypy.log("====TreeStudiesGetInfoError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    
 	#-----------------------------------------------	
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def study_info(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            study_id_lst = input_json["study_ids"]
            
        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except ConversionException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            service_result = tree_studies_service.get_studies(study_id_lst)  
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'study_ids': study_id_lst}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====TreeStudiesInfoError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    get_studies.exposed = True
    studies.exposed = True
    study_info = True
    get_study_info = True

#----------------------------------------------------------
class Compound_Service_Tree_API(object):
    def index(self):
        return "Compound_Service_Tree_API : Get tree combining multiple services"

    #---------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def tree(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST','OPTIONS']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            lst = input_json["list"]
            list_type = input_json["list_type"]
            if list_type.lower() == "common":
               common_lst = lst
               source = "NCBI"
            elif list_type.lower() == "scientific":
               scientific_lst = lst
               source = "GNR"
            else:
               raise ConversionException("'%s' is not a valid value for 'list_type' parameter"%(list_type))

            if 'source' in input_json:
               source = input_json['source']
               if list_type.lower() == "scientific" and source not in ["NCBI", "EOL", "GNR"]:
                  return return_response_error(403,"Error: Invalid source parameter value","JSON")
               elif list_type.lower() == "common" and source not in ["NCBI", "ITIS", "EBI", "TROPICOS"]:
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
        except ConversionException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try: 
            if list_type.lower() == "common":
               #return {'status_code': 500, 'message': "Service under construction"}
               service_result = compound_service_tree.get_tree_com_names(common_lst, source, multiple)
            elif list_type.lower() == "scientific":
               service_result = compound_service_tree.get_tree_sc_names(scientific_lst, source, multiple)  
            
            #--------------------------------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'list_type': list_type, 'list': lst}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
 
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====CompoundServiceTreeError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

    #-----------------------------------------------------
    #Public /index
    index.exposed = True
    tree.exposed = True	

#============================================================
class Compare_Trees_Service_API(object):

    def index(self):
        return "Compare_Trees_Service API: Compare two phylogenetic trees"
    #------------------------------------------------------
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def compare_trees(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['POST']:
               return return_response_error(405,"Error: HTTP Methods other than POST are not allowed","JSON")

            input_json = cherrypy.request.json
            tree1_str = input_json["tree1_nwk"]
            tree2_str = input_json["tree2_nwk"]

            if len(tree1_str) == 0: 
               raise CustomException("'tree1_nwk' parameter must have a valid value")
            if len(tree2_str) == 0: 
               raise CustomException("'tree2_nwk' parameter must have a valid value")

        except KeyError, e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
 
        try:
            service_result = compare_trees_service.compare_trees(tree1_str, tree2_str)
            #---------------log-------------------
            header = cherrypy.request.headers
            log = {'client_ip': cherrypy.request.remote.ip, 'date': datetime.datetime.now(), 'request_base': cherrypy.request.base, 'request_script': cherrypy.request.script_name, 'request_path': cherrypy.request.path_info, 'method': cherrypy.request.method, 'params': {'tree1_nwk': tree1_str, 'tree2_nwk': tree2_str}, 'user_agent': header['User-Agent'], 'response_status': service_result['status_code']}
            insert_log(log)
            #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception, e:
            cherrypy.log("====CompareTreeError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
 	
 	#------------------------------------------------
    index.exposed = True	
    compare_trees.exposed = True

#-----------------------------------------------------------
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
    cherrypy.config.update({#'server.socket_host': HOST, #'0.0.0.0' "127.0.0.1",
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
                'error_page.400': error_page_400
                #'error_page.500': error_page_500,
                #'request.show_tracebacks': True
                
             }
    }
    
    #Starting Server
    cherrypy.tree.mount(Tree_Studies_Service_API(), '/%s/%s' %(str(WS_NAME),str(WS_GROUP1)), conf_CORS )
    cherrypy.tree.mount(Compare_Trees_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP1), "dp"), conf_CORS )
    cherrypy.tree.mount(Compound_Service_Tree_API(), '/%s/%s/%s' %(str(WS_NAME),str(WS_GROUP3), "gt"), conf_CORS )
    
    cherrypy.engine.start()
    cherrypy.engine.block()
