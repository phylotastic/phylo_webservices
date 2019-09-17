#from distutils.util import strtobool
from ete3 import Tree, TreeStyle
from ete3.parser.newick import NewickError

from tree_handler import WebTreeHandler, NodeActions, TreeStyle
from tree_config import WebTreeConfig
import types
import json
#from IPython import embed

TREE_HANDLER = WebTreeHandler
TREE_CONFIG = WebTreeConfig

def create_tree_obj(tree_newick, tree_id, node_data=None):

    tree_handler_obj = TREE_HANDLER(tree_newick, tree_id)
    newick_checker = tree_handler_obj.parse_newick()

    if type(newick_checker) != types.BooleanType:
       return {"message:":newick_checker, "status_code": 500}
    
    tree_config_obj = TREE_CONFIG(tree_handler_obj.tree, tree_id)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #add node data to tree
    if node_data is not None:
       #print "node data is not none"
       data_dict =  ast.literal_eval(node_data.strip())
       #print data_dict
       #data_json = json.loads(node_data)
       #print data_json
       tree_config_obj.set_extra_tipdata(data_dict)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #set default actions and styles
    tree_handler_obj.set_actions(tree_config_obj.get_node_action())
    tree_handler_obj.set_style(tree_config_obj.get_tree_style())
    
    tree_handler_obj.set_tree_config(tree_config_obj)
    
    return tree_handler_obj

#------------------------------------------------------
def apply_actions(tree_handler, actions_dic, top_offset=0, left_offset=0):

    new_dic = {'tree_newick':tree_handler.treenewick, 'tree_id':tree_handler.treeid, 'actions': {}}
    #check whether any tree action exists
    if 'tree_actions' in actions_dic and (not is_empty(actions_dic['tree_actions'])):
       tree_actions = actions_dic['tree_actions']      
       new_dic['actions']['tree_actions'] = apply_tree_actions(tree_handler, tree_actions)
    #check whether any node action exists
    if 'node_actions' in actions_dic and (not is_empty(actions_dic['node_actions'])):
       node_actions_dic = actions_dic['node_actions']
       node_actions = apply_node_pre_actions(tree_handler, node_actions_dic, actions_dic['latest_action_node_id'])
       new_dic['actions']['node_actions'] = apply_node_actions(tree_handler, node_actions)

    # Renders tree using ETEtoolkit
    html_img = tree_handler.redraw(top_offset, left_offset) 
    new_dic['html_data'] = html_img

    #print new_dic
    return new_dic

#-------------------------------------------------------------
def apply_tree_actions(tree_handler, tree_actions_dic):
    new_tree_actions_dic = {}
    #print "tree_actions dict"
    #print type(tree_actions_dic)
    try:
       tree_actions_dic = json.loads(tree_actions_dic)
    except:
       tree_actions_dic = tree_actions_dic
    #embed()
    if (is_empty(tree_actions_dic)):
       return new_tree_actions_dic
 
    line_color = tree_actions_dic['line_color']
    line_width = tree_actions_dic["line_width"]
    #set default values for line colors and line width
    if line_color == '':
       line_color = "black"
    if line_width == '':
       line_width = "1"

    tree_handler.run_tree_action(line_color, line_width)
    #update tree_actions dictionary
    new_tree_actions_dic['line_color'] = line_color
    new_tree_actions_dic['line_width'] = line_width

    ladderize = False
    if 'ladderize' in tree_actions_dic:
        ladderize = tree_actions_dic['ladderize']
        
    show_branch_length = False
    if 'show_branch_length' in tree_actions_dic: 
        show_branch_length = tree_actions_dic['show_branch_length']

    show_internal_node = False
    if 'show_internal_node' in tree_actions_dic: 
        show_internal_node = tree_actions_dic['show_internal_node']

    #~~~~~~~~~~~~~~common name~~~~~~~~~~~~~~~~
    show_common_name = False
    if 'show_common_names' in tree_actions_dic: 
        show_common_name = tree_actions_dic['show_common_names']
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          
    tree_handler.run_tree_customize(show_branch_length, show_internal_node, ladderize)
    #update tree_actions dictionary
    new_tree_actions_dic['show_branch_length'] = show_branch_length
    new_tree_actions_dic['show_internal_node'] = show_internal_node
    new_tree_actions_dic['ladderize'] = ladderize  
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    new_tree_actions_dic['show_common_names'] = show_common_name
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      
   
    return new_tree_actions_dic

