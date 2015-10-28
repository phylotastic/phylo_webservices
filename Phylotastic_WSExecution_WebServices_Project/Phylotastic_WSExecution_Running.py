'''
Created on Sep 3, 2015

@author: thanhnh2911
'''
import cherrypy
import time
import datetime
import json
import os
import sys
import collections
import socket

ROOT_FOLDER = os.getcwd()

PUBLIC_HOST = "http://128.123.177.21:5003/WSExecution"


ACCESS_LOG_CHERRYPY_5003 = ROOT_FOLDER + "/log/%s_5001_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5003 = ROOT_FOLDER + "/log/%s_5001_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


#Operation 1

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
    return json.dumps(forester_object,indent=4)

def return_success_text(result):
    cherrypy.response.headers['Content-Type'] = "text/plain"
    cherrypy.response.headers['Retry-After']=60
    cherrypy.response.status = 200
    return result

def run_command(command):
    try:
        from subprocess import Popen, PIPE, STDOUT
        p = Popen(command, stdout=PIPE, stderr=STDOUT)
        for line in p.stdout:
            #print str(line)
            if (str(line).strip().upper()[:25] == "FINAL_RESULT_JSON_OUTPUT:"):
                return line[25:]
        return None
    except Exception,err:
        print err
        return None

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
    except Exception,err:
        print err
        return None

def buildListParams(params_string,delimeter_between_params,delimeter_inside_one_param):
    return params_string.split(delimeter_between_params)
   
class Phylotastic_WSExecution_WS(object):
    def index(self):
        return "Server is running. " + socket.gethostname();
    
    
    def runWSFunctionWithWSDL_json(self,**request_data):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        input_json_data = json.loads(rawbody)
        
        try:
            ws_function_name = str(input_json_data['ws_function_name']).strip();
        except:
            return return_response_error(400,"error","Missing parameters ws_function_name","JSON")
        
        try:
            ws_wsdl_url = str(input_json_data['ws_wsdl_url']).strip();
        except:
            return return_response_error(400,"error","Missing parameters ws_wsdl_url","JSON")
        
        try:
            ws_input_params_list = input_json_data['ws_input_params']
            print ws_input_params_list
        except:
            ws_input_params_list = []
            pass
        
        ws_call_function_result = runWebServiceFunction(ws_function_name,ws_wsdl_url,ws_input_params_list,'-run')
        print ws_call_function_result
        return return_success_text(ws_call_function_result)
    
      
    def runWSFunctionWithWSDL_wwwEncode(self,**request_data):
        try:
            ws_function_name = str(request_data['ws_function_name']).strip();
        except:
            return return_response_error(400,"error","Missing parameters ws_function_name","JSON")
            
        try:
            ws_wsdl_url = str(request_data['ws_wsdl_url']).strip();
        except:
            return return_response_error(400,"error","Missing parameters ws_wsdl_url","JSON")
        
        try:
            delimeter_between_params = str(request_data['delimeter_between_params']).strip();
        except:
            delimeter_between_params = "|"
            pass
        
        try:
            ws_input_params = str(request_data['ws_input_params']).strip();
            ws_input_params_list = buildListParams(ws_input_params, delimeter_between_params,",")
        except:
            ws_input_params = ""
            ws_input_params_list = []
            pass
    
        ws_call_function_result = runWebServiceFunction(ws_function_name,ws_wsdl_url,ws_input_params_list,'-run')
        print ws_call_function_result
        return return_success_text(ws_call_function_result)        
    #Public /index
    index.exposed = True
    runWSFunctionWithWSDL_wwwEncode.exposed = True
    runWSFunctionWithWSDL_json.exposed = True
if __name__ == '__main__':
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5003,
                            'log.error_file':ERROR_LOG_CHERRYPY_5003,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5003
                          })
   
    conf = {
              '/static' : {
                           'tools.staticdir.on' : True,
                           'tools.staticdir.dir' : os.path.join(ROOT_FOLDER, 'files'),
                           'tools.staticdir.content_types' : {'xml': 'application/xml'}
               },
               '/crossdomain.xml': {
                           'tools.staticfile.on': True,
                           'tools.staticfile.filename': os.path.join(ROOT_FOLDER, 'static/crossdomain.xml')
               }
               
    }
    
    cherrypy.config.update(conf)
    
    print cherrypy.config
    #Starting Server
    cherrypy.quickstart(Phylotastic_WSExecution_WS(), '/WSExecution', conf)
    #cherrypy.engine.start()