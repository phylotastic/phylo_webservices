#from tree_handler import NodeActions
from ete3 import TreeStyle, NodeStyle, TextFace, add_face_to_node, ImgFace, BarChartFace, faces
import os, json
import requests
import random

from . import tree_actions
#import importlib, importlib.util

#def module_from_file(module_name, file_path):
#    spec = importlib.util.spec_from_file_location(module_name, file_path)
#    module = importlib.util.module_from_spec(spec)
#    spec.loader.exec_module(module)
#    return module

#na = module_from_file("NodeActions", os.getcwd()+"/ete_helper/"+"tree_actions.py")
#NodeActions = na

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Custom ETE Tree styles and web actions
#image_path = "/images" #"/var/web_service"
image_path = ""

class WebTreeConfig(object):
    def __init__(self, treeobj, tid):
        self._treeobj = treeobj
        self._treeid = tid
        self._treestyle = None
        #self._tree_leaves = [leaf.name for leaf in treeobj.iter_leaves()]
        self._tip2info = {}
        self._tip2color = {}
        self._tip2headers = None
        self._tip_max = 0.0
        #self._custom_options = {"draw_support": False, "draw_internal": False}
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~add custom options~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._custom_options = {"draw_support": False, "draw_internal": False, "show_common": False}
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._node2label = {}
        self._img_chk_list = []
        self._img_data_dic = {}
        self._eol_link_dic = {}

    
    def get_tree_style(self):
        ts = TreeStyle()
        ts.layout_fn = self.custom_layout
        ts.show_leaf_name = False
        ts.draw_guiding_lines = True
        ts.guiding_lines_type = 0 #solid line
        ts.guiding_lines_color = "#000000"
        if not(self.is_scaled_tree()):
           #print "set scale to false"
           ts.show_scale = False
        else:
           ts.show_scale = True

        self._treestyle = ts
        return ts

    def get_node_action(self):
        print("get_node_action called..")
        act = tree_actions.NodeActions() #NodeActions()
        #act.add_action('Root here', self.show_action_root, self.run_action_root, None)
        act.add_action('Box Highlight', "Add (remove) box", 3, self.show_action_highlight, self.run_action_boxhighlight, None)
        #act.add_action('Line Highlight', "Thick (thin) branch", 4, self.show_action_highlight, self.run_action_indvhighlight, None)
        #act.add_action('Change style', self.show_action_change_style, self.run_action_change_style, None)
        act.add_action('EOL Link', 'Read info page', 1, self.show_eol_link, None, self.eol_link)
        act.add_action('Display Picture', "Add (remove) photo", 2, self.show_action_picture, self.run_action_picture, None)
        #act.add_action('Hide Picture', self.show_action_picture, self.run_clear_picture, None)
        act.add_action('Change Picture', "Change photo", 5, self.show_change_picture, self.run_change_picture, None)
        act.add_action('Collapse', "Collapse subtree", 1, self.show_action_collapse, self.collapse, None)
        act.add_action('Expand', "Expand subtree", 1, self.show_action_expand, self.expand, None)
        act.add_action('Swap Children',"Rotate subtree", 2, self.show_action_swap,self.swap_branches,None)

        print(act)

        return act

    def set_custom_options(self, branch_len=False, internal_node=False, show_common=False):
        #set whether branch lengths should be drawn or not
        self._custom_options["draw_support"] = branch_len
        #set whether internal nodes should be drawn or not
        self._custom_options["draw_internal"] = internal_node 
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #set whether common names should be shown or not
        self._custom_options["show_common"] = show_common  
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    #Checks whether the tree is scaled or not
    def is_scaled_tree(self):
        is_scaled = False
        for node in self._treeobj.iter_descendants("postorder"):
            #print node.dist
            if node.dist != 1.0:
               is_scaled = True
               break
            
        #print is_scaled
        return is_scaled
#--------------------------------------------
    def set_extra_tipdata(self, extra_tipdata):
        #ext_json_data = json.loads(extra_tipdata)
        ext_json_data = extra_tipdata 
        self._tip2headers = ext_json_data['tip_data_headers']
        tips_list = ext_json_data['tip_list']
        for tip_obj in tips_list:
            self._tip2info[tip_obj['tip_name']] = tip_obj['tip_data_values']
            self._tip2color[tip_obj['tip_name']] = tip_obj['tip_data_colors']

        self._tip_max = get_max_value(tips_list)

        node_label_list = ext_json_data['node_label_list']
        for node_obj in node_label_list:
            self._node2label[node_obj['node_name']] = node_obj['node_label']
         
