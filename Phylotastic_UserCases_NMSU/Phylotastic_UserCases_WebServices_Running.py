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
import subprocess
from pprint import pprint
from support import UserCase_GetTree_FromWebPage, UseCase_GetTree
from support import UseCase_GetTree_FromText, treebase_api
from __builtin__ import True



USER_CASE_1 = "generateGeneSpeciesReconciliationTree"
USER_CASE_2 = "generateTreesFromWebPages"
USER_CASE_2_2 = "generateTreesFromText"
WS_NAME = "phylotastic_ws"

ROOT_FOLDER = os.getcwd()
IP_ADDRESS = "127.0.0.1:5002"
PUBLIC_HOST_ROOT_WS = "http://%s/%s" %(str(IP_ADDRESS),str(WS_NAME))
PUBLIC_HOST_WS_GENERATE_GENE_SPECIES_RECONCILIATION_TREE = "%s/%s" %(str(PUBLIC_HOST_ROOT_WS),str(USER_CASE_1))


ACCESS_LOG_CHERRYPY_5002 = ROOT_FOLDER + "/log/%s_5002_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5002 = ROOT_FOLDER + "/log/%s_5002_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


WSDL_FORESTER_WS = "http://128.123.177.13/WSRegistry/sites/default/files/wsdl/Phylotastic_Forester_WS.wsdl"
WSDL_PHYLOTASTIC_PRUNNING_WS = "http://128.123.177.13/WSRegistry/sites/default/files/wsdl/Phylotastic_Prunning_WS.wsdl"
WORK_FLOW_CONFIGURATION_FILE = ROOT_FOLDER + "/configuration/work_flow_1.json"

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
def parseWorkFlow_Configuration(WF_CON_FILE):
    with open(WF_CON_FILE) as data_file:    
        data = json.load(data_file)
    return data
class Phylotastic_UserCase_1_GeneSpeciesReconciliationTree(object): 
    def index(self):
        message = "Server is Running. Service is Phylotastic UserCase 1 Gene-SpeciesReconciliationTree." 
        message += "\n ==== WORK FLOW 1 ===== \n"
        message += "\n %s " %(WORK_FLOW_CONFIGURATION_FILE)
        #work_flow_conf = parseWorkFlow_Configuration(WORK_FLOW_CONFIGURATION_FILE)
        #work_flow_function = work_flow_conf['work_flow_web_services'][0]
        #pprint(work_flow_function['ws_input'][0]['input_name'])
        return message;
    def work_flow_2(self,**request_data):
        # Step 1 : Read Gene Tree Data as Newick Format
        try:
            gene_tree_data = str(request_data['gene_tree_data']).strip();
            if (gene_tree_data[len(gene_tree_data)-1] <> ";"):
                gene_tree_data = gene_tree_data + ";"
        except:
            return return_response_error(400,"error","Missing parameters gene_tree_data","JSON")
            
        try:
            format = str(request_data['format']).strip();
        except:
            format = "NEWICK"
            pass
        
        return "thanh nguyen hai"
 
    def work_flow_1(self,**request_data):
        # Step 1 : Read Gene Tree Data as Newick Format
        try:
            gene_tree_data = str(request_data['gene_tree_data']).strip();
            if (gene_tree_data[len(gene_tree_data)-1] <> ";"):
                gene_tree_data = gene_tree_data + ";"
        except:
            return return_response_error(400,"error","Missing parameters gene_tree_data","JSON")
            
        try:
            format = str(request_data['format']).strip();
        except:
            format = "NEWICK"
            pass
        
        #Step 2 : Get Species Name List from Gene Tree by using Forester Web Services
        # Web Service Using : Forester Web Service
        # Function using:
        FUNCTION_NAME = "ForesterWS_GetSpeciesList_By_GeneTree"
        PARAMS = []
        PARAMS.append(gene_tree_data)
        PARAMS.append(format)
        TYPE_RUNNING = "-run"
        result = runWebServiceFunction("%s" %(str(FUNCTION_NAME)), "%s" %(str(WSDL_FORESTER_WS)), PARAMS,TYPE_RUNNING)
        
        if (is_json(result)):
            foresterWS_GetSpeciesList_Object = json.loads(result)
            # Step 3 : Query Species Tree From Species Name list
            species_name_list_url = foresterWS_GetSpeciesList_Object['material']['species_names_list']['text']
            species_name_list_content = readContent(species_name_list_url)
            species_name_result = ""
            for specie in species_name_list_content:
                species_name_result += str(specie).strip() + ", "
            
            #Step 3 : Get Phylotastic Species Tree 
            FUNCTION_NAME_STEP_3 = "PhylotasticPrunner_GetPhylotasticSpeciesTree"
            PARAMS_STEP_3 = []
            PARAMS_STEP_3.append(species_name_result)
            PARAMS_STEP_3.append("mammals")
            PARAMS_STEP_3.append("newick")
        
            TYPE_RUNNING_STEP_3 = "-run"
            newickSpeciesTree = runWebServiceFunction("%s" %(str(FUNCTION_NAME_STEP_3)), "%s" %(str(WSDL_PHYLOTASTIC_PRUNNING_WS)), PARAMS_STEP_3,TYPE_RUNNING_STEP_3)
            
            #Step 4 : Query reconciliation tree from species tree and gene tree
            FUNCTION_NAME_STEP_4 = "ForesterWS_GetReconciliationTree"
            PARAMS_STEP_4 = []
            PARAMS_STEP_4.append(foresterWS_GetSpeciesList_Object['ws_id'])
            PARAMS_STEP_4.append(newickSpeciesTree)
            TYPE_RUNNING_STEP_4 = "-run"
            result_2 = runWebServiceFunction("%s" %(str(FUNCTION_NAME_STEP_4)), "%s" %(str(WSDL_FORESTER_WS)), PARAMS_STEP_4,TYPE_RUNNING_STEP_4)
            
            if (is_json(result_2)):
                #return result_2
                json_result_2 = json.loads(result_2)
                # Build Result Object #
                work_flow_result = MultipleLevelsOfDictionary()
                work_flow_result['ws_name'] = json_result_2['ws_name']
                work_flow_result['ws_operation'] = json_result_2['ws_operation']
                work_flow_result['ws_id'] = "%s" %(json_result_2['ws_id'])  
                work_flow_result['material']['gene_tree']['newick_format'] = foresterWS_GetSpeciesList_Object['material']['gene_tree']['newick_format']
                work_flow_result['material']['gene_tree']['phyloxml_format'] = foresterWS_GetSpeciesList_Object['material']['gene_tree']['phyloxml_format'] 
                work_flow_result['material']['species_tree']['newick_format'] = "%s/static/%s/%s" %(str("http://128.123.177.21:5001/forester_ws"),str(json_result_2['ws_id']),str("input_genetree_newick_species_tree.txt"))
                work_flow_result['material']['gene_species_tree_reconciliation']['phyloxml_format'] = json_result_2['material']['gene_species_tree_reconciliation']['phyloxml_format']
                return return_success_get(work_flow_result)
        else:
            return "NONE"
        
    #Public /index
    index.exposed = True
    
    #Public /work_flow_1
    work_flow_1.exposed = True
    
