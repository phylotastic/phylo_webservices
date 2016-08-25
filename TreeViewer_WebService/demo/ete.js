/*  it requires jquery loaded */
var ete_webplugin_URL = "http://phylo.cs.nmsu.edu:8989";
var loading_img = '<img border=0 src="loader.gif">';
var current_tree_id = "";

function update_server_status(){
  console.log('updating');
  $('#server_status').load(ete_webplugin_URL+"/status");

}

function save_tree_image(){
  $('#svg_image').html(loading_img);
  format = $('input[name="format"]:checked').val();
  var params = {'treeid': current_tree_id, 'format': format }; 
  $('#svg_image').load(ete_webplugin_URL+'/save_tree_image',params);
}

/*
function get_tree_image(newick, recipient){
  var treeid = makeid();
  current_tree_id = treeid;
  $(recipient).html('<div id="' + treeid + '">' + loading_img + '</div>');
  //$(recipient).fadeTo(500, 0.2);
  var params = {'newick':newick, 'treeid':treeid};
  $('#'+treeid).load(ete_webplugin_URL+'/get_tree_image', params,
    function() {
            $('#'+treeid).fadeTo(100, 0.9);
  });
}
*/

function get_tree_image(newick,recipient){
  var treeid = makeid();
  current_tree_id = treeid;
  $(recipient).html('<div id="' + treeid + '">' + loading_img + '</div>');
  xhr = new XMLHttpRequest();
  var url = ete_webplugin_URL+'/get_tree_image';
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () { 
    if (xhr.readyState == 4 && xhr.status == 200) {
        $('#'+treeid).html(xhr.responseText)
        $('#'+treeid).fadeTo(100, 0.9);
    }
  }
  var data = JSON.stringify({"newick": newick,"treeid":treeid, "extra_data":{
	"tip_data_headers": ["habitat","mass"],
	"tip_list": 
        [
           {
		"tip_name": "Rangifer tarandus",
		"tip_data_values": ["herbivore", 109.09],
                "tip_data_colors": ["steelblue", "steelblue"]
	   }, 
           {
		"tip_name": "Cervus elaphus",
		"tip_data_values": ["herbivore", 240.87],
                "tip_data_colors": ["steelblue", "steelblue"]
	   },
           {
		"tip_name": "Bos taurus",
		"tip_data_values": ["herbivore", 618.64],
                "tip_data_colors": ["steelblue", "steelblue"]
	   },
	   {
		"tip_name": "Ovis orientalis",
		"tip_data_values": ["herbivore", 39.1],
                "tip_data_colors": ["steelblue", "steelblue"]
	   },
	   {
		"tip_name": "Suricata suricatta",
		"tip_data_values": ["carnivore", 0.73],
                "tip_data_colors": ["yellowgreen", "yellowgreen"]
	   },
	   {
		"tip_name": "Mephitis mephitis",
		"tip_data_values": ["omnivore", 2.4],
                "tip_data_colors": ["tan", "tan"]
	   }
         ],
    "node_label_list": [
       {
        "node_name": "Cervidae",
	    "node_label": "7 steps"
       }
       ]
       } 
     });
  xhr.send(data);
}

//-----------------------------------------
function show_actions(treeid, nodeid, faceid){
  $("#popup").html(loading_img);
  var params = {"treeid": treeid, "nodeid": nodeid, "faceid": faceid};
  $('#popup').load(ete_webplugin_URL+'/get_actions', params);
}

function run_action(treeid, nodeid, faceid, aindex){
  $("#popup").hide();
  $('#'+treeid).html(loading_img);
  console.log(treeid, nodeid, faceid, aindex, $('#'+treeid));
  var params = {"treeid": treeid, "nodeid": nodeid, "faceid": faceid, "aindex":aindex};
  $('#'+treeid).load(ete_webplugin_URL+'/run_action', params,
    function() {
      console.log('run action');
            $('#'+treeid).fadeTo(100, 0.9);
  });
}


function bind_popup(){
  $(".ete_tree_img").bind('click',function(e){
                          $("#popup").css('left',e.pageX-2 );
                          $("#popup").css('top',e.pageY-2 );
                          $("#popup").css('position',"absolute" );
                          $("#popup").css('background-color',"#fff" );
                          $("#popup").draggable({ cancel: 'span,li' });
                          $("#popup").show();
                            });
}
function hide_popup(){
  $('#popup').hide();
}

//------------------------------------
function run_tree_action() {
    colorcode = document.getElementsByName("color")[0].value;
    //colorcode="DarkRed";
    linewidth = $('input[name="lwidth"]:checked').val();
    if(document.getElementById('ladderize').checked){
        ladderize = true;
    }
    else{
        ladderize = false;
    }
    $('#'+current_tree_id).html(loading_img);
    var params = {"treeid": current_tree_id, "colorcode": colorcode, "linewidth":linewidth, "ladderize": ladderize};
   
  $('#'+current_tree_id).load(ete_webplugin_URL+'/run_tree_action', params,
    function() {
      console.log('run tree action');
            $('#'+current_tree_id).fadeTo(100, 0.9);
  });
    
}
/*
function run_tree_ladderize(){
   if(document.getElementById('ladderize').checked) {
     $('#'+current_tree_id).html(loading_img);
     var params = {"treeid": current_tree_id};
     $('#'+current_tree_id).load(ete_webplugin_URL+'/run_tree_ladderize', params,
       function() {
            console.log('run tree action');
            $('#'+current_tree_id).fadeTo(100, 0.9);
       });

   } 
   else {
    //$("#txtAge").hide()
   }
}
*/
//-----------------------------------

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






$(document).ready(function(){
  hide_popup();
});
