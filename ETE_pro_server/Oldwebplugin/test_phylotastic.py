from ete3_webserver import NodeActions, start_server
from ete3 import TreeStyle, TextFace, add_face_to_node, ImgFace, BarChartFace

# Custom ETE Tree styles and web actions
image_checker = {'Rangifer_tarandus': True}

def show_action_root(node):
    if node.up:
        return True
    return False

def run_action_root(tree, node):
    tree.set_outgroup(node)

def show_action_highlight(node):
    # Any node can be highlighted
    return True

def run_action_highlight(tree, node):
    node.img_style['bgcolor'] = 'pink'
    node.img_style['size'] = 8
    node.img_style['hz_line_width'] = 4

def show_action_change_style(node):
    return True

def run_action_change_style(tree, node):
    if tree.tree_style == ts:
        tree.tree_style = ts2
    else:
        tree.tree_style = ts

#--------------------------------
def show_action_linecolor(node):
    # Any node can be colored
    return True

def run_action_linecolor(tree, node):
    #nstyle = NodeStyle()
    #nstyle["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
    #nstyle["vt_line_color"] = "#4253a1"
    #nstyle["vt_line_width"] = 2 
    
    #nstyle["hz_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
    #nstyle["hz_line_color"] = "#4253a1"
    #nstyle["hz_line_width"] = 2 

    # Applies the same static style to all nodes in the tree. Note that,
    # if "nstyle" is modified, changes will affect to all nodes
    #for n in t.traverse():
    #    n.set_style(nstyle)
    node.img_style['hz_line_color'] = "#4253a1"
    node.img_style["vt_line_color"] = "#4253a1"

def change_linecolor(aindex, treeid, nodeid, node):
    return """<li><a onClick="myFunction()">Change color</a></li>"""

#-----------------------------------
def show_eol_link(node):
    return True

#-----------------------------------
def eol_link(aindex, treeid, nodeid, node):
    return '''<li>
          <a target="_blank" href="http://www.ensembl.org/">
          <img src="" alt=""> Search in eol: %s >
          </a>
          </li> ''' %\
          (node.name)

#-------------------------------------------
def custom_layout(node):
    if node.is_leaf():
        aligned_name_face = TextFace(node.name, fgcolor='olive', fsize=14)
        add_face_to_node(aligned_name_face, node, column=2, position='aligned')
        name_face = TextFace(node.name, fgcolor='#333333', fsize=11)
        add_face_to_node(name_face, node, column=2, position='branch-right')
        node.img_style['size'] = 0

        if (node.name in tip2info) and (node.name in image_checker):
            # image
            img_face = ImgFace(tip2info[node.name][0], is_url=True)
            add_face_to_node(img_face, node, column=4, position='branch-right')

            habitat_face = TextFace(tip2info[node.name][2], fsize=11, fgcolor='white')
            habitat_face.background.color = 'steelblue'
            habitat_face.margin_left = 3
            habitat_face.margin_top = 3
            habitat_face.margin_right = 3
            habitat_face.margin_bottom = 3
            add_face_to_node(habitat_face, node, column=3, position='aligned')
    else:
        node.img_style['size'] = 4
        node.img_style['shape'] = 'square'
        if node.name:
            name_face = TextFace(node.name, fgcolor='grey', fsize=10)
            name_face.margin_bottom = 2
            add_face_to_node(name_face, node, column=0, position='branch-top')
        if node.support:
            support_face = TextFace(node.support, fgcolor='indianred', fsize=10)
            add_face_to_node(support_face, node, column=0, position='branch-bottom')

tip_info_csv = """
Rangifer_tarandus,http://media.eol.org/content/2014/05/02/09/88803_98_68.jpg,109.09,herbivore
Cervus_elaphus,http://media.eol.org/content/2013/02/22/16/31998_98_68.jpg,240.87,herbivore
Bos_taurus,http://media.eol.org/content/2014/09/29/06/46535_98_68.jpg,618.64,herbivore
Ovis_orientalis,http://media.eol.org/content/2015/01/04/05/30107_98_68.jpg,39.1,herbivore
Suricata_suricatta,http://media.eol.org/content/2012/06/19/04/84840_98_68.jpg,0.73,carnivore
Mephitis_mephitis,http://media.eol.org/content/2012/08/30/16/23686_98_68.jpg,2.4,omnivore"""
tip2info = {}
for line in tip_info_csv.split('\n'):
    if line:
        name, url, mass, habit = map(str.strip, line.split(','))
        tip2info[name] = [url, mass, habit]


# Server configuration

ts = TreeStyle()
ts.layout_fn = custom_layout
ts.show_leaf_name = False

ts2 = TreeStyle()

actions = NodeActions()

actions.add_action('Root here', show_action_root, run_action_root, None)
actions.add_action('Highlight', show_action_highlight, run_action_highlight, None)
actions.add_action('Change style', show_action_change_style, run_action_change_style, None)
actions.add_action('EOL link', show_eol_link, None, eol_link)
actions.add_action('Change color', show_action_linecolor, None, change_linecolor)

start_server(node_actions=actions, tree_style=ts)
