from distutils.util import strtobool
import bottle
import json
import gzip
import logging as log
from io import StringIO
from bottle import (run, get, post, request, route, response, abort, hook,
                    error, HTTPResponse)

#from ete_helper.tree_handler import WebTreeHandler, NodeActions, TreeStyle
#from ete_helper.tree_config import WebTreeConfig
from ete_helper import controller as ctrl 

from ete_helper import tree_handler
from ete_helper import tree_config

#--------------------------------------
LOADED_TREES = {}
COMPRESS_DATA = True
COMPRESS_MIN_BYTES = 10000

TREE_HANDLER = tree_handler.WebTreeHandler
TREE_CONFIG = tree_config.WebTreeConfig

def web_return(html, response):
    if COMPRESS_DATA and len(html) >= COMPRESS_MIN_BYTES:
        chtmlF = StringIO()
        z = gzip.GzipFile(fileobj=chtmlF, mode='w')
        z.write(html)
        z.close()
        chtmlF.seek(0)
        html = chtmlF.read()
        log.info('returning compressed %0.3f KB' %(len(html)/1024.))
        response.set_header( 'Content-encoding', 'gzip')
        response.set_header( 'Content-length', len(html))
    else:
        log.info('returning %0.3f KB' %(len(html)/1024.))
    
    return html

def json_return(data, response): 
    #print data
    response.content_type = 'application/json'
    
    return json.dumps(data)


# THESE ARE THE WEB SERVICES PROVIDING DATA TO THE WEB AND API
@error(405)
def method_not_allowed(res):
    if request.method == 'OPTIONS':
        new_res = HTTPResponse()
        new_res.headers['Access-Control-Allow-Origin'] = '*'
        new_res.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT'
        new_res.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        return new_res
    res.headers['Allow'] += ', OPTIONS'
    return request.app.default_error_handler(res)

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

# WEB API FUNCTIONALITY
@route('/ete_pro/status')
def server_status():
    return web_return('alive', response)

#-------------------------------------------
@post('/ete_pro/get_tree_image')
def get_tree_image():
    # Requires a POST parameter "newick" containing the tree to be loaded.
    #print "get_tree_image called...."
    if request.json:
        source_dict = request.json
    else:
        source_dict = request.POST
    
    #tree_newick = source_dict.get('tree_newick', '').strip()
    #tree_id = str(source_dict.get('tree_id', '')).strip()
    #actions = source_dict.get('actions', '')
    tree_newick = source_dict["tree_newick"]
    tree_id = source_dict["tree_id"]
    actions = source_dict["actions"]
    print(tree_newick)
    print(tree_id)
    print(actions)    

    if "top_offset" in source_dict:
       topoffset = source_dict["top_offset"]
    else:
       topoffset = 0
    if "left_offset" in source_dict:
       leftoffset = source_dict["left_offset"]
    else:
       leftoffset = 0

    if not tree_newick or not tree_id:
        return json_return({'status_code': "400",'message':"Missing Parameter Error: No newick tree or tree id provided"}, response)

    try:
       tree_handler = ctrl.create_tree_obj(tree_newick, tree_id)
       #check for errors related to parsing newick
       if type(tree_handler) is dict:
          return json_return(tree_handler, response)
    except Exception as e:
          print("tree_handler error: %s"%str(e))
          return json_return({"message:":"tree_handler error: %s"%str(e), "status_code": 500}, response) 

    try:
       # Renders initial tree image with actions applied
       if actions != '':
          print("Applying actions....")
          tree_data = ctrl.apply_actions(tree_handler, actions, topoffset, leftoffset)
          return json_return(tree_data, response) 
       else:
          print("Drawing tree image....")
          # Renders initial tree image without any actions applied   
          html_img_data = tree_handler.redraw(topoffset, leftoffset)
    except Exception as e:
          print("tree_actions error: %s"%str(e))
          return json_return({"message:":"tree_actions error: %s"%str(e), "status_code": 500}, response) 


    #print "returning initial image from get_tree_image.."
    return json_return({'tree_newick':tree_handler.treenewick, 'tree_id':tree_handler.treeid, 'html_data': html_img_data, 'actions':{'tree_actions':{}, 'node_actions':[]}}, response)

