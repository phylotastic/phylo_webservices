from tree_handler import NodeActions
from ete3 import TreeStyle, NodeStyle, TextFace, add_face_to_node, ImgFace, BarChartFace, faces
import os, json
import requests
import random

# Custom ETE Tree styles and web actions
image_path = "/var/web_service/TayeenFolders/TreeViewer/webplugin_test/data/"

class WebTreeConfig(object):
    def __init__(self, treeobj, tid):
        self._treeobj = treeobj
        self._treeid = tid
        self._treestyle = None
        self._tree_leaves = [leaf.name for leaf in treeobj.iter_leaves()]
        self._tip2info = {}
        self._tip2color = {}
        self._tip2headers = None
        self._tip_max = 0.0
        self._node2label = {}
        self._img_chk_list = []
        self._img_data_dic = {}
        self._eol_link_dic = {}

    
    def get_tree_style(self):
        ts = TreeStyle()
        ts.layout_fn = self.custom_layout
        ts.show_leaf_name = False
        ts.draw_guiding_lines = True
        #ts.guiding_lines_type = 1
        self._treestyle = ts
        return ts

    def get_node_action(self):
        act = NodeActions()
        #act.add_action('Root here', self.show_action_root, self.run_action_root, None)
        act.add_action('Box Highlight', self.show_action_highlight, self.run_action_boxhighlight, None)
        act.add_action('Line Highlight', self.show_action_highlight, self.run_action_indvhighlight, None)
        #act.add_action('Change style', self.show_action_change_style, self.run_action_change_style, None)
        act.add_action('EOL link', self.show_eol_link, None, self.eol_link)
        act.add_action('Display picture', self.show_action_picture, self.run_action_picture, None)
        act.add_action('Hide picture', self.show_action_picture, self.run_clear_picture, None)
        act.add_action('Collapse', self.show_action_collapse, self.collapse, None)
        act.add_action('Expand', self.show_action_collapse, self.expand, None)
        act.add_action('Swap children',self.show_action_swap,self.swap_branches,None)

        return act

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
         
#------------------------------------------        
    def custom_layout(self,node):
        if node.is_leaf():
           aligned_name_face = TextFace(node.name, fgcolor='olive', fsize=12)
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

           image_col_no = column_no
           #----------------------------------------------
           if (node.name in self._img_chk_list):
              if self._img_data_dic[node.name] is not None:
                  img_face = ImgFace(self._img_data_dic[node.name], is_url=True)
                  #img_face = ImgFace(self._tip2info[node.name][0], is_url=True)
                  #img_path = os.path.join("file:///home/tayeen/TayeenFolders/TreeViewer/WebTreeApp/newplugin_test/data/", "328653.jpg")
                  #img_face = ImgFace(img_path, is_url=True)
                  img_face.margin_top = 10
                  img_face.margin_right = 10
                  img_face.margin_left = 10
                  img_face.margin_bottom = 10
                  #add_face_to_node(img_face, node, column=3, position='branch-right')
                  #add_face_to_node(img_face, node, column=3, aligned= True, position='branch-right')
              else:
                  img_path = os.path.join("file://"+image_path, "ina.jpg")
                  img_face = ImgFace(img_path, is_url=True)  
              
              #add_face_to_node(img_face, node, column=5, position='branch-right')
              add_face_to_node(img_face, node, column=image_col_no, position='aligned')
                   
        else: #node is not a leaf
            node.img_style['size'] = 4
            node.img_style['shape'] = 'square'
        
            if node.name:
              name_face = TextFace(node.name, fgcolor='grey', fsize=10)
              name_face.margin_top = 4
              name_face.margin_right = 4
              name_face.margin_left = 4
              name_face.margin_bottom = 4
              add_face_to_node(name_face, node, column=0, position='branch-top')
            
            if node.name in self._node2label: 
               label_face = TextFace(self._node2label[node.name], fgcolor='DarkGreen', fsize=10)
               label_face.margin_top = 4
               label_face.margin_right = 4
               label_face.margin_left = 4
               label_face.margin_bottom = 4
               add_face_to_node(label_face, node, column=0, position="branch-top")
            
            if node.support:
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
#----------------------------------------------
    def show_action_collapse(self, node):
        # Only internal node can be collapsed
        if node.is_leaf():
           return False
        else:
           return True

#-----------------------------------------------
    def collapse(self,tree,node):
        can_collapse = lambda node: not node.is_leaf() and (not hasattr(node, "hide") or node.hide==False)
        if can_collapse:
           node.add_feature("hide", 1)
           node.add_feature("bsize", 25)
           node.add_feature("shape", "sphere")
           node.add_feature("fgcolor", "#000080")
