/*  it requires jquery loaded */
var ete_webplugin_URL = "https://phylo.cs.nmsu.edu/ete_dev";
var loading_img = '<img border=0 src="https://phylo.cs.nmsu.edu/treeviewer/loader.gif">';

var current_tree_id = "";
var current_tree_newick = "";
var node_actions_list = [];
//for common names
var node_data = null;
var tree_actions = {};
var latest_action_node_id = "";
var tree_state_changed = false;

function update_server_status(){
  console.log('updating');
  $('#server_status').load(ete_webplugin_URL+"/status");

}
//------------------------------------------
function save_tree_image(){
  $('#svg_image').html(loading_img);
  format = $('input[name="format"]:checked').val();
  console.log("save image called");
  xhr = new XMLHttpRequest();
  var url = ete_webplugin_URL+'/save_tree_image';
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
        var hres = JSON.parse(xhr.responseText);
	$('#svg_image').html("");
        $('#svg_image').append(hres.html_data);
        $('#svg_image').on('click', 'a', function() {  
                var redirectWindow = window.open($('#svg_image').children('a').attr('href'), '_blank');
	})
        console.log($('#svg_image').children('a').attr('href'));
        $('#svg_image').children('a').click();
    }
  }
  //parameters for POST request 
  var params = JSON.stringify({"tree_newick": current_tree_newick,"tree_id":current_tree_id, "actions":{"tree_actions": tree_actions, "node_actions": node_actions_list, "latest_action_node_id":latest_action_node_id},"format": format, "node_data":node_data});
  xhr.send(params); 
}

//----------------------------------------------------
function get_tree_image(treeid, newick, recipient, data, topOffset, leftOffset){
  topOffset = (typeof topOffset !== 'undefined') ? topOffset : 0;
  leftOffset = (typeof leftOffset !== 'undefined') ? leftOffset : 0;
  //console.log("topoffset:"+topOffset+" leftoffset:"+leftOffset);
  //console.log("treeid:"+treeid+" current_treeid:"+current_tree_id);
  //console.log("This is dev test");
  if (current_tree_id != treeid)
  {
     node_actions_list = [];
     tree_actions = {};
     latest_action_node_id = ""; 
  } 
  current_tree_id = treeid;
  current_tree_newick = newick;
  if (data === undefined) {
     node_data = null;
  }
  else{
     node_data = data;
  }
  //console.log("recipient:" + recipient);
  //console.log("get tree image called");
  if (recipient != ''){
     $(recipient).html('<div id="' + treeid + '">' + loading_img + '</div>');
     //node_actions_list = [];
     //tree_actions = {};
     //latest_action_node_id = "";
  }
  
  xhr = new XMLHttpRequest();
  var url = ete_webplugin_URL+'/get_tree_image';
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () { 
    if (xhr.readyState == 4 && xhr.status == 200) {
        var hres = JSON.parse(xhr.responseText);
        //update the global tree actions
        var ta = hres.actions["tree_actions"];
        if (typeof(ta) != "undefined"){ 
           tree_actions = ta;
           //console.log("ta:"+JSON.stringify(tree_actions));
        }
        //update the global node actions
        var na = hres.actions["node_actions"];
        if (typeof(na) != "undefined"){
           node_actions_list = na;
           //console.log("na:"+JSON.stringify(node_actions_list));
        }
        //console.log("na: "+typeof(na)); 
        $('#'+treeid).html(hres.html_data);
        $('#'+treeid).fadeTo(100, 0.9);
    }
  }
  //parameters for POST request 
  var params = JSON.stringify({"tree_newick": newick,"tree_id":treeid, 'top_offset': topOffset, 'left_offset': leftOffset, "actions":{"tree_actions": tree_actions, "node_actions": node_actions_list, "latest_action_node_id":latest_action_node_id}, "node_data": node_data});
  xhr.send(params);
}

