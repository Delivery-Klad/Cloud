function delete_file(){
    var data = {};
    data.file_path  = document.getElementById("file_path").value + "/" + document.getElementById("file_name").value;
    var json = JSON.stringify(data);
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", "/file/", true);
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.onload = function () {
        var data = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById(document.getElementById("file_name").value).remove();
        } else { console.log(data); }
    }
    xhr.send(json);
}

function rename_file(){
    var data = {};
    data.file_path  = document.getElementById("file_path").value;
    data.file_name = document.getElementById("file_name").value;
    data.new_name = document.getElementById("new_name").value;
    var json = JSON.stringify(data);
    console.log(data);
    var xhr = new XMLHttpRequest();
    xhr.open("PATCH", "/file/", true);
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.onload = function () {
        var data = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == 200) {
            var li_block = document.getElementById(document.getElementById("file_name").value);
            var new_name = document.getElementById("new_name").value;
            li_block.textContent = "";
            li_block.setAttribute("id", new_name);
            var li_href = document.createElement("a");
            li_href.innerText = new_name;
            li_href.setAttribute("href", document.getElementById("file_path").value + "/" + new_name);
            li_href.setAttribute("title", document.getElementById("file_path").value + "/" + new_name);
            li_href.setAttribute("class", "file");
            li_block.appendChild(li_href);
        } else { console.log(data); }
    }
    xhr.send(json);
}

function replace_path(){
    document.location.href = "/source/tree?path=" + document.getElementById("file_path").value + "/" + document.getElementById("file_name").value;
}

function delete_folder(){
    var data = {};
    var local_path = document.getElementById("file_path").value;
    data.file_path  = local_path + "/" + document.getElementById("file_name").value;
    var json = JSON.stringify(data);
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", "/folder/", true);
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.onload = function () {
        var data = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById(document.getElementById("file_name").value).remove();
        } else { console.log(data); }
    }
    xhr.send(json);
}

function rename_folder(){
    var data = {};
    data.path  = document.getElementById("file_path").value + "/" + document.getElementById("file_name").value;
    data.arg = document.getElementById("new_name").value;
    data.access = document.querySelector('input[name="access"]:checked').value;
    var json = JSON.stringify(data);
    console.log(data);
    var xhr = new XMLHttpRequest();
    xhr.open("PATCH", "/folder/", true);
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.onload = function () {
        var data = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == 200) {
            var li_block = document.getElementById(document.getElementById("file_name").value);
            var new_name = document.getElementById("new_name").value;
            li_block.textContent = "";
            li_block.setAttribute("id", new_name);
            var li_href = document.createElement("a");
            li_href.innerText = new_name;
            li_href.setAttribute("href", document.getElementById("file_path").value + "/" + new_name);
            li_href.setAttribute("title", document.getElementById("file_path").value + "/" + new_name);
            li_href.setAttribute("class", "folder");
            li_block.appendChild(li_href);
        } else { console.log(data); }
    }
    xhr.send(json);
}

function create_new_folder(){
    var data = {};
    var folder_name = document.getElementById("folder_name").value;
    var folder_path = document.getElementById("folder_path").value;
    data.path  = folder_path;
    data.arg = folder_name;
    data.access = document.querySelector('input[name="folder_access"]:checked').value;
    var json = JSON.stringify(data);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/folder/", true);
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.onload = function () {
        var data = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == 200) {
            let new_folder = document.createElement("li");
            new_folder.setAttribute("id", folder_name);
            ul_block.appendChild(new_folder);
            let folder_href = document.createElement("a");
            folder_href.textContent = folder_name;
            folder_href.href = folder_path + "/" + folder_name;
            new_folder.appendChild(folder_href);
            folder_href.setAttribute("title", folder_name);
            folder_href.className = "folder";
        }
    }
    xhr.send(json);
}

function create_message(text){
    var block = document.createElement("div");
    block.setAttribute("class", "error");
    block.textContent = text;
    alert_box.appendChild(block);
    setTimeout(remove_message, 5000, block);
}

function remove_message(block){ block.remove(); }