#-----------------------------------------------------
def set_all_picture_action(tree_handler, node_actions_dic):
 	leaves = tree_handler.get_tree_leaves()
 	leaf_ids = [leaf._nid for leaf in leaves]
 	if node_actions_dic is None:
 		node_actions_dic = []

 	if len(node_actions_dic) == 0:
 		for nid in leaf_ids:
 			node_action = {'node_id': nid, 'display_picture': True}
 			node_actions_dic.append(node_action)
 	else:
 		#update existing node property
 		for n_index, n_action in enumerate(node_actions_dic):
 			node_id = int(n_action['node_id'])        
        	if node_id in leaf_ids:
 				node_actions_dic[n_index]['display_picture'] = True
 				leaf_ids.remove(node_id)
 		#insert new nodes display property
 		for lv_id in leaf_ids:
 			new_node_actions = {"node_id": lv_id, "display_picture": True}
 			node_actions_dic.append(new_node_actions)

 	return node_actions_dic
    
#--------------------------------------------------------
def apply_node_pre_actions(tree_handler, node_actions_dic, latest_action_node_id):
 	box_highlights = {}
        try:
           node_actions_dic = json.loads(node_actions_dic)
        except:
           node_actions_dic = node_actions_dic

 	new_node_actions_dic = node_actions_dic
 	
 	for n_action in new_node_actions_dic:
 		node_id = n_action['node_id']
 		if node_id == latest_action_node_id and 'box_highlight' in n_action:
 			ds_nodes = tree_handler.get_node_descendants(node_id)
 			box_highlights[int(node_id)] = [[dsnode._nid for dsnode in ds_nodes],n_action['box_highlight']]
 	
 	for key in sorted(box_highlights.iterkeys(),reverse=True):
 		hglight_nodes = box_highlights[key][0]
 		hg_property = box_highlights[key][1]
 		for n_index, n_action in enumerate(new_node_actions_dic):
 			node_id = n_action['node_id']
 			if int(node_id) in hglight_nodes:
 				new_node_actions_dic[n_index]['box_highlight'] = hg_property

 	return new_node_actions_dic

#---------------------------------------------------------------
def apply_node_actions(tree_handler, node_actions_dic):
    node_actions_list = []
    #node_actions_dic = json.loads(node_actions_dic)

    for n_action in node_actions_dic:
        node_id = n_action['node_id']
        new_node_actions_dic = {}
        box_highlight = False
        if 'box_highlight' in n_action:
           box_highlight = n_action['box_highlight']
           aindex = 'Box_Highlight'
           tree_handler.run_action(aindex, node_id, box_highlight)

        line_highlight = False
        if 'line_highlight' in n_action:
           line_highlight = n_action['line_highlight']
           aindex = 'Line_Highlight'
           #print "run action called in apply node actions"
           tree_handler.run_action(aindex, node_id, line_highlight)

        collapse = False
        if 'collapse' in n_action:
           collapse = n_action['collapse']
        aindex = 'Collapse' if collapse else 'Expand'
        if not(collapse):
           tree_handler.run_action(aindex, node_id, True) # expand 
        else:
           tree_handler.run_action(aindex, node_id, collapse)

        swap_children = False
        if 'swap_children' in n_action: 
           swap_children = n_action['swap_children']
           aindex = 'Swap_Children'
           tree_handler.run_action(aindex, node_id, swap_children) 
        
        pic_id = -1
        if 'picture_id' in n_action:
           pic_id = n_action['picture_id']

        display_picture = False
        if 'display_picture' in n_action:
           display_picture = n_action['display_picture']
           aindex = 'Display_Picture'
           pic_id = tree_handler.run_action(aindex, node_id, display_picture, pic_id) 
           
        change_picture = False
        if 'change_picture' in n_action:
           change_picture = n_action['change_picture']
           aindex = 'Change_Picture'
           pic_id = n_action['picture_id']
           pic_id = tree_handler.run_action(aindex, node_id, change_picture, pic_id) 
        
        #print " nodeid: " + str(nodeid) + " aindex: " + str(aindex)
        new_node_actions_dic['node_id'] = node_id
        new_node_actions_dic['node_name'] = tree_handler.get_node_name(node_id)
        new_node_actions_dic['box_highlight'] = box_highlight
        #new_node_actions_dic['line_highlight'] = line_highlight
        new_node_actions_dic['collapse'] = collapse
        new_node_actions_dic['swap_children'] = swap_children
        new_node_actions_dic['display_picture'] = display_picture
        if display_picture:
           new_node_actions_dic['picture_id'] = pic_id

        node_actions_list.append(new_node_actions_dic)
    
    return node_actions_list

#-------------------------------------------------
#check if any list, dictionary, set, string or tuple is empty in Python
def is_empty(any_structure):
    if any_structure:
       print('Structure is not empty.')
       return False
    else:
       print('Structure is empty.')
       return True