//-----------------------------------------
function show_actions(treeid, nodeid){
  $("#popup").html(loading_img);
  xhr = new XMLHttpRequest();
  var url = ete_webplugin_URL+'/get_actions';
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
        var hres = JSON.parse(xhr.responseText);
        //console.log("html_data: "+hres.html_data);
        $('#popup').html(hres.html_data);
    }
  }
  //parameters for POST request 
  var params = JSON.stringify({"tree_newick": current_tree_newick,"tree_id":current_tree_id,"node_actions": node_actions_list, "node_id":nodeid});
  xhr.send(params);
  
}
//------------Node Action---------------------------
function run_action(treeid, nodeid, aindex){
  $("#popup").hide();
  $('#'+treeid).html(loading_img);
  //console.log(treeid, nodeid, faceid, aindex, $('#'+treeid));
  latest_action_node_id = nodeid;
  //console.log("nodeid type:"+typeof(nodeid));
  tree_state_changed = true;
  update_node_action(nodeid, aindex);
  //console.log("runaction called..na:"+JSON.stringify(node_actions_list));
  get_tree_image(current_tree_id, current_tree_newick,'', node_data);
}

//----------------------------------------
function update_node_action(nodeid, aindex){
  //console.log("update node action called");
  var len = node_actions_list.length;
  var node_found = false;
  aindex = aindex.toLowerCase();
  //console.log("aindex: "+aindex+" nodeid: "+nodeid);
  alter_actions = ["expand"]
  for (i=0; i < len; i++){
     node_action_obj = node_actions_list[i];
     node_id = node_action_obj["node_id"];
     //update action of an existing node
     if (node_id == nodeid){
        node_found = true;
        if (aindex in node_action_obj){
           action_val = node_action_obj[aindex];
           node_action_obj[aindex] = !action_val;
        } 
        else{
           ain = alter_actions.indexOf(aindex);
           //if (ain != -1 && aindex == alter_actions[0]){
           //   node_action_obj["display_picture"] = false;
           //}
           if(ain != -1 && aindex == alter_actions[0]){
              node_action_obj["collapse"] = false;
           }
           else{
              node_action_obj[aindex] = true;
           }
        }
     }
  }//end of for
  //add action of a new node
  if (!node_found){
    node_action = {};
    node_action["node_id"] = nodeid;

    ain = alter_actions.indexOf(aindex);
    //if (ain != -1 && aindex == alter_actions[0]){
    //   node_action["display_picture"] = false;
    //}
    if(ain != -1 && aindex == alter_actions[0]){
       node_action["collapse"] = false;
    }
    else
       node_action[aindex] = true;
    node_actions_list.push(node_action);
  }
  //console.log(JSON.stringify(node_actions_list));
}
//-------------TreeAction------------------------
function run_tree_action() {
    colorcode = document.getElementsByName("color")[0].value;
    linewidth = $('#line-weight').val();
    //linewidth = $('select[name="lwidth"]:checked').val();
    /*if(document.getElementById('ladderize').checked){
        ladderize = true;
    }else{
        ladderize = false;
    }*/
    tree_state_changed = true;
    ladderize = $("#ladderize").is(':checked');
    showbranch = $("#branch").is(':checked');
    showinternal = $("#internal").is(':checked');
    showcommon = $("#common").is(':checked');
    $('#'+current_tree_id).html(loading_img);

    tree_actions = {"line_color":colorcode,"line_width": linewidth ,"ladderize": ladderize, "show_branch_length": showbranch, "show_internal_node": showinternal, "show_common_names": showcommon};
    //console.log(JSON.stringify(tree_actions));
    get_tree_image(current_tree_id, current_tree_newick,'', node_data);
}
//-------------------------------------------
function load_tip_images(){
  var service_url = "https://phylo.cs.nmsu.edu/phylotastic_ws/ds/";
  var service_func1 = "images_download_time";
  //var service_url = "http://phylo.cs.nmsu.edu:5008/phylotastic_ws/ds/images_download_time";
  var service_param = "newick="+ encodeURIComponent(current_tree_newick);
  //var service_param = {"newick": current_tree_newick};  
  //console.log("load tip images called");
  xhr = new XMLHttpRequest();
  xhr.open("POST", service_url+service_func1, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
        var hres = JSON.parse(xhr.responseText);
        if (hres.number_species != 0){
           $('#tree_image_message').html("Wait "+hres.download_time+" seconds for image retrieval, then re-click.");
           //console.log("download started");
           var pm = {"newick":current_tree_newick}
           $('#tree_image_message').load(service_url+"/download_all_images", pm);
        }
        else{
           //console.log("click load button again");
           xhr2 = new XMLHttpRequest();
           var url2 = ete_webplugin_URL+'/set_all_images';
           xhr2.open("POST", url2, true);
           xhr2.setRequestHeader("Content-type", "application/json");
           xhr2.onreadystatechange = function () {
              if (xhr2.readyState == 4 && xhr2.status == 200) {
                 var hres2 = JSON.parse(xhr2.responseText);
                 var ndac = hres2.actions["node_actions"];
                 //console.log("na load:"+JSON.stringify(ndac));
                 if (typeof(ndac) != "undefined"){
                    node_actions_list = ndac;
                    tree_state_changed = true;
                    //console.log("na in load:"+JSON.stringify(node_actions_list));
                 }
                 get_tree_image(current_tree_id, current_tree_newick,'');
              }
           }
           //parameters for second POST request 
           var params2 = JSON.stringify({"tree_newick": current_tree_newick,"tree_id":current_tree_id, "node_actions": node_actions_list});
           xhr2.send(params2);
        }//end of else
     }
  }//end of xhr
  //parameters for POST request 
  xhr.send(service_param);
}