#----------------------------------------
    #add extra data to tree~~~~~~NEW FORMAT~~~~~~~~~~
    def set_extra_tipdata(self, extra_tipdata): 
        tips_list = extra_tipdata['tip_list']
        for tip_obj in tips_list:
            for sc_name in tip_obj['scientific_names']:
                self._tip2info[sc_name] = tip_obj['common_name'][0] #make a list of common names
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

#------------------------------------------        
    def custom_layout(self,node):
        if node.is_leaf():
           aligned_name_face = TextFace(node.name, fgcolor='olive', fsize=14)
           aligned_name_face.margin_top = 5
           aligned_name_face.margin_right = 5
           aligned_name_face.margin_left = 5
           aligned_name_face.margin_bottom = 5
           aligned_name_face.hz_align = 0     #0 = left, 1 = center, 2 = right 
           add_face_to_node(aligned_name_face, node, column=2, position='aligned')
           #name_face = TextFace(node.name, fgcolor='#333333', fsize=11)
           #name_face.margin_top = 3
           #name_face.margin_right = 3
           #name_face.margin_left = 3
           #name_face.margin_bottom = 3 
           #add_face_to_node(name_face, node, column=2, position='branch-right')
           node.img_style['size'] = 0
           #---------------------------------------------
           #displaying extra categorical and numeric data
           '''
           if (node.name in self._tip2info):
              column_no = 3
              for headerIndex, dataheader in enumerate(self._tip2headers):
                  extra_data = self._tip2info[node.name][headerIndex]
                  if isinstance( extra_data, ( int, float ) ):
                     extra_face = BarChartFace([extra_data], width=100,height=25,colors=[self._tip2color[node.name][headerIndex]],labels=[dataheader],min_value=0.0,max_value=self._tip_max)
                  else:
                     extra_face = TextFace(extra_data, fsize=11, fgcolor='black')
                     extra_face.background.color = self._tip2color[node.name][headerIndex]

                  extra_face.margin_left = 5
                  extra_face.margin_top = 5
                  extra_face.margin_right = 5
                  extra_face.margin_bottom = 5
                   
                  add_face_to_node(extra_face, node, column=column_no, position='aligned')
                  #add_face_to_node(extra_face, node, column=column_no, aligned = True, position='branch-right')
                  column_no += 1
           else:
              #print "No data available"
              column_no = 3
              for headerIndex, dataheader in enumerate(self._tip2headers):     
                  extra_face = TextFace("No data available", fsize=10, fgcolor='black')
         
                  extra_face.margin_left = 5
                  extra_face.margin_top = 5
                  extra_face.margin_right = 5
                  extra_face.margin_bottom = 5
              
                  add_face_to_node(extra_face, node, column=column_no, position='aligned')
                  column_no += 1
           '''
           #displaying extra common name information
           #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
           column_no = 3
           if (node.name in self._tip2info) and self._custom_options["show_common"]:   
              extra_data = self._tip2info[node.name]
              extra_face = TextFace(extra_data, fsize=11, fgcolor='black')
              #extra_face.background.color = self._tip2color[node.name]

              extra_face.margin_left = 5
              extra_face.margin_top = 5
              extra_face.margin_right = 5
              extra_face.margin_bottom = 5
                   
              add_face_to_node(extra_face, node, column=column_no, position='aligned')
              #add_face_to_node(extra_face, node, column=column_no, aligned = True, position='branch-right')
              column_no += 1
           elif (node.name not in self._tip2info) and self._custom_options["show_common"]:
              #print "No data available"
              extra_face = TextFace("No common name found", fsize=10, fgcolor='red')
         
              extra_face.margin_left = 5
              extra_face.margin_top = 5
              extra_face.margin_right = 5
              extra_face.margin_bottom = 5
              
              add_face_to_node(extra_face, node, column=column_no, position='aligned')
              column_no += 1

           image_col_no = column_no
           #image_col_no = 3#column_no
           #----------------------------------------------
           if (node.name in self._img_chk_list):
              image_local_path = "file://" + image_path
              if self._img_data_dic[node.name] is not None:
                  print(image_local_path + self._img_data_dic[node.name][0]) 
                  img_face = ImgFace(image_local_path + self._img_data_dic[node.name][0], is_url=True)
                  #add_face_to_node(img_face, node, column=3, position='branch-right')
                  #add_face_to_node(img_face, node, column=3, aligned= True, position='branch-right')
              else:
                  print("No image data found")
                  img_face = ImgFace(image_local_path + "/images/ina.jpg", is_url=True)  
              img_face.margin_top = 10
              img_face.margin_right = 10
              img_face.margin_left = 10
              img_face.margin_bottom = 10
              #add_face_to_node(img_face, node, column=5, position='branch-right')
              add_face_to_node(img_face, node, column=image_col_no, position='aligned')
                   
        else: #node is not a leaf
            node.img_style['size'] = 4
            node.img_style['shape'] = 'square'
        
            if node.name and self._custom_options["draw_internal"]:
              name_face = TextFace(node.name, fgcolor='grey', fsize=10)
              #name_face.margin_top = 4
              #name_face.margin_right = 4
              #name_face.margin_left = 4
              #name_face.margin_bottom = 4
              add_face_to_node(name_face, node, column=0, position='branch-top')
            '''
            if node.name in self._node2label: 
               label_face = TextFace(self._node2label[node.name], fgcolor='DarkGreen', fsize=10)
               add_face_to_node(label_face, node, column=0, position="branch-top")
            '''
            if node.support and self._custom_options["draw_support"]:
              support_face = TextFace(node.support, fgcolor='indianred', fsize=10)
              support_face.margin_top = 4
              support_face.margin_right = 4
              support_face.margin_left = 4
              support_face.margin_bottom = 4
              add_face_to_node(support_face, node, column=0, position='branch-bottom')
              
              
            if hasattr(node, "hide") and int(node.hide) == 1:
              node.img_style["draw_descendants"]= False
              collapsed_face = faces.TextFace(" %s collapsed leaves." %len(node), \
                    fsize=10, fgcolor="#444", ftype="Arial")
              faces.add_face_to_node(collapsed_face, node, 0)
            else:
              node.img_style["draw_descendants"] = True

            # Parse node features features and conver them into styles. This must be done like this, since current ete version 
            #does not allow modifying style outside the layout function.
            if hasattr(node, "bsize"):
              node.img_style["size"]= int(node.bsize)

            if hasattr(node, "shape"):
              node.img_style["shape"]= node.shape

            if hasattr(node, "bgcolor"):
              node.img_style["bgcolor"]= node.bgcolor

            if hasattr(node, "fgcolor"):
              node.img_style["fgcolor"]= node.fgcolor
        #parse all nodes features
        
        if hasattr(node, "bh_bgcolor"):
           node.img_style["bgcolor"]= node.bh_bgcolor
        if hasattr(node, "bh_size"):
           node.img_style["size"]= node.bh_size

        if hasattr(node, "lh_color"):
           node.img_style['hz_line_color'] = node.lh_color
           node.img_style["vt_line_color"] = node.lh_color
        
        if hasattr(node, "lh_width"):
           node.img_style['hz_line_width'] = node.lh_width
           node.img_style['vt_line_width'] = node.lh_width

        if hasattr(node, "lh_width") and hasattr(node, "lh_color"):
           for n in node.iter_descendants():
               n.img_style['hz_line_color'] = node.lh_color
               n.img_style["vt_line_color"] = node.lh_color
               n.img_style['hz_line_width'] = node.lh_width
               n.img_style['vt_line_width'] = node.lh_width

