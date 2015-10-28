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

PUBLIC_HOST = "http://127.0.0.1:5001/forester_ws"


ACCESS_LOG_CHERRYPY_5001 = ROOT_FOLDER + "/log/%s_5001_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_5001 = ROOT_FOLDER + "/log/%s_5001_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


#Operation 1
FORESTER_WS_NAME = "forester_web_service"
FORESTER_WS_GET_SPECIES_NAME_NAME = "get_species_names_list"
FORESTER_WS_GET_GENE_SPECIES_RECONCILIATION = "get_gene_species_tree_reconciliation"
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


def create_static_file(ROOT_FOLDER,PRIVATE_FOLDER,FILE_NAME,FILE_DATA_CONTENT):
    DIRECTION = os.path.join(ROOT_FOLDER + "/files",PRIVATE_FOLDER)
    if not os.path.exists(DIRECTION):
        os.makedirs(DIRECTION)
    try:
        fo = open(os.path.join(DIRECTION, FILE_NAME), "wb")
        fo.write(FILE_DATA_CONTENT)
        return 1
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
        return -1
    finally :
        # close the cursor and connection
        fo.close()

def getSpeciesList(ROOT_FOLDER,PRIVATE_FOLDER,FILE_NAME):
    try:
        absoluteFileName = os.path.join(ROOT_FOLDER,"files",PRIVATE_FOLDER,FILE_NAME)
        shellCall = 'java -Xmx1024m -cp '
        shellCall += ROOT_FOLDER +'/model/forester_1038.jar '
        shellCall += 'org.forester.application.gene_tree_preprocess '
        shellCall += absoluteFileName
        
        file_prefix = FILE_NAME[:-4]
        
        print shellCall
        os.system(shellCall)
        species_present_file = file_prefix + '_species_present.txt'
        gene_tree_xml_file = file_prefix + "_preprocessed_gene_tree.phylo.xml"
    
        return [species_present_file,gene_tree_xml_file]
    except:
        return None
def reconcileTrees(ROOT_FOLDER,PRIVATE_FOLDER,FILE_NAME):
    try:
        abs_input_gene_tree_xml = os.path.join(ROOT_FOLDER,"files",PRIVATE_FOLDER,"input_genetree_newick_preprocessed_gene_tree.phylo.xml")
        
        abs_speciesTreeFile = os.path.join(ROOT_FOLDER,"files",PRIVATE_FOLDER,FILE_NAME)
    
        shellCall = 'java -Xmx1024m -cp '
        shellCall += ROOT_FOLDER+'/model/forester.jar '
        shellCall += 'org.forester.application.gsdi '
        shellCall += '-m -q '
        shellCall += abs_input_gene_tree_xml
        shellCall += ' '+abs_speciesTreeFile
    
        print shellCall 
        os.system(shellCall)
        return 1
    except:
        return -1

def resampledInferenceOfOrthologs(ROOT_FOLDER,ws_id):
    try:
        abs_input_gene_tree_xml = os.path.join(ROOT_FOLDER,"files",ws_id,"input_genetree_newick_preprocessed_gene_tree.phylo.xml")
        
        abs_speciesTreeFile = os.path.join(ROOT_FOLDER,"files",ws_id,"input_genetree_newick_species_tree.txt")
    
        shellCall = 'java -Xmx2048m -cp '
        shellCall += ROOT_FOLDER+'/model/forester.jar '
        shellCall += 'org.forester.application.rio '
        shellCall += abs_input_gene_tree_xml
        shellCall += ' ' + abs_speciesTreeFile
        shellCall += ' ' + "input_genetree_newick_rio.tsv" 
    
        print shellCall 
        os.system(shellCall)
        return 1
    except:
        return -1
   