#------------------------------------------------
@post('/ete_pro/save_tree_image')
def save_tree_image():
    #Requires a POST parameter format of the tree to be saved
    #print "save_tree_image called...."
    if request.json:
        source_dict = request.json
    else:
        source_dict = request.POST
    
    tree_newick = source_dict.get('tree_newick', '').strip()
    tree_id = str(source_dict.get('tree_id', '')).strip()
    actions = source_dict.get('actions', '')
    img_format = source_dict.get('format', '').strip()

    if not tree_newick or not tree_id:
        return json_return({'status_code': "400",'message':"Missing Parameter Error: No newick tree or tree id provided"}, response)
    
    if not img_format:
        return json_return({'status_code': "400",'message':"Missing Parameter Error: No image format provided"}, response)
    
    tree_handler = ctrl.create_tree_obj(tree_newick, tree_id)
    #check for errors related to parsing newick
    if type(tree_handler) is dict:
       return json_return(tree_handler, response)

    # Renders initial tree image with actions applied
    if actions != '':
       tree_data = ctrl.apply_actions(tree_handler, actions) 
    
    # Renders initial tree
    html_url_part = tree_handler.save_image(img_format)
    return json_return({'tree_newick':tree_handler.treenewick, 'tree_id':tree_handler.treeid, 'html_data': html_url_part}, response)

#------------------------------------------------
@post('/ete_pro/get_actions')
def get_action():
    #print "get_actions method called...."
    if request.json:
        source_dict = request.json
    else:
        source_dict = request.POST
    
    tree_newick = source_dict.get('tree_newick', '').strip()
    tree_id = str(source_dict.get('tree_id', '')).strip()
    node_actions = source_dict.get('node_actions')
    node_id = source_dict.get('node_id', '')

    #print "treeid: " + str(treeid) + " nodeid: " + str(nodeid)
    
    if not tree_newick or not tree_id:
        return json_return({'status_code': "400",'message':"Missing Parameter Error: No newick tree or tree id provided"}, response)

    tree_handler = ctrl.create_tree_obj(tree_newick, tree_id)

    if not ctrl.is_empty(node_actions):
       new_node_actions = ctrl.apply_node_actions(tree_handler, node_actions)
       #return json_return({'status_code': "400",'message':"Missing Parameter Error: No action provided for node"}, response)
    
    node_name = tree_handler.get_node_name(node_id)
    #print node_name
    #header = "Actions menu"
    if node_name:
       header = """
               <i>%s</i> actions
                """ %(node_name)
    else:
       header = "Node actions"
             
    html = """<div id="ete_popup_header"><span id="ete_popup_header_text">%s</span><div id="ete_close_popup" onClick='hide_popup();'></div></div><ul>""" % (header)
    
    for aindex, aname, aorder, html_generator in tree_handler.get_avail_actions(node_id):
        node = tree_handler.get_tree_node(node_id)
        if html_generator:
           html += html_generator(aindex, tree_id, node_id, node)
        else:
           html += """<li style="font-size:12pt"><a  onClick="run_action('%s', '%s', '%s');" >%s</a></li>""" %(tree_id, node_id, aindex, aname)
    html += "</ul>"
    #print "returning html for actions from get_actions.."
    
    return json_return({'tree_newick':tree_handler.treenewick, 'tree_id':tree_handler.treeid, 'html_data': html}, response)

#---------------------------------------------------------
@post('/ete_pro/set_all_images')
def set_all_pictures():
    #print "set_pictures method called...."
    if request.json:
        source_dict = request.json
    else:
        source_dict = request.POST
    
    tree_newick = source_dict.get('tree_newick', '').strip()
    tree_id = str(source_dict.get('tree_id', '')).strip()
    node_actions = source_dict.get('node_actions')
    
    #print "tree_id: " + str(tree_id) + " node_actions: " + str(node_actions)
    
    if not tree_newick or not tree_id:
        return json_return({'status_code': "400",'message':"Missing Parameter Error: No newick tree or tree id provided"}, response)

    tree_handler = ctrl.create_tree_obj(tree_newick, tree_id)

    new_node_actions = ctrl.set_all_picture_action(tree_handler, node_actions)
    
    return json_return({'tree_newick':tree_handler.treenewick, 'tree_id':tree_handler.treeid, 'actions': {'node_actions': new_node_actions}}, response)

#--------------------------------------------------------
# Server configuration

def start_server(host="0.0.0.0", port=8989, serverName=None):
    if serverName is not None:
       run(host=host, port=port, server=serverName)
    else:
       run(host=host, port=port)
#----------------MAIN---------------------------------
if __name__ == '__main__':
    start_server()
# Run bottle in application mode. Required in order to get the application working with uWSGI!
else:
    app = application = bottle.default_app() 		