#----------------------------------------------
    def show_action_collapse(self, node):
        # Only internal node can be collapsed
        if (not node.is_leaf() and (not hasattr(node, "hide") or node.hide==False)):
           return True
        else:
           return False

#-----------------------------------------------
    def collapse(self,tree, node, status, a_data):
        #can_collapse = lambda node: not node.is_leaf() and (not hasattr(node, "hide") or node.hide==False)
        can_collapse = status
        if can_collapse:
           node.add_feature("hide", 1)
           node.add_feature("bsize", 25)
           node.add_feature("shape", "sphere")
           node.add_feature("fgcolor", "#000080")
#-------------------------------------------------
    def show_action_expand(self, node):
        # Only internal node can be collapsed
        if (not node.is_leaf() and (hasattr(node, "hide") and node.hide==True)):
           return True
        else:
           return False

#--------------------------------------------
    def expand(self,tree, node, status, a_data):
        #can_expand = lambda node: not node.is_leaf() and (hasattr(node, "hide") and node.hide==True)
        can_expand = status
        try:
           if can_expand:
              node.del_feature("hide")
              node.del_feature("bsize")
              node.del_feature("shape")
              node.del_feature("fgcolor")
        except (KeyError, AttributeError):
           pass

#--------------------------------------------
    def show_action_swap(self, node):
        #only nodes with children can be swaped
        if node.is_leaf():
           return False
        else:
           return True
        
    def swap_branches(self,tree, node, status, a_data):
        is_not_leaf = lambda node: not node.is_leaf()
        #print "swap status: "+ str(status) 
        if is_not_leaf and status:
           node.children.reverse()