var place_holder = document.getElementById("meta_place_holder")
var menu_element = document.getElementById("menu_m");
var scnd_menu = document.getElementById("scnd_menu");
var ul_block = document.getElementById("files");

$(document).ready(function() {
    if ($("#file").addEventListener) {
        $("#file").addEventListener('contextmenu', function(e) {
            alert("You've tried to open context menu");
            e.preventDefault();
        }, false);
    } else {
        $('body').on('contextmenu', 'a.file', function() {
            var xhr = new XMLHttpRequest();
            var text = $(this).contents()[0].nodeValue.trim();
            xhr.open('GET', '/file/meta?path=' + document.getElementById("file_path").value + '&name=/' + text);
            xhr.onreadystatechange = function(){
                if(xhr.readyState === 4 && xhr.status === 200){
                    var arr = JSON.parse(xhr.responseText).res;
                    place_holder.textContent = "";
                    arr.forEach((element) => {
                        let block = document.createElement('div');
                        block.textContent += element;
                        place_holder.append(block);
                    })
                }
            }
            xhr.send()
            scnd_menu.className = "hide";
            menu_element.className = "show";
            document.getElementById('file_name').value = text;
            menu_element.style.top = mouseY(event) + 'px';
            menu_element.style.left = mouseX(event) + 'px';
            try{
                document.getElementById("access_holder").textContent = "";
                var rename_btn = document.getElementById("rename_btn");
                rename_btn.setAttribute("onclick", "rename_file();");
                var delete_btn = document.getElementById("delete_btn");
                delete_btn.setAttribute("onclick", "delete_file();");
            } catch {}
            setFocusToTextBox();
            window.event.returnValue = false;
        });
        $('body').on('contextmenu', 'a.image', function() {
            var xhr = new XMLHttpRequest();
            var text = $(this).contents()[0].nodeValue.trim();
            xhr.open('GET', '/file/meta?path=' + document.getElementById("file_path").value + '&name=/' + text);
            xhr.onreadystatechange = function(){
                if(xhr.readyState === 4 && xhr.status === 200){
                    var arr = JSON.parse(xhr.responseText).res;
                    place_holder.textContent = "";
                    arr.forEach((element) => {
                        let block = document.createElement('div');
                        block.textContent += element;
                        place_holder.append(block);
                    })
                }
            }
            xhr.send()
            scnd_menu.className = "hide";
            menu_element.className = "show";
            document.getElementById('file_name').value = text;
            menu_element.style.top = mouseY(event) + 'px';
            menu_element.style.left = mouseX(event) + 'px';
            try{
                document.getElementById("access_holder").textContent = "";
                var rename_btn = document.getElementById("rename_btn");
                rename_btn.setAttribute("onclick", "rename_file();");
                var delete_btn = document.getElementById("delete_btn");
                delete_btn.setAttribute("onclick", "delete_file();");
            } catch {}
            setFocusToTextBox();
            window.event.returnValue = false;
        });
        $('body').on('contextmenu', 'a.folder', function() {
            document.getElementById("access_holder").textContent = "";
            var text = $(this).contents()[0].nodeValue.trim();
            place_holder.textContent = "";
            scnd_menu.className = "hide";
            menu_element.className = "show";
            document.getElementById('file_name').value = text;
            menu_element.style.top = mouseY(event) + 'px';
            menu_element.style.left = mouseX(event) + 'px';
            var rename_btn = document.getElementById("rename_btn");
            rename_btn.setAttribute("onclick", "rename_folder();");
            var delete_btn = document.getElementById("delete_btn");
            delete_btn.setAttribute("onclick", "delete_folder();");
            var access1_container = document.createElement("div");
            var access1 = document.createElement("input");
            access1.setAttribute("id", "radio-1");
            access1.setAttribute("type", "radio");
            access1.setAttribute("name", "access");
            access1.setAttribute("value", "root");
            access1_container.appendChild(access1);
            var label1 = document.createElement("label");
            label1.setAttribute("for", "radio-1");
            label1.textContent = "Root";
            access1_container.appendChild(label1);
            var access2_container = document.createElement("div");
            var access2 = document.createElement("input");
            access2.setAttribute("id", "radio-2");
            access2.setAttribute("type", "radio");
            access2.setAttribute("name", "access");
            access2.setAttribute("value", "auth");
            access2_container.appendChild(access2);
            var label2 = document.createElement("label");
            label2.setAttribute("for", "radio-2");
            label2.textContent = "Authorized";
            access2_container.appendChild(label2);
            var access3_container = document.createElement("div");
            var access3 = document.createElement("input");
            access3.setAttribute("id", "radio-3");
            access3.setAttribute("type", "radio");
            access3.setAttribute("name", "access");
            access3.setAttribute("value", "all");
            access3_container.appendChild(access3);
            var label3 = document.createElement("label");
            label3.setAttribute("for", "radio-3");
            label3.textContent = "All users";
            access3_container.appendChild(label3);
            var access4_container = document.createElement("div");
            var access4 = document.createElement("input");
            access4.setAttribute("id", "radio-4");
            access4.setAttribute("type", "radio");
            access4.setAttribute("name", "access");
            access4.setAttribute("value", "privilege");
            access4_container.appendChild(access4);
            var label4 = document.createElement("label");
            label4.setAttribute("for", "radio-4");
            label4.textContent = "Privileged";
            access4_container.appendChild(label4);
            var menu_form = document.getElementById("access_holder");
            menu_form.appendChild(access1_container);
            menu_form.appendChild(access2_container);
            menu_form.appendChild(access3_container);
            menu_form.appendChild(access4_container);
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/folder' + document.getElementById("file_path").value + '/' + text);
            xhr.onreadystatechange = function(){
                if(xhr.readyState === 4 && xhr.status === 200){
                    var res = JSON.parse(xhr.responseText).res;
                    if (res == 1){ access1.checked = true; }
                    else if (res == 2){ access2.checked = true; }
                    else if (res == 3){ access3.checked = true; }
                    else if (res == 4){ access4.checked = true; }
                }
            }
            xhr.send()
            window.event.returnValue = false;
        });
        $('body').on('contextmenu', function(e) {
            if ($(e.target).is("body")){
                scnd_menu.className = "show";
                menu_element.className = "hide";
                scnd_menu.style.top = mouseY(event) + 'px';
                scnd_menu.style.left = mouseX(event) + 'px';
                window.event.returnValue = false;
            }
        });
    }
});