class Forester_WS(object):
    def index(self):
        return "Server is running. " + socket.gethostname();
    
    def querySpeciesList(self,**request_data):
        PRIVATE_FILE_FOLDER = str(time.time())
        #Step 2 : if action is get species names list
        #Step 2 : Read input gene_tree_data
        forester_object = MultipleLevelsOfDictionary()
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
            
        #Step 3: Create file input_genetree.nwk
        try:
            file_name = "input_genetree_newick.nwk"
            created_file = create_static_file(ROOT_FOLDER,PRIVATE_FILE_FOLDER,file_name,gene_tree_data)
            if (created_file <> 1):
                return return_response_error(400,"error","Cannot create input gene tree file","JSON")
        except:
                return return_response_error(400,"error","Cannot create input gene tree file","JSON")
            
        #Step 4: Running Forester model Input : Gene tree newick file, Output : Gene tree XML file + Species Name List File
        runningModel = getSpeciesList(ROOT_FOLDER,PRIVATE_FILE_FOLDER,file_name)
        if (runningModel is  None):
            return return_response_error(400,"error","Running to get species fails","JSON")
        species_present_file = runningModel[0]
        gene_tree_xml_file = runningModel[1]
            
        #Step 5: Return value for client
        forester_object['ws_name'] = FORESTER_WS_NAME
        forester_object['ws_operation'] = FORESTER_WS_GET_SPECIES_NAME_NAME
        forester_object['ws_id'] = "%s" %(str(PRIVATE_FILE_FOLDER))  
        forester_object['material']['gene_tree']['newick_format'] = "%s/static/%s/%s" %(str(PUBLIC_HOST),str(PRIVATE_FILE_FOLDER),str(file_name))
        forester_object['material']['gene_tree']['phyloxml_format'] = "%s/static/%s/%s" %(str(PUBLIC_HOST),str(PRIVATE_FILE_FOLDER),str(gene_tree_xml_file))
        forester_object['material']['species_names_list']['text'] = "%s/static/%s/%s" %(str(PUBLIC_HOST),str(PRIVATE_FILE_FOLDER),str(species_present_file))
        return return_success_get(forester_object)
        

    def queryReconciliationTree(self,**request_data):
            #Step 2 : if action is get gene-species tree reconciliation
            forester_object = MultipleLevelsOfDictionary()
            
            #Step 2 : Read input gene_tree_data
            try:
                ws_id = str(request_data['ws_id']).strip();
                if (ws_id is None or ws_id == ""):
                    return return_response_error(400,"error","Missing parameters ws_id","JSON")
                
            except:
                return return_response_error(400,"error","Missing parameters ws_id","JSON")
            
            #Step 3 : Read input species name tree
            try:
                species_tree_data = str(request_data['species_tree_data']).strip();
                if (species_tree_data is None or species_tree_data == ""):
                    return return_response_error(400,"error","Missing parameters species_tree_data","JSON")
                if (species_tree_data[len(species_tree_data)-1] <> ";"):
                    species_tree_data = species_tree_data + ";"
            except:
                return return_response_error(400,"error","Missing parameters species_tree_data","JSON")
            
            
            #Step 3: Create file input_genetree.nwk
            try:
                file_name = "input_genetree_newick_species_tree.txt"
                created_file = create_static_file(ROOT_FOLDER,ws_id,file_name,species_tree_data)
                if (created_file <> 1):
                    return return_response_error(400,"error","Cannot create input species tree file","JSON")
            except:
                return return_response_error(400,"error","Cannot create input species tree file","JSON")
            
            
            #Step 4: Running Forester model Input : GeneTreeXML + Species Tree Txt, Output : Gene-species tree reconciliation
            runningModel = reconcileTrees(ROOT_FOLDER,ws_id,file_name)
            if (runningModel == 1):
                forester_object['ws_name'] = FORESTER_WS_NAME
                forester_object['ws_operation'] = FORESTER_WS_GET_GENE_SPECIES_RECONCILIATION
                forester_object['ws_id'] = "%s" %(str(ws_id))  
                forester_object['material']['gene_species_tree_reconciliation']['phyloxml_format'] = "%s/static/%s/%s" %(str(PUBLIC_HOST),str(ws_id),str("input_genetree_newick_preprocessed_gene_tree.phylo_gsdi_out.phylo.xml"))
                return return_success_get(forester_object)
            else:
                return return_response_error(400,"error","Running model error","JSON")
             
    
        
        
    #Public /index
    index.exposed = True
    #public querySpeciesList
    querySpeciesList.exposed = True
    
    queryReconciliationTree.exposed = True

if __name__ == '__main__':
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 5001,
                            'log.error_file':ERROR_LOG_CHERRYPY_5001,
                            'log.access_file':ACCESS_LOG_CHERRYPY_5001
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
    cherrypy.quickstart(Forester_WS(), '/forester_ws', conf)
    #cherrypy.engine.start()