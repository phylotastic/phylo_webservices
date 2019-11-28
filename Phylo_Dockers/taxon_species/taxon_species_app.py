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

from service import taxon_to_species_service_OpenTree
from service import taxon_genome_species_service_NCBI
from service import popularity_service

#==============================================================

WebService_Group = "ts"

WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
HOST = "0.0.0.0" #"127.0.0.1" "phylo.cs.nmsu.edu"
PORT = "5053"

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
       
#-------------------------------------------
class CustomException(Exception):
    pass

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
            
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")    
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = taxon_genome_species_service_NCBI.get_genome_species(taxonName)   
            result_json = service_result
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception as e:
            cherrypy.log("====TaxonGenomeError=====", traceback=True)

            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

 	#------------------------------------------------
    #Public /index
    index.exposed = True
    genome_species.exposed = True

#========================================================
class Popularity_Service_API(object):

    def index(self):
        return "Popularity_Service API: Get popular species of a particular taxon using OneZoom API"
    #------------------------------------------------------
    @cherrypy.tools.json_out()
    def popular_species(self,**request_data):
        try:
            http_method = cherrypy.request.method
            if http_method not in ['GET']:
               return return_response_error(405,"Error: HTTP Methods other than GET are not allowed","JSON")

            if request_data is not None and 'taxon' in request_data:
               taxon = str(request_data['taxon']).strip()
               if len(taxon) == 0: 
                  raise CustomException("'taxon' parameter must have a valid value")
            else:
               taxon = None

            if request_data is not None and 'num_species' in request_data:
                num_species = int(request_data['num_species'].strip())
                if num_species > 100:
                   raise CustomException("Maximum value allowed for 'num_species' parameter is 100")
                #print num_species
            else: 
                num_species = 20

        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            if taxon is None:
               service_result = popularity_service.get_popular_species()
            else:
               service_result = popularity_service.get_popular_species(taxon, num_species)
            #------------------------------------------
            if service_result['status_code'] == 200:
               return service_result
            else:
               return return_response_error(service_result['status_code'], service_result['message'], "JSON")

        except Exception as e:
            cherrypy.log("====PopularityServiceError====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
 	
 	#------------------------------------------------
    index.exposed = True	
    popular_species.exposed = True

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
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        try:
            service_result = taxon_to_species_service_OpenTree.get_all_species(taxon)   
            result_json = service_result
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception as e:
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
        except KeyError as e:
            return return_response_error(400,"Error: Missing parameter %s"%(str(e)),"JSON")
        except CustomException as e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")   
        except Exception as e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

        try:
            service_result = taxon_to_species_service_OpenTree.get_country_species(taxon, country)   
            result_json = service_result
            if result_json['status_code'] == 200:
               return service_result
            else:
               return return_response_error(result_json['status_code'], result_json['message'], "JSON")

        except Exception as e:
            cherrypy.log("=====TaxonCountrySpeciesError=====", traceback=True)
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
    #-------------------------------------------------------------    
    #Public /index
    index.exposed = True
    all_species.exposed = True
    country_species.exposed = True


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CORS():
    #print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({'server.socket_host': HOST, 
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
                'error_page.500': error_page_500,
                'request.show_tracebacks': True
             }
    }
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

    #Mounting Services
    cherrypy.tree.mount(Taxon_Genome_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group), "ncbi"), conf_app)
    cherrypy.tree.mount(Taxon_to_Species_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group), "ot"), conf_app)
    cherrypy.tree.mount(Popularity_Service_API(), '/%s/%s/%s' %(str(WS_NAME),str(WebService_Group), "oz"), conf_app )

    #Starting Server
    cherrypy.engine.start()
    cherrypy.engine.block()