class Phylotastic_UserCase_2_GenerateTreesFromWebPages(object):
    def index(self):
        return "Use case 2 (Abu Saleh) : Autogenerate trees for web pages ";
    def work_flow_1(self,**request_data):
        try:
            inputURL = str(request_data['url']).strip();
            
        except:
            return return_response_error(400,"error","Missing parameters inputURL","JSON")
        
        usecase2_result = UseCase_GetTree.run_UseCase(inputURL, 2)
        
        return usecase2_result;
        
    #Public /index
    index.exposed = True
    work_flow_1.exposed = True

class Phylotastic_UserCase_2_GenerateTreesFromText(object):
    def index(self):
        return "Use case 2 (Abu Saleh) : Autogenerate trees for Text ";
    def work_flow_1(self,**request_data):
        try:
            inputTEXT = str(request_data['text']).strip();
            
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        usecase2_result = UseCase_GetTree.run_UseCase(inputTEXT, 1)  
        
        return usecase2_result;
        
    #Public /index
    index.exposed = True
    work_flow_1.exposed = True

class Phylotastic_TreeBase_API(object):
    def index(self):
        return "Tree Base API (Abu Saleh) : Build Tree from Taxon ";
    def run(self,**request_data):
        try:
            taxon = str(request_data['taxon']).strip();
            
        except:
            return return_response_error(400,"error","Missing parameters text","JSON")
        
        treebase_result = treebase_api.get_tree(taxon)   
        
        return treebase_result;
        
    #Public /index
    index.exposed = True
    run.exposed = True
    
if __name__ == '__main__':
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5002,
                            'log.error_file':ERROR_LOG_CHERRYPY_5002,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5002
                          })
    
    conf_user_case_1 = {
              '/static' : {
                           'tools.staticdir.on' : True,
                           'tools.staticdir.dir' : os.path.join(ROOT_FOLDER, 'files'),
                           'tools.staticdir.content_types' : {'xml': 'application/xml'}
               }
               
    }
    #Starting Server
    cherrypy.tree.mount(Phylotastic_UserCase_1_GeneSpeciesReconciliationTree(), '/%s/%s' %(str(WS_NAME),str(USER_CASE_1)), conf_user_case_1)
    cherrypy.tree.mount(Phylotastic_UserCase_2_GenerateTreesFromWebPages(), '/%s/%s' %(str(WS_NAME),str(USER_CASE_2)), conf_user_case_1)
    cherrypy.tree.mount(Phylotastic_UserCase_2_GenerateTreesFromText(), '/%s/%s' %(str(WS_NAME),str(USER_CASE_2_2)), conf_user_case_1)
    cherrypy.tree.mount(Phylotastic_TreeBase_API(), '/%s/%s' %(str(WS_NAME),str("treebase_api")), conf_user_case_1)
    cherrypy.engine.start()
    cherrypy.engine.block()