#-------------------------------------------------
    def expand(self,tree,node):
        can_expand = lambda node: not node.is_leaf() and (hasattr(node, "hide") and node.hide==True)
        try:
           if can_expand:
              node.del_feature("hide")
              node.del_feature("bsize")
              node.del_feature("shape")
              node.del_feature("fgcolor")
        except (KeyError, AttributeError):
           pass

#---------------------------------------
    def show_action_swap(self, node):
        #only nodes with children can be swaped
        if node.is_leaf():
           return False
        else:
           return True
        
    def swap_branches(self,tree,node):
        is_not_leaf = lambda node: not node.is_leaf()
        if is_not_leaf:
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

    def run_action_boxhighlight(self, tree, node):
        is_highlighted = True if ( hasattr(node, "bh_bgcolor") and hasattr(node, "bh_size") ) else False
        
        if is_highlighted:
           node.add_feature("bh_bgcolor", "White")
           node.del_feature("bh_size")
        else:
           node.add_feature("bh_bgcolor", "Yellow")
           node.add_feature("bh_size", 8)
        #node.img_style['bgcolor'] = 'Yellow'
        #node.img_style['size'] = 8
        

    def run_action_indvhighlight(self, tree, node):
        node.img_style['hz_line_color'] = "#800000"
        node.img_style["vt_line_color"] = "#800000"
        node.img_style['hz_line_width'] = 4
        node.img_style['vt_line_width'] = 4
        for n in node.iter_descendants():
            n.img_style['hz_line_color'] = "#800000"
            n.img_style["vt_line_color"] = "#800000"
            n.img_style['hz_line_width'] = 4
            n.img_style['vt_line_width'] = 4
        #node.img_style['size'] = 4

#-----------------------------------------------
    def show_action_change_style(self, node):
        return True

    def run_action_change_style(self, tree, node):
        if tree.tree_style == self._treestyle:
           ts2 = TreeStyle()
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

    def run_action_picture(self, tree, node):
        #print "executing run action picture....."
        tip_img_url = get_image_data(node.name)
        self._img_data_dic[node.name] = tip_img_url
        #self._tip2info[node.name] = [url, mass, habit]
        if node.name not in self._img_chk_list:
           self._img_chk_list.append(node.name)

    def run_clear_picture(self, tree, node):
        if node.name in self._img_chk_list:
           self._img_chk_list.remove(node.name)

#----------------TREE ACTIONS---------------------------------
    def run_action_linecolorwidth(self, tree, colorcode, linewidth):
        #nstyle["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
        #nstyle["hz_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted 
        if colorcode == '' and linewidth == '':
           return

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

        return '''<li>
              <a target="_blank" href="%s">
              <b>EOL link: <i>%s</i></b>
              </a>
              </li> ''' %\
              (eol_link, node.name)

#=========================Non-Class methods========================

#def get_random_color():
#    r = lambda: random.randint(0,255)
#    return '#%02X%02X%02X' % (r(),r(),r()))
#-----------------------------------------------------
def get_max_value(tipdata_lst):
    data_values = []
    for tip_obj in tipdata_lst:
        tmp_lst = tip_obj['tip_data_values']
        for val in tmp_lst: 
            if isinstance( val,(int,float) ):
               data_values.append(val)

    return max(data_values)

#-----------------------------------------------------
def get_image_data(tip_name):
    image_service_uri = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/images"
    image_service_payload = {'species': [tip_name]}
    #print "Executing service..."
    service_response = execute_webservice(image_service_uri, json.dumps(image_service_payload))
    img_lst_len = len(service_response['species'][0]['images'])
    if img_lst_len != 0:
       tip_img_url = service_response['species'][0]['images'][0]['eolThumbnailURL']
    else:
       tip_img_url = None

    return tip_img_url

#--------------------------------------------------------------
def get_link_data(tip_name):
    eol_service_uri = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/sl/eol/links"
    eol_service_payload = {'species': [tip_name]}
    #print "Executing service..."
    service_response = execute_webservice(eol_service_uri, json.dumps(eol_service_payload))
    if service_response['species'][0]['matched_name'] == '':
       tip_eol_url = None
    else:
       tip_eol_url = service_response['species'][0]['species_info_link']

    return tip_eol_url


#-----------------------------------------------------------
def execute_webservice(service_url, service_payload):
    response = requests.post(service_url, data=service_payload, headers={'content-type': 'application/json'})
    
    if response.status_code == requests.codes.ok:    
        res_json = json.loads(response.text)
    else:
        res_json = None

    return res_json 
