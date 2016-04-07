var editor = ace.edit("editor");
var prev_file="";
var undo_manager_dict={};
editor.setTheme("ace/theme/solarized_light");
editor.getSession().setMode("ace/mode/c_cpp");

function add_input(){
    $.get(add_input_url+"?prob_code="+get_par("prob_code"),function(data){
        update_file_list();
    });
}

function submit(){

    $("#submit_status").html("Submitting ...");
    $.get(submit_url+"?prob_code="+get_par("prob_code"),function(data){
        $("#submit_status").html(data);
    });
}

function run(){
    $("#run_status").html("Running ...");
    var test_case_num = parseInt($("#test_case_num").val(), 0).toString();
    $.get(run_url+"?prob_code="+get_par("prob_code")+"&test_case_num="+test_case_num,function(data){
        $("#run_status").html(data);
    });
}

function change_mode(val){
    editor.getSession().setMode("ace/mode/"+val);
}
// http://stackoverflow.com/a/901144/2258503
function get_par(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)", "i"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function set_text(val){
    // jsonp http://stackoverflow.com/a/21948020/2258503
    $.ajax({url: "http://localhost:8008"+val, type: "GET",contentType: "application/json", dataType: "jsonp", success: function(result){
        // editor.setSession(ace.createEditSession();
        // http://stackoverflow.com/questions/18614169/set-value-for-ace-editor-without-selecting-the-whole-editor
        editor.setValue(result,1);
        editor.getSession().setUndoManager(undo_manager_dict[val]);
    }});
}

function save_text(file,text,async_req){
        // You cannot use jsonp with POST
    $.ajax({url: "http://localhost:8008"+file, type: "POST", data: text, async: async_req, success: function(result){
        alert(result);
    }});
}

function save_text_helper(){
    file=$("#file_paths").val();
    save_text(file,editor.getValue(),true);
}

// https://developer.mozilla.org/en-US/docs/Web/API/WindowTimers/setInterval
setInterval(save_text_helper,5000);

function change_text(val){
    if(prev_file != ""){
        save_text(prev_file,editor.getValue(),false)
    }
    set_text(val);
    prev_file=val;
}

// http://www.w3schools.com/jquery/ajax_ajax.asp
$(document).ready(update_file_list);


function update_file_list(){
    // jsonp http://stackoverflow.com/a/21948020/2258503
    $.ajax({url: "http://localhost:8008/"+get_par('prob_code'), type: "GET",contentType: "application/json", dataType: "jsonp", success: function(result){
        $("#file_paths").empty();
        $.each( result, function( i, val ) {
            $("#file_paths").append('<option value='+val+'>'+val+'</option>');
            if(!(val in undo_manager_dict))
                undo_manager_dict[val]=new ace.UndoManager();
        });
        set_text($("#file_paths").val());
        prev_file=$("#file_paths").val();
    }});
}
