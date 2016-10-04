from distutils.util import strtobool
import gzip
import logging as log
from StringIO import StringIO
from bottle import (run, get, post, request, route, response, abort, hook,
                    error, HTTPResponse)

from ete3_helper.tree_handler import WebTreeHandler, NodeActions, TreeStyle
from ete3_helper.tree_config import WebTreeConfig
import types


LOADED_TREES = {}
COMPRESS_DATA = True
COMPRESS_MIN_BYTES = 10000
TREE_HANDLER = WebTreeHandler
TREE_CONFIG = WebTreeConfig

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

@route('/status')
def server_status():
    return web_return('alive', response)

# WEB API FUNCTIONALITY
@post('/get_tree_image')
def get_tree_image():
    ''' Requires a POST param "newick" containing the tree to be loaded. '''
	
    #print "get_tree_image called...."
    if request.json:
        source_dict = request.json
    else:
        source_dict = request.POST
    
    newick = source_dict.get('newick', '').strip()
    treeid = source_dict.get('treeid', '').strip()
    
    if "top_offset" in source_dict:
        topoffset = source_dict.get('top_offset','').strip()
    if "left_offset" in source_dict:
        leftoffset = source_dict.get('left_offset', '').strip()

    if not newick or not treeid:
        return web_return('No tree provided', response)
  
    if treeid in LOADED_TREES:
       del LOADED_TREES[treeid] #"delete existing tree obj of same tree"

    h = TREE_HANDLER(newick, treeid)
    newick_checker = h.parse_newick()

    if type(newick_checker) != types.BooleanType:
       del h
       return web_return("<b>"+newick_checker+"</b>", response)

    tc = TREE_CONFIG(h.tree, h.treeid)
    #check whether external data is provided or not
    if 'extra_data' in source_dict:
        external_data = source_dict.get('extra_data')
        tc.set_extra_tipdata(external_data)

    h.set_actions(tc.get_node_action())
    h.set_style(tc.get_tree_style())
    h.set_tree_config(tc)
    LOADED_TREES[h.treeid] = h
    #print "redraw called....."
    # Renders initial tree
    img = h.redraw(topoffset, leftoffset)
    
    return web_return(img, response)

#------------------------------------------------
@post('/save_tree_image')
def save_tree_image():
    ''' Requires a POST param "newick" containing the tree to be loaded. '''
    if request.json:
        source_dict = request.json
    else:
        source_dict = request.POST
    
    treeid = source_dict.get('treeid', '').strip()
    img_format = source_dict.get('format', '').strip()
    #print "save_tree_image called...."
    if not treeid:
        return web_return('No tree provided', response)
    elif not img_format:
        return web_return('No image format provided', response)

    h = LOADED_TREES[treeid]
    
    # Renders initial tree
    html_part = h.save_image(img_format)
    
    return web_return(html_part, response)


#------------------------------------------------
@post('/get_actions')
def get_action():
    if request.json:
        source_dict = request.json
    else:
        source_dict = request.POST
    #print "get_actions method called...."  
    treeid = source_dict.get('treeid', '').strip()
    nodeid = source_dict.get('nodeid', '').strip()
    #print "treeid: " + str(treeid) + " nodeid: " + str(nodeid)
    if treeid and nodeid:
        h = LOADED_TREES[treeid]
        #html = "<ul class='ete_action_list'>"
        node_name = h.get_node_name(nodeid)
        header = "Node Actions"
        html = """<div id="ete_popup_header"><span id="ete_popup_header_text">%s</span><div id="ete_close_popup" onClick='hide_popup();'></div></div><ul>""" % (header)
        
        if node_name:
           html += """
                <li style="background:#eee; font-size:10pt;">
                <div style="text-align:left;font-weight:bold;">
                 Node: %s
                </div>
                </li>"""  %(node_name)

        for aindex, aname, html_generator in h.get_avail_actions(nodeid):
            node = h.get_tree_node(nodeid)
            if html_generator:
               html += html_generator(aindex, treeid, nodeid, node)
            else:
               html += """<li><a  onClick="run_action('%s', '%s', '%s', '%s');" >%s</a></li>""" %(treeid, nodeid, '', aindex, aname)
        html += "</ul>"
    
    return web_return(html, response)

@post('/run_action')
def run_action():
    if request.json:
        source_dict = request.json
    else:
        source_dict = request.POST
    #print "run_action method called...."
  
    treeid = source_dict.get('treeid', '').strip()
    nodeid = source_dict.get('nodeid', '').strip()
    faceid = source_dict.get('faceid', '').strip()
    aindex = source_dict.get('aindex', '').strip()
    #print "treeid: " + str(treeid) + " nodeid: " + str(nodeid) + " aindex: " + str(aindex)
    if treeid and nodeid and aindex:
        h = LOADED_TREES[treeid]
        print "run_action method in treehandler called...."
        h.run_action(aindex, nodeid)
        print "redraw method in treehandler called..."
        img = h.redraw()
    
    return web_return(img, response)


@post('/run_tree_action')
def run_tree_action():
    if request.json:
        source_dict = request.json
    else:
        source_dict = request.POST
    #print "run_tree_action method called...."
  
    treeid = source_dict.get('treeid', '').strip()
    colorcode = source_dict.get('colorcode', '').strip()
    linewidth = source_dict.get('linewidth', '').strip()
    
    do_ladderize = False
    if "ladderize" in source_dict:
        ladderized = source_dict.get('ladderize', '').strip()
        do_ladderize = bool(strtobool(ladderized))

    show_branch_info = False
    if "show_branch" in source_dict: 
        show_branch = source_dict.get('show_branch', '').strip()
        show_branch_info = bool(strtobool(show_branch))

    show_internal_nodes = False
    if "show_internal" in source_dict: 
        show_internal = source_dict.get('show_internal', '').strip()
        show_internal_nodes = bool(strtobool(show_internal))
    
    if "top_offset" in source_dict:
        topoffset = source_dict.get('top_offset','').strip()
    if "left_offset" in source_dict:
        leftoffset = source_dict.get('left_offset', '').strip()

    #print "treeid: " + str(treeid) + " nodeid: " + str(nodeid) + " aindex: " + str(aindex)
    if treeid:
        h = LOADED_TREES[treeid]
        
        h.run_tree_action(colorcode, linewidth)
        if do_ladderize:
           #print "run_tree_ladderize method called...."
           h.run_tree_ladderize()
        
        h.run_tree_customize(show_branch_info, show_internal_nodes)
        #print "redraw method in treehandler called..."
        img = h.redraw(topoffset, leftoffset)
    
    return web_return(img, response)


# Server configuration
def start_server(host="phylo.cs.nmsu.edu", port=8989):
    run(host=host, port=port)

if __name__ == '__main__':
    #localhost = ""
    #port =
    start_server(); 		
