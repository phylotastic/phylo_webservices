import time
import string
import random
import re
import os
import logging as log
from ete3 import Tree, TreeStyle
from ete3.parser.newick import NewickError
from xvfbwrapper import Xvfb

from . import tree_actions

def timeit(f):
    def a_wrapper_accepting_arguments(*args, **kargs):
        t1 = time.time()
        r = f(*args, **kargs)
        print (" %0.3f secs: %s" %(time.time() - t1, f.__name__))
        return r
    return a_wrapper_accepting_arguments

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class WebTreeHandler(object):
    def __init__(self, newick_str, tid, actions=None, style=None):
        self.tree = None
        self.treenewick = newick_str

        self.treeid = tid
        self.mapid = "map_" + str(tid)
        self.imgid = "img_" + str(tid)
        self.boxid = 'box_' + str(tid)

        self.treeconfig_obj = None

    def get_node_descendants(self, node_id):
         target = self.tree.search_nodes(_nid=int(node_id))[0]
         des_nodes = target.get_descendants('preorder')
         return des_nodes

    def get_tree_leaves(self):
         return [leaf for leaf in self.tree.iter_leaves()]
    
    def init_nodeids(self):
        # Initialze node internal IDs
        for index, n in enumerate(self.tree.traverse('preorder')):
            n._nid = index

    def parse_newick(self):
        #print (self.treenewick)
        newick_str = self.treenewick.encode('ascii', 'ignore').decode('ascii') #to remove unicode errors
        tmp_nwk =  newick_str.replace("&#39;", "'") #to remove the html code of apostrophe 
        self.treenewick = tmp_nwk  
        #print (self.treenewick)
        try:
           self.tree = Tree(self.treenewick)
        except NewickError:
           try:
              self.tree = Tree(self.treenewick, format=1)
           except NewickError as e:
              if 'quoted_node_names' in str(e):
                  self.tree = Tree(self.treenewick, format=1, quoted_node_names=True)
              else:
                  return "Newick Parsing Error: "+str(e)

        self.init_nodeids()
        return True

    def set_actions(self, actions=None):
        if actions is None:
           self.tree.actions = tree_actions.NodeActions()#NodeActions()
        else:
           self.tree.actions = actions

    def set_style(self, style=None):
        if style is None:
           self.tree.tree_style = TreeStyle()
        else:
           self.tree.tree_style = style

    def set_tree_config(self, tcofg):
        self.treeconfig_obj = tcofg

    @timeit
    def redraw(self, top_offset=0,left_offset=0):
        print ("in redraw topoffset:"+str(top_offset)+" leftoffset:"+str(left_offset))
        #print "Inside redraw calling tree.render()"
        #os.environ["DISPLAY"]=":0" # Used by ete to render images
        with Xvfb() as xvfb:
             base64_img_byte, img_map = self.tree.render("%%return.PNG", tree_style=self.tree.tree_style)
             base64_img = str(base64_img_byte, 'utf-8', 'ignore') #need only in python3
             #print "Inside redraw calling get_html_map()...."
             html_map = self.get_html_map(img_map)

        ete_link = '<div style="margin:0px;padding:0px;text-align:left;"><a href="http://etetoolkit.org" style="font-size:10pt;" target="_blank" >Powered by etetoolkit</a></div>'
        #html_img = """<img id="%s" class="ete_tree_img" USEMAP="#%s" onLoad="javascript:bind_popup(%s,%s);" src="data:image/gif;base64,%s">""" %(self.imgid, self.mapid, left_offset, top_offset, base64_img)
        html_img = """<img id="%s" class="ete_tree_img" USEMAP="#%s" onLoad="javascript:bind_popup(%s,%s);" src="data:image/gif;base64,%s">""" %(self.imgid, self.mapid, left_offset, top_offset, base64_img)

        tree_div_id = self.boxid
        #print "returning html from redraw method...."
        return html_map+ '<div id="%s" >'%tree_div_id + html_img + ete_link + "</div>"

    #------------------------------------------
    def save_image(self, img_format):
        img_url = os.path.join("http://localhost:8080/trees/", self.treeid+"."+img_format)
        #img_path = os.path.join("/var/www/TreeViewer/html/tmp/", self.treeid+"."+img_format)
        img_path = os.path.join("/trees/", self.treeid+"."+img_format)
        with Xvfb() as xvfb:        
             img = self.tree.render(img_path, tree_style=self.tree.tree_style)

        #print "returning from save image"
        return '<a target="_blank" href="%s">Download Image</a>' %(img_url)
    #------------------------------------------
    def get_html_map(self, img_map):
        html_map = '<MAP NAME="%s" class="ete_tree_img">' %(self.mapid)
        #print "get_html_map method called......."
        if img_map["nodes"]:
            for x1, y1, x2, y2, nodeid, text in img_map["nodes"]:
                text = "" if not text else text
                area = img_map["node_areas"].get(int(nodeid), [0,0,0,0])
                html_map += """ <AREA SHAPE="rect" COORDS="%s,%s,%s,%s"
                                onMouseOut='unhighlight_node();'
                                onMouseOver='highlight_node("%s", "%s", "%s", %s, %s, %s, %s);'
                                onClick='show_actions("%s", "%s");'
                                href="javascript:void('%s');">""" %\
                    (int(x1), int(y1), int(x2), int(y2),
                     self.treeid, nodeid, text, area[0], area[1], area[2]-area[0], area[3]-area[1],
                     self.treeid, nodeid,
                     nodeid)

        if img_map["faces"]:
            for x1, y1, x2, y2, nodeid, text in img_map["faces"]:
                text = "" if not text else text
                area = img_map["node_areas"].get(int(nodeid), [0,0,0,0])
                html_map += """ <AREA SHAPE="rect" COORDS="%s,%s,%s,%s"
                                onMouseOut='unhighlight_node();'
                                onMouseOver='highlight_node("%s", "%s", "%s", %s, %s, %s, %s);'
                                onClick='show_actions("%s", "%s", "%s");'
                                href='javascript:void("%s");'>""" %\
                    (int(x1),int(y1),int(x2),int(y2),
                     self.treeid, nodeid, text, area[0], area[1], area[2]-area[0], area[3]-area[1],
                     self.treeid, nodeid, text,
                     text,
                     )
        html_map += '</MAP>'
        #print "returning html from get_html_map()...."
        return html_map
    
    #---------------------------------------
    def get_tree_node(self, nodeid):
        target_node = self.tree.search_nodes(_nid=int(nodeid))[0]
        return target_node

    def get_node_name(self, nodeid):
        target_node = self.get_tree_node(nodeid)
        return target_node.name
    #--------------------------------------
    def get_avail_actions(self, nodeid):
        #print("getting available options")
        try:
          target = self.tree.search_nodes(_nid=int(nodeid))[0]
          action_list = []
          for aindex, aname, aorder, show_fn, run_fn, html_generator in self.tree.actions:
              if show_fn(target):
                  action_list.append([aindex, aname, aorder, html_generator])
          action_list.sort(key=lambda x: x[2])
          #print(action_list)
        except Exception as e:
          print("Error in nodeaction: %s"%str(e))

        return action_list

    #--------------------------------------------
    def run_action(self, aindex, nodeid, astatus,a_data=-1):
        if aindex is None:
           return #no_action
        
        target = self.tree.search_nodes(_nid=int(nodeid))[0]
        run_fn = self.tree.actions.actions[aindex][3]
        #print "run action called in tree handler"
        return run_fn(self.tree, target, astatus, a_data)

    #--------------------------------------------
    def run_tree_action(self, color_code,line_width):
        #print "run_tree_action called..."
        return self.treeconfig_obj.run_action_linecolorwidth(self.tree, color_code, line_width)

    def run_tree_customize(self, branch, internal, ladderize):
        #print "run_tree_customize called..."
        self.treeconfig_obj.set_custom_options(branch, internal)
        if ladderize:
           self.treeconfig_obj.run_action_ladderize(self.tree)

    #---------------------------------------------
'''   
class NodeActions(object):
    def __str__(self):
        text = []
        for aindex, aname, aorder, show_fn, run_fn, html_generator in self:
            text.append("%s: %s, %s, %s, %s" %(aindex, aname, show_fn, run_fn, html_generator))
        return '\n'.join(text)

    def __iter__(self):
        for aindex, (aname, aorder, show_fn, run_fn, html_generator) in self.actions.items():
            yield (aindex, aname, aorder, show_fn, run_fn, html_generator)

    def __init__(self):
        self.actions = {}

    def clear_default_actions(self):
        self.actions = {}

    def add_action(self, action_strid, action_name, display_order, show_fn, run_fn, html_generator):
        #aindex = "act_"+id_generator()
        aindex = re.sub(r"\s+", '_', action_strid)
        self.actions[aindex] = [action_name, display_order, show_fn, run_fn, html_generator]
'''
