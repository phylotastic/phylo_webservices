import cherrypy
import time
import datetime
import json
import os
import sys
import collections

from cherrypy import tools

from database import DatabaseAPI
import qos_measure as qm

#-----------------------------------------------------------------
WS_NAME = "phylotastic_ws"
WS_GROUP1 = "qs" #metadata service

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5010"
PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
#============================================================================
ACCESS_LOG_CHERRYPY_5010 = ROOT_FOLDER + "/log/%s_5010_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5010 = ROOT_FOLDER + "/log/%s_5010_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))

#-----------------------------------------------------------------
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

#--------------------------------------------------------------
class CustomException(Exception):
    pass
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class QoS_Service_API(object):
    def index(self):
        return "QoS_Service API : Get QoS info of phylotastic services";

    #---------------------------------------------
    @cherrypy.tools.json_out()
    def get_serviceids(self, **request_data):
        service_result = {} 
        try:
            group = str(request_data['group']).strip()
            
            #create a database connection
            db = DatabaseAPI("qos")
			#query the table
            query_result = db.query_db("qos_wsinfo", ["ws_map_id","ws_title"], "ws_group like %s", (group, ))
            if len(query_result) == 0:
               return return_response_error(400,"No web services found on group %s"%group, "JSON")
            else:
               service_result['status_code'] = 200
               service_result['message'] = "Success"
               service_list = [] 
               for result in query_result:
			       service_list.append({'service_id': result[0], 'service_title': result[1]})
               service_result['matched_services'] = service_list
 
        except KeyError, e:
            return return_response_error(400,"KeyError: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")

        return service_result

    #-------------------------------------------
    @cherrypy.tools.json_out()
    def get_qosvalue(self, **request_data):
        service_result = {} 
        try:
            sid = str(request_data['service_id']).strip()
            qid = str(request_data['qos_id']).strip()

            if int(qid) == 1:
               service_result = qm.compute_rspt(sid)
            elif int(qid) == 2:
               service_result = qm.compute_thrpt(sid)
            elif int(qid) == 3:
               service_result = qm.compute_avlty(sid)
            elif int(qid) == 4:
               service_result = qm.compute_relbty(sid)
            else:
               raise CustomException("'%d' is not a valid value for 'qos_id' parameter"%(int(qid)))			

        except KeyError, e:
            return return_response_error(400,"KeyError: Missing parameter %s"%(str(e)),"JSON")
        except CustomException, e:
            return return_response_error(400,"Error: %s"%(str(e)),"JSON")
        except Exception, e:
            return return_response_error(500,"Error: %s"%(str(e)), "JSON")
        
        return service_result

	#------------------------------------------------
    #Public /index
    index.exposed = True
    get_serviceids.exposed = True
    get_qosvalue.exposed = True

#-----------------------------------------------------------
def CORS():
    #print "Run CORS"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

#--------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    cherrypy.tools.CORS = cherrypy.Tool("before_finalize",CORS)
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5010,
                            'log.error_file':ERROR_LOG_CHERRYPY_5010,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5010
                          })
    
    conf_CORS = {
             '/':{
                'tools.CORS.on': True,
                'request.show_tracebacks': True,
                'error_page.404': error_page_404,
                'error_page.400': error_page_400,
                'error_page.500': error_page_500
             }
    }
    #cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    #cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

    #Starting Server
    cherrypy.tree.mount(QoS_Service_API(), '/%s/%s' %(str(WS_NAME),str(WS_GROUP1)), conf_CORS )
    
    cherrypy.engine.start()
    cherrypy.engine.block()