#--------------------------------------------------
    def show_action_root(self, node):
        if node.up:
           return True
        return False

    def run_action_root(self, tree, node):
        tree.set_outgroup(node)

#---------------------------------------------------    
    def run_action_ladderize(self, tree):
        tree.ladderize()

#--------------------------------------------------
    def show_action_highlight(self, node):
        # Any node can be highlighted
        return True

    def run_action_boxhighlight(self, tree, node, status, a_data):
        #is_highlighted = True if ( hasattr(node, "bh_bgcolor") and hasattr(node, "bh_size") ) else False
        box_highlight = status
        
        if box_highlight:
           node.add_feature("bh_bgcolor", "Yellow")
           #node.add_feature("bh_size", 8) #to remove the misplaced dots appearing 
        else:
           node.add_feature("bh_bgcolor", "White")
           #node.del_feature("bh_size")
        
    def run_action_indvhighlight(self, tree, node, status, a_data):
        #is_highlighted = True if ( hasattr(node, "lh_color") and hasattr(node, "lh_width") ) else False
        line_highlight = status

        if line_highlight:
           node.add_feature("lh_color", "#800000")
           node.add_feature("lh_width", 4)
           self.run_action_change_style(tree, "#800000")
        else:
           node.del_feature("lh_color")#node.add_feature("lh_color", "#000000")
           node.del_feature("lh_width")#node.add_feature("lh_width", 0)
           #self.run_action_change_style(tree, "#000000")
       
#-----------------------------------------------
    def show_action_change_style(self, node):
        return True

    def run_action_change_style(self, tree, a_data):
        #print "action change style called.."        
        if tree.tree_style == self._treestyle:
           ts2 = TreeStyle()
           ts2.layout_fn = self.custom_layout
           ts2.show_leaf_name = False
           ts2.draw_guiding_lines = True
           ts2.guiding_lines_type = 0 #solid line
           ts2.guiding_lines_color = a_data
           if not(self.is_scaled_tree()):
              #print "inside run action set scale to false"
              ts2.show_scale = False
           else:
              ts2.show_scale = True
           tree.tree_style = ts2
           self._treestyle = ts2
        else:
           tree.tree_style = self._treestyle

#-----------------------------------------------
    def show_action_picture(self, node):
        if node.is_leaf():
           return True
        else:
           return False

    def run_action_picture(self, tree, node, status, pic_id):
        if not(node.is_leaf()):
           return -1
        #remove picture"
        if not(status) and (node.name in self._img_chk_list):
           self._img_chk_list.remove(node.name)
           return
 
        if pic_id != -1:
           img_info = get_image_data(node.name, pic_id)
        else:
           img_info = get_image_data(node.name)
        
        if not(is_empty(img_info)) and img_info['thumb_local_path'] != "":
           self._img_data_dic[node.name] = [img_info['thumb_local_path'],img_info['thumb_id']]
           image_id = img_info['thumb_id']
        else:
           self._img_data_dic[node.name] = None
           image_id = 0 #no image available

        #self._tip2info[node.name] = [url, mass, habit]
        if status and (node.name not in self._img_chk_list):
           self._img_chk_list.append(node.name)
           return image_id


    def show_change_picture(self, node):
        #print "change picture called %s" %(node.name)
        if node.is_leaf() and can_change_image(node.name) and (node.name in self._img_chk_list):
           return True
        else:
           return False

    def run_change_picture(self, tree, node, status, img_id):
        #print "run change picture called"
        #print "image_id" + str(img_id)
        img_info = get_image_data(node.name, img_id, status)
        
        if not(is_empty(img_info)) and img_info['thumb_local_path'] != "":
           self._img_data_dic[node.name] = [img_info['thumb_local_path'],img_info['thumb_id']]
           image_id = img_info['thumb_id']
        else:
           self._img_data_dic[node.name] = None
           image_id = 0 #no image available

        return image_id


    #def run_clear_picture(self, tree, node, status):
    #    if status and (node.name in self._img_chk_list):
    #       self._img_chk_list.remove(node.name)