//-------------------------------------------
/*function bind_popup(){
  $(".ete_tree_img").bind('click',function(e){
      $("#popup").css('left', e.pageX - 2);
      $("#popup").css('top', e.pageY - 2);
      $("#popup").css('position',"absolute" );
      $("#popup").css('background-color',"#fff" );
      $("#popup").draggable({ cancel: 'span,li' });
      $("#popup").show();
   });
   
}
*/
function bind_popup(leftOffset, topOffset){
  topOffset = (typeof topOffset !== 'undefined') ? topOffset : 0;
  leftOffset = (typeof leftOffset !== 'undefined') ? leftOffset : 0;
  console.log("bind popup called");
  console.log("topoffset:"+topOffset+" leftoffset:"+leftOffset);

  $(".ete_tree_img area").bind('click',function(e){
      $("#popup").css('left', e.pageX - leftOffset);
      $("#popup").css('top', e.pageY - topOffset);
      $("#popup").css('position',"absolute" );
      $("#popup").css('background-color',"#fff" );
      $("#popup").draggable({ cancel: 'span,li' });
      //$("#popup").show_popup();
      show_popup();
      e.preventDefault();
      return false;
   });
   $(".ete_tree_img").bind('click', function(e) {
     $("#popup").css("display", "none");
   })

   $(".ete_tree_img + div").bind('click', function(e) {
     $('#popup').css('display', 'none');
   })

}

/*
function hide_popup(){
  $('#popup').hide();
}
*/

function show_popup(){
  $('#popup').css("display","initial");
}

function hide_popup(){
  $('#popup').css("display","none");
}


//-------------OTHERS----------------------

function highlight_node(treeid, nodeid, faceid, x, y, width, height){
  return;
  console.log(treeid, nodeid, x, y, width, height);
  var img = $('#img_'+treeid);
  var offset = img.offset();
  console.log(img);
  console.log(offset);

  $("#highlighter").show();
  $("#highlighter").css("top", offset.top+y-1);
  $("#highlighter").css("left", offset.left+x-1);
  $("#highlighter").css("width", width+1);
  $("#highlighter").css("height", height+1);

}
function unhighlight_node(){
  return;
  console.log("unhighlight");
  $("#highlighter").hide();
}

function makeid()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}


///////OLD STUFF
//http://www.jquery-az.com/css-display-and-visibility-6-examples-to-showhide-html-elements/

$(document).ready(function(){
  hide_popup();
});