$(document).bind("click", function(event) {
    if (event.target.name === "new_name"){ return; }
    else if (event.target.name === "access"){ return; }
    else if (event.target.name === "folder_access"){ return; }
    else if (event.target.name === "folder_name"){ return; }
    else if (event.target.name === "data"){ return; }
    place_holder.textContent = "";
    scnd_menu.className = "hide";
    menu_element.className = "hide";
});

function mouseX(evt) {
    if (evt.pageX) { return evt.pageX; }
    else if (evt.clientX) {
        return evt.clientX + (document.documentElement.scrollLeft ?
        document.documentElement.scrollLeft : document.body.scrollLeft); }
    else { return null; }
}

function mouseY(evt) {
    if (evt.pageY) { return evt.pageY; }
    else if (evt.clientY) {
        return evt.clientY + (document.documentElement.scrollTop ?
        document.documentElement.scrollTop : document.body.scrollTop); }
    else { return null; }
}

function setFocusToTextBox(){ document.getElementById("new_name").focus(); }

$("form#data").submit(function(event){
    event.preventDefault();
    var formData = new FormData($(this)[0]);
    var file_name = document.getElementsByName("data")[0].value.split("\\").pop();
    $.ajax({
        url: '/file/?path=' + document.getElementById("upload_path").value,
        type: 'POST',
        data: formData,
        async: true,
        cache: false,
        contentType: false,
        processData: false,
        success: function () {
            let new_file = document.createElement("li");
            new_file.setAttribute("id", file_name);
            ul_block.appendChild(new_file);
            let file_href = document.createElement("a");
            file_href.textContent = file_name;
            file_href.href = "/" + document.getElementById("upload_path").value + file_name;
            new_file.appendChild(file_href);
            file_href.setAttribute("title", file_href.href);
            file_href.className = "file";
        }
    });
});