#----------------TREE ACTIONS---------------------------------
    def run_action_linecolorwidth(self, tree, colorcode, linewidth):
        #nstyle["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
        #nstyle["hz_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted 
        if colorcode == '' and linewidth == '':
           return
        elif colorcode != '':
           self.run_action_change_style(tree, colorcode)
        # Applies the same static style to all nodes in the tree. Note that,if "nstyle" is modified, changes will affect to all nodes
        for n in tree.traverse():
            if linewidth != '':
               n.img_style['vt_line_width'] = int(linewidth)
               n.img_style['hz_line_width'] = int(linewidth)
            if colorcode != '':
               n.img_style['hz_line_color'] = colorcode#"#800000"
               n.img_style["vt_line_color"] = colorcode#"#800000"
              
#--------------------------------------------------------------         
    '''
    def change_linecolor(self,aindex, treeid, nodeid, node):
        return """<li><a onClick="myFunction()">Change color</a></li>"""
    '''
#---------------------------------------------------
    def show_eol_link(self, node):
        if node.is_leaf():
           return True
        else:
           return False

    def eol_link(self, aindex, treeid, nodeid, node):        
        if node.name not in self._eol_link_dic:
           eol_link = get_link_data(node.name)        
           self._eol_link_dic[node.name] = eol_link
        else:
           eol_link = self._eol_link_dic[node.name]
        
        if eol_link == "":
           return '''<li style="font-size:12pt">
              No info page available
              </li> '''
        else:
           return '''<li style="font-size:12pt">
              <a target="_blank" href="%s">
              Read info page
              </a>
              </li> ''' %\
              (eol_link)

#=========================Non-Class methods========================

#def get_random_color():
#    r = lambda: random.randint(0,255)
#    return '#%02X%02X%02X' % (r(),r(),r()))
#-----------------------------------------------------
'''
def get_max_value(tipdata_lst):
    data_values = []
    for tip_obj in tipdata_lst:
        tmp_lst = tip_obj['tip_data_values']
        for val in tmp_lst: 
            if isinstance( val,(int,float) ):
               data_values.append(val)

    return max(data_values)
'''
#---------------------------------------------------
#check if any list, dictionary, set, string or tuple is empty in Python
def is_empty(any_structure):
    if any_structure:
       #print('Structure is not empty.')
       return False
    else:
       #print('Structure is empty.')
       return True
#-----------------------------------------------------
def get_link_data(sp_name):
    #service_uri = "https://phylo.cs.nmsu.edu/phylotastic_ws/ds/get_link_info"
    service_uri = "http://data_api:5000/phylotastic_ws/ds/get_link_info"
    service_payload = {'species': sp_name}
    
    service_response = execute_webservice(service_uri, service_payload)
    link = ""
    if service_response is not None:    
        link = service_response["eol_link"]

    return link

#-----------------------------------------------------
def get_image_data(sp_name, img_id=0, next_img=False):
    #service_uri = "https://phylo.cs.nmsu.edu/phylotastic_ws/ds/get_image_info"
    service_uri = "http://data_api:5000/phylotastic_ws/ds/get_image_info"
    service_payload = {'species': sp_name, 'image_id': img_id, 'next_image': next_img}
   
    service_response = execute_webservice(service_uri, service_payload)
    
    if service_response is not None:
       image = service_response
    else:
       image = {}

    return image

#----------------------------------------------------
def can_change_image(sp_name):
    #service_uri = "https://phylo.cs.nmsu.edu/phylotastic_ws/ds/image_info_exists"
    service_uri = "http://data_api:5000/phylotastic_ws/ds/image_info_exists"
    service_payload = {'species': sp_name}
   
    service_response = execute_webservice(service_uri, service_payload)
      
    if service_response is not None:
       has_img_info = service_response['image_info_exists']
       #print service_response['image_info']
       if 'image_info' in service_response: 
          img_count = len(service_response['image_info'])
       else:
          img_count = 0 
          
       if has_img_info and img_count > 1:
          can_change_img = True
       else:
          can_change_img = False        
    else:
       can_change_img = False
    
    return can_change_img

#-----------------------------------------------------------
def execute_webservice(service_url, service_payload):
    response = requests.get(service_url, params=service_payload)
    
    if response.status_code == requests.codes.ok:    
        res_json = json.loads(response.text)
    else:
        res_json = None

    return res_json 
