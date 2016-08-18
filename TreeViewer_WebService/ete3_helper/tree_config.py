from tree_handler import NodeActions
from ete3 import TreeStyle, NodeStyle, TextFace, add_face_to_node, ImgFace, BarChartFace
import os, json
import requests

# Custom ETE Tree styles and web actions
image_dir = "/var/web_service/TreeViewer/img/"


class WebTreeConfig(object):
    def __init__(self, treeobj, tid):
        self._treeobj = treeobj
        self._treeid = tid
        self._treestyle = None
        self._tree_leaves = [leaf.name for leaf in treeobj.iter_leaves()]
        self._tip2info = {}
        self._img_chk_list = []
        self._img_data_dic = {}
        #self.get_node_data()
    
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
        act.add_action('BoxHighlight', self.show_action_highlight, self.run_action_boxhighlight, None)
        act.add_action('IndividualHighlight', self.show_action_highlight, self.run_action_indvhighlight, None)
        #act.add_action('Change style', self.show_action_change_style, self.run_action_change_style, None)
        #act.add_action('EOL link', self.show_eol_link, None, self.eol_link)
        #act.add_action('Change line thickness', self.show_action_linethickness, self.run_action_linethickness, None)
        #act.add_action('Change line color', self.show_action_linecolor, None, self.change_linecolor)
        act.add_action('Display picture', self.show_action_picture, self.run_action_picture, None)
        act.add_action('Hide picture', self.show_action_picture, self.run_clear_picture, None)

        return act

    def get_node_data(self):
        #print self._tree_leaves 
        tip_info_csv = """
           Rangifer_tarandus,http://media.eol.org/content/2014/05/02/09/88803_98_68.jpg,109.09,herbivore
           Cervus_elaphus,http://media.eol.org/content/2013/02/22/16/31998_98_68.jpg,140.87,herbivore
           Bos_taurus,http://media.eol.org/content/2014/09/29/06/46535_98_68.jpg,97.64,herbivore
           Ovis_orientalis,http://media.eol.org/content/2015/01/04/05/30107_98_68.jpg,39.1,herbivore
           Suricata_suricatta,http://media.eol.org/content/2012/06/19/04/84840_98_68.jpg,50.73,carnivore
           Mephitis_mephitis,http://media.eol.org/content/2012/08/30/16/23686_98_68.jpg,25.4,omnivore"""

        for line in tip_info_csv.split('\n'):
            if line:
               name, url, mass, habit = map(str.strip, line.split(','))
               self._tip2info[name] = [url, mass, habit]
        

#------------------------------------------        
    def custom_layout(self,node):
        if node.is_leaf():
           aligned_name_face = TextFace(node.name, fgcolor='olive', fsize=14)
           aligned_name_face.margin_top = 5
           aligned_name_face.margin_right = 5
           aligned_name_face.margin_left = 5
           aligned_name_face.margin_bottom = 5
           aligned_name_face.hz_align = 0     #0 = left, 1 = center, 2 = right 
           add_face_to_node(aligned_name_face, node, column=3, position='aligned')
           name_face = TextFace(node.name, fgcolor='#333333', fsize=11)
           name_face.margin_top = 3
           name_face.margin_right = 3
           name_face.margin_left = 3
           name_face.margin_bottom = 3 
           add_face_to_node(name_face, node, column=2, position='branch-right')
           node.img_style['size'] = 0

           #if (node.name in self._tip2info):
              # image
               
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
                  #add_face_to_node(img_face, node, column=5, position='aligned')
                  #add_face_to_node(img_face, node, column=3, aligned= True, position='branch-right')
              else:
                  img_path = os.path.join("file://"+image_dir, "ina.jpg")
                  img_face = ImgFace(img_path, is_url=True)  
              
              add_face_to_node(img_face, node, column=3, position='branch-right')

              #habitat_face = TextFace(self._tip2info[node.name][2], fsize=11, fgcolor='white')
              #habitat_face.background.color = 'steelblue'
              #habitat_face.margin_left = 5
              #habitat_face.margin_top = 5
              #habitat_face.margin_right = 5
              #habitat_face.margin_bottom = 5
              #add_face_to_node(habitat_face, node, column=4, position='aligned')
              #add_face_to_node(habitat_face, node, column=4, aligned = True, position='branch-right')

              #massbar_face = BarChartFace([self._tip2info[node.name][1]], width=50, height=25,colors=['navy'], labels=['Mass'], min_value=0.0, max_value=200.0)
              #add_face_to_node(massbar_face, node, column=4, position='aligned')
        else:
            node.img_style['size'] = 4
            node.img_style['shape'] = 'square'
        
            if node.name:
              name_face = TextFace(node.name, fgcolor='grey', fsize=10)
              name_face.margin_top = 4
              name_face.margin_right = 4
              name_face.margin_left = 4
              name_face.margin_bottom = 4
              add_face_to_node(name_face, node, column=0, position='branch-top')
            if node.support:
              support_face = TextFace(node.support, fgcolor='indianred', fsize=10)
              support_face.margin_top = 4
              support_face.margin_right = 4
              support_face.margin_left = 4
              support_face.margin_bottom = 4
              add_face_to_node(support_face, node, column=0, position='branch-bottom')

#--------------------------------------------------
    def show_action_root(self, node):
        if node.up:
           return True
        return False

    def run_action_root(self, tree, node):
        tree.set_outgroup(node)

#--------------------------------------------------
    def show_action_highlight(self, node):
        # Any node can be highlighted
        return True

    def run_action_boxhighlight(self, tree, node):
        node.img_style['bgcolor'] = 'Yellow'
        node.img_style['size'] = 8
        #node.img_style['hz_line_width'] = 4

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
        return True

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
#-----------------------------------
    def show_eol_link(self, node):
        return True

    def eol_link(self, aindex, treeid, nodeid, node):
        return '''<li>
          <a target="_blank" href="http://www.eol.org/">
          <img src="" alt=""> Search in eol: %s
          </a>
          </li> ''' %\
          (node.name)

#-------------------------------------------
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

def execute_webservice(service_url, service_payload):
    response = requests.post(service_url, data=service_payload, headers={'content-type': 'application/json'})
    
    if response.status_code == requests.codes.ok:    
        res_json = json.loads(response.text)
    else:
        res_json = None

    return res_json 
