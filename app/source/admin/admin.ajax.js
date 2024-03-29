var place_holder = document.getElementById("place_holder1");
var sidebar1 = document.getElementById("sidebar");
var alert_box = document.getElementById("alert-box");

function create_arrow(up, user){
    var a_block = document.createElement("a");
    a_block.setAttribute("href", "javascript:set_permissions(" + up + "," + user + ");");
    var arrow = document.createElement("img");
    if (up === true){ arrow.setAttribute("src", "source/images/up.svg"); }
    else{ arrow.setAttribute("src", "source/images/down.svg"); }
    a_block.appendChild(arrow);
    return a_block;
}

function toggle_menu(num){
    localStorage.setItem("current_page", num);
    document.getElementById("sidebar1").className = "sidebar-item";
    document.getElementById("sidebar2").className = "sidebar-item";
    document.getElementById("sidebar3").className = "sidebar-item";
    document.getElementById("sidebar4").className = "sidebar-item";
    document.getElementById("sidebar5").className = "sidebar-item";
    document.getElementById("sidebar6").className = "sidebar-item";
    document.getElementById("sidebar7").className = "sidebar-item";
    document.getElementById("sidebar" + num).className = "sidebar-item active";
}

function show_loader(parent){
    parent.textContent = "";
    var loading = document.createElement("div");
    loading.className = "loader";
    parent.appendChild(loading);
}

function fill_placeholder(response, func){
    var arr = JSON.parse(response).res;
    place_holder.textContent = "";
    let div_block = document.createElement('div');
    let href = document.createElement('a');
    href.href = func;
    href.textContent = "Clear logs";
    href.className = "clear";
    place_holder.append(div_block);
    div_block.appendChild(href);
    arr.forEach((element) => {
        let block = document.createElement('div');
        block.textContent += element;
        place_holder.append(block);
    })
}

function set_table_header(table){
    var headers = table.insertRow();
    var id_header = document.createElement("th");
    id_header.textContent = " Id ";
    headers.appendChild(id_header);
    var name_header = document.createElement("th");
    name_header.textContent = " Username ";
    headers.appendChild(name_header);
    var password_header = document.createElement("th");
    password_header.textContent = " Password ";
    headers.appendChild(password_header);
    var agent_header = document.createElement("th");
    agent_header.textContent = " User-Agent ";
    headers.appendChild(agent_header);
    var permissions_header = document.createElement("th");
    permissions_header.textContent = " Permissions ";
    headers.appendChild(permissions_header);
    var actions_header = document.createElement("th");
    actions_header.textContent = " Actions ";
    headers.appendChild(actions_header);
}

function open_dashboard(){
    toggle_menu(1);
    show_loader(place_holder)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/dashboard/');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            var arr = JSON.parse(xhr.responseText).res;
            place_holder.textContent = "";
            arr.forEach((element) => {
                let block = document.createElement('div');
                if (element === "Summary"){
                    block.style.fontWeight = "bold";
                    block.style.fontSize = "20px";
                }
                block.textContent += element;
                place_holder.append(block);
            })
        }
        if (xhr.readyState === 4 && xhr.status === 403){ create_message(JSON.parse(xhr.responseText).res, "error"); }
    }
    xhr.send();
}

function untracked(){
    toggle_menu(2);
    show_loader(place_holder)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/dashboard/?arg=true');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            var arr = JSON.parse(xhr.responseText).res;
            place_holder.textContent = "";
            arr.forEach((element) => {
                let block = document.createElement('div');
                if (element === "Untracked files"){
                    block.style.fontWeight = "bold";
                    block.style.fontSize = "20px";
                }
                block.textContent += element;
                place_holder.append(block);
            })
        }
        else if (xhr.readyState === 4 && xhr.status === 403){ create_message(JSON.parse(xhr.responseText).res, "error"); }
    }
    xhr.send();
}

function logs(){
    toggle_menu(3);
    show_loader(place_holder)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/logs');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){ fill_placeholder(xhr.responseText, "javascript:clear_logs();") }
        else if (xhr.readyState === 4 && xhr.status === 403){ create_message(xhr.responseText, "error"); }
    }
    xhr.send();
}

function clear_logs(){
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/admin/clear_logs');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            fill_placeholder(xhr.responseText, "javascript:clear_logs();");
            create_message("Лог очищен!", "info");
        }
        else if (xhr.readyState === 4 && xhr.status === 403){ create_message(xhr.responseText, "error"); }
    }
    xhr.send();
}

function errors(){
    toggle_menu(4);
    show_loader(place_holder)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/errors');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
			fill_placeholder(xhr.responseText, "javascript:clear_errors();")
        }
        else if (xhr.readyState === 4 && xhr.status === 403){ create_message(xhr.responseText, "error"); }
    }
    xhr.send();
}

function clear_errors(){
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/admin/clear_errors');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            fill_placeholder(xhr.responseText, "javascript:clear_errors();")
            create_message("Лог ошибок очищен!", "info");
        }
        else if (xhr.readyState === 4 && xhr.status === 403){ create_message(xhr.responseText, "error"); }
    }
    xhr.send();
}

function users(){
    toggle_menu(5);
    show_loader(place_holder)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/users');
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
            var arr = JSON.parse(xhr.responseText).res;
            place_holder.textContent = "";
            var table = document.createElement("TABLE");
            table.setAttribute("style", "width:100%");
            set_table_header(table);
            arr.forEach((element) => {
                if (element === "Users"){
                    let block = document.createElement('div');
                    block.setAttribute("style", "font-weight: bold; font-size: 20px;");
                    block.textContent += element;
                    place_holder.append(block);
                }
                else {
                    var current_row = table.insertRow();
                    var counter = 0;
                    var user_id = element[0];
                    element.forEach((row) => {
                        counter = counter + 1;
                        var table_block = document.createElement("td");
                        table_block.textContent = row;
                        current_row.appendChild(table_block);
                        if (counter === 5){
                            table_block.appendChild(create_arrow(true, user_id));
                            table_block.appendChild(create_arrow(false, user_id));
                        }
                    })
                    var table_block = document.createElement("td");
                    current_row.appendChild(table_block);
                    var a_block = document.createElement("a");
                    a_block.setAttribute("href", "javascript:delete_user(" + user_id + ");");
                    a_block.textContent = "Delete";
                    table_block.appendChild(a_block);
                }
            });
            place_holder.append(table);
        }
        else if (xhr.readyState === 4 && xhr.status === 403){ create_message(JSON.parse(xhr.responseText).res, "error"); }
    }
    xhr.send();
}

function push_files(){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/admin/');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){ create_message(xhr.responseText, "info"); }
        else if (xhr.readyState === 4 && xhr.status === 403){ create_message(xhr.responseText, "error"); }
    }
    xhr.send();
}

function swagger(){
    toggle_menu(6);
    show_loader(place_holder)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/swagger/');
    var docs_page = document.createElement("iframe");
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            place_holder.removeChild(document.getElementsByClassName('loader')[0]);
            docs_page.setAttribute("src", JSON.parse(xhr.responseText).res);
        }
    }
    xhr.send();
    docs_page.setAttribute("width", "100%");
    docs_page.setAttribute("height", "100%");
    docs_page.setAttribute("scrolling", "auto%");
    place_holder.append(docs_page);
}

function heroku(){
    toggle_menu(7);
    show_loader(place_holder)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/heroku/', true);
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            place_holder.textContent = "";
            JSON.parse(xhr.responseText).res.forEach((element) => {
                var div_block = document.createElement("p");
                var h_block = document.createElement("h");
                h_block.textContent = element.email;
                h_block.className = "email";
                div_block.appendChild(h_block);
                element.apps.forEach((app) => {
                    var li_block = document.createElement("ul")
                    li_block.setAttribute("style", "text-size: 16px;");
                    li_block.textContent = app.name + " (" + app.type + ")"
                    if (app.type != "database") {
                        var label = document.createElement("label");
                        label.className = "switch";
                        var checkbox = document.createElement("input");
                        checkbox.setAttribute("type", "checkbox");
                        checkbox.setAttribute("onclick", "enable_project(this, " + app.args + ")");
                        if (app.enable === "ON") {
                            checkbox.setAttribute("checked", "");
                        }
                        var span = document.createElement("span");
                        span.className = "slider round";
                        label.appendChild(checkbox);
                        label.appendChild(span);
                        var logs_but = document.createElement("a");
                        logs_but.setAttribute("title", "Application logs");
                        logs_but.setAttribute("onclick", "heroku_logs('" + app.name + "', " + app.args + ");");
                        var log_img = document.createElement("img");
                        log_img.setAttribute("src", "source/images/log.svg");
                        log_img.setAttribute("width", "20");
                        log_img.setAttribute("height", "20");
                        logs_but.appendChild(log_img);
                        var vars_but = document.createElement("a");
                        vars_but.setAttribute("title", "Application variables");
                        vars_but.setAttribute("href", "#openModal");
                        vars_but.setAttribute("onclick", "heroku_vars('" + app.name + "', " + app.args + ");");
                        var vars_img = document.createElement("img");
                        vars_img.setAttribute("src", "source/images/vars.svg");
                        vars_img.setAttribute("width", "20");
                        vars_img.setAttribute("height", "20");
                        vars_but.appendChild(vars_img);
                        li_block.appendChild(label);
                        li_block.appendChild(logs_but);
                        li_block.appendChild(vars_but);
                    }
                    var addon_but = document.createElement("a");
                    addon_but.setAttribute("title", "Application addons");
                    addon_but.setAttribute("onclick", "heroku_addon('" + app.name + "', " + app.args + ");");
                    var addon_img = document.createElement("img");
                    addon_img.setAttribute("src", "source/images/addon.svg");
                    addon_img.setAttribute("width", "20");
                    addon_img.setAttribute("height", "20");
                    addon_but.appendChild(addon_img);
                    li_block.appendChild(addon_but);
                    if (app.type != "database") {
                        var console_div = document.createElement("div");
                        console_div.setAttribute("id", app.name + "_console");
                        li_block.appendChild(console_div);
                    }
                    var addon_div = document.createElement("div");
                    addon_div.setAttribute("id", app.name + "_addon");
                    li_block.appendChild(addon_div);
                    div_block.appendChild(li_block);
                });
                place_holder.appendChild(div_block);
            });
        }
    }
    xhr.send();
}

function heroku_logs(block, key, app){
    var parent = document.getElementById(block + "_console");
    if (parent.textContent == ""){
        show_loader(parent)
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/heroku/logs?key=' + key + "&app=" + app, true);
        xhr.onreadystatechange = function(){
            if (xhr.readyState === 4 && xhr.status === 200){
                parent.className = "console";
                parent.textContent = "";
                JSON.parse(xhr.responseText).res.forEach((element) => {
                    var console_line = document.createElement("div");
                    var title_div = document.createElement("div");
                    title_div.className = "console_title";
                    title_div.textContent = element.title;
                    var body_div = document.createElement("div");
                    body_div.className = "console_body";
                    body_div.textContent = element.body;
                    console_line.appendChild(title_div);
                    console_line.appendChild(body_div);
                    parent.appendChild(console_line);
                });
            }
            else if (xhr.readyState === 4 && xhr.status != 200){
                parent.className = ""; parent.textContent = "";
            }
        }
        xhr.send();
    }
    else { parent.className = ""; parent.textContent = ""; }
}

function heroku_vars(block, key, app){
    document.getElementById("modal-title").textContent = "Variables";
    var parent = document.getElementById("modal-body");
    show_loader(parent)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/heroku/vars?key=' + key + "&app=" + app, true);
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            parent.textContent = "";
            JSON.parse(xhr.responseText).res.forEach((element) => {
                var console_line = document.createElement("div");
                console_line.setAttribute("id", element.title + "full_line");
                var title = document.createElement("label");
                title.setAttribute("style", "width: 100%;");
                title.textContent = element.title;
                var body = document.createElement("input");
                body.setAttribute("style", "width: 90%;");
                body.setAttribute("id",  element.title);
                body.value = element.body;
                var confirm = document.createElement("a");
                var confirm_img = document.createElement("img");
                confirm_img.setAttribute("src", "source/images/confirm.svg");
                confirm_img.setAttribute("width", "20");
                confirm_img.setAttribute("height", "20");
                confirm.appendChild(confirm_img);
                confirm.setAttribute("onclick", "update_var('" + element.title + "'," + app + "," + key +");");
                var remove = document.createElement("a");
                var remove_img = document.createElement("img");
                remove_img.setAttribute("src", "source/images/trash.svg");
                remove_img.setAttribute("width", "20");
                remove_img.setAttribute("height", "20");
                remove.appendChild(remove_img);
                remove.setAttribute("onclick", "delete_var('" + element.title + "'," + app + "," + key +");");
                console_line.appendChild(title);
                console_line.appendChild(body);
                console_line.appendChild(confirm);
                console_line.appendChild(remove);
                parent.appendChild(console_line);
            });
            var console_line = document.createElement("div");
            console_line.setAttribute("style", "text-align: center; font-size: 25px;");
            var body = document.createElement("a");
            body.setAttribute("id", "add_new_var");
            body.textContent = "+";
            body.setAttribute("onclick", "add_var(" + app + "," + key +");")
            console_line.appendChild(body);
            parent.appendChild(console_line);
        }
        else if (xhr.readyState === 4 && xhr.status != 200){
            var console_line = document.createElement("div");
            console_line.setAttribute("style", "text-align: center; font-size: 25px;");
            var body = document.createElement("a");
            body.setAttribute("id", "add_new_var");
            body.textContent = "+";
            body.setAttribute("onclick", "add_var(" + app + "," + key +");")
            console_line.appendChild(body);
            parent.appendChild(console_line);
        }
    }
    xhr.send();
}

function add_var(app, key){
    $("#add_new_var").remove()
    var parent = document.getElementById("modal-body");
    var div_block = document.createElement("div");
    div_block.setAttribute("id", "new_var_block");
    var var_name = document.createElement("input");
    var_name.setAttribute("id", "new_var");
    var var_value = document.createElement("input");
    var_value.setAttribute("id", "new_var_value");
    var confirm = document.createElement("a");
    var confirm_img = document.createElement("img");
    confirm_img.setAttribute("src", "source/images/confirm.svg");
    confirm_img.setAttribute("width", "20");
    confirm_img.setAttribute("height", "20");
    confirm.appendChild(confirm_img);
    confirm.setAttribute("onclick", "update_var('new_var'," + app + "," + key +");");
    div_block.appendChild(var_name);
    div_block.appendChild(var_value);
    div_block.appendChild(confirm);
    parent.appendChild(div_block);
    var console_line = document.createElement("div");
    console_line.setAttribute("style", "text-align: center; font-size: 25px;");
    var body = document.createElement("a");
    body.setAttribute("id", "add_new_var");
    body.textContent = "+";
    body.setAttribute("onclick", "add_var(" + app + "," + key +");")
    console_line.appendChild(body);
    parent.appendChild(console_line);
}

function update_var(title, app, key){
    var data = {};
    data.app = app;
    data.key = key;
    if (title != "new_var") {
        var input_block = document.getElementById(title);
        data.var_name = title;
        data.var_value = input_block.value;
    }
    else{
        var name_block = document.getElementById("new_var");
        var value_block = document.getElementById("new_var_value");
        data.var_name = name_block.value;
        data.var_value = value_block.value;
    }
    var xhr = new XMLHttpRequest();
    xhr.open('PATCH', "/heroku/var/");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            create_message(JSON.parse(xhr.responseText).res, "info");
            if (title != "new_var") {
                var block = document.getElementById("new_var_block");
                block.remove();
                $("#add_new_var").remove()
                var parent = document.getElementById("modal-body");
                var console_line = document.createElement("div");
                console_line.setAttribute("id", data.var_name + "full_line");
                var title = document.createElement("label");
                title.setAttribute("style", "width: 100%;");
                title.textContent = data.var_name;
                var body = document.createElement("input");
                body.setAttribute("style", "width: 90%;");
                body.setAttribute("id",  data.var_name);
                body.value = data.var_value;
                var confirm = document.createElement("a");
                var confirm_img = document.createElement("img");
                confirm_img.setAttribute("src", "source/images/confirm.svg");
                confirm_img.setAttribute("width", "20");
                confirm_img.setAttribute("height", "20");
                confirm.appendChild(confirm_img);
                confirm.setAttribute("onclick", "update_var('" + data.var_name + "'," + app + "," + key +");");
                var remove = document.createElement("a");
                var remove_img = document.createElement("img");
                remove_img.setAttribute("src", "source/images/trash.svg");
                remove_img.setAttribute("width", "20");
                remove_img.setAttribute("height", "20");
                remove.appendChild(remove_img);
                remove.setAttribute("onclick", "delete_var('" + data.var_name + "'," + app + "," + key +");");
                console_line.appendChild(title);
                console_line.appendChild(body);
                console_line.appendChild(confirm);
                console_line.appendChild(remove);
                parent.appendChild(console_line);
                var console_line = document.createElement("div");
                console_line.setAttribute("style", "text-align: center; font-size: 25px;");
                var body = document.createElement("a");
                body.setAttribute("id", "add_new_var");
                body.textContent = "+";
                body.setAttribute("onclick", "add_var(" + app + "," + key +");")
                console_line.appendChild(body);
                parent.appendChild(console_line);
            }
        }
        else if (xhr.readyState === 4 && xhr.status === 404) {
            check.checked = false;
            create_message(JSON.parse(xhr.responseText).res, "error");
        }
    }
    xhr.send(JSON.stringify(data));
}

function delete_var(title, app, key){
    var block = document.getElementById(title + "full_line");
    block.remove();
    var data = {};
    data.app = app;
    data.key = key;
    data.title = title;
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', "/heroku/var/");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            create_message(JSON.parse(xhr.responseText).res, "info");
        }
        else if (xhr.readyState === 4 && xhr.status === 404) {
            check.checked = false;
            create_message(JSON.parse(xhr.responseText).res, "error");
        }
    }
    xhr.send(JSON.stringify(data));
}

function heroku_addon(block, key, app){
    var parent = document.getElementById(block + "_addon");
    if (parent.textContent == ""){
        show_loader(parent)
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/heroku/addon?key=' + key + "&app=" + app, true);
        xhr.onreadystatechange = function(){
            if (xhr.readyState === 4 && xhr.status === 200){
                parent.className = "console";
                parent.textContent = "";
                JSON.parse(xhr.responseText).res.forEach((element) => {
                    var console_line = document.createElement("div");
                    var title_div = document.createElement("div");
                    title_div.className = "console_title";
                    title_div.textContent = element.title;
                    var body_div = document.createElement("div");
                    body_div.className = "console_body";
                    body_div.textContent = element.body;
                    console_line.appendChild(title_div);
                    console_line.appendChild(body_div);
                    parent.appendChild(console_line);
                });
            }
            else if (xhr.readyState === 4 && xhr.status != 200){
                parent.className = ""; parent.textContent = "";
            }
        }
        xhr.send();
    }
    else { parent.className = ""; parent.textContent = ""; }
}

function enable_project(check, key, app){
    var data = {}
    var xhr = new XMLHttpRequest();
    data.enable = check.checked;
    data.key = key;
    data.app = app;
    xhr.open('PATCH', "/heroku/");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            create_message(JSON.parse(xhr.responseText).res, "info");
        }
        else if (xhr.readyState === 4 && xhr.status === 404) {
            check.checked = false;
            create_message(JSON.parse(xhr.responseText).res, "error");
        }
    }
    xhr.send(JSON.stringify(data));
}

function hide_sidebar(){
    if (sidebar1.className === "sidebar js-sidebar"){ sidebar1.className = "sidebar js-sidebar collapsed"; }
    else{ sidebar1.className = "sidebar js-sidebar"; }
}

function set_permissions(up, user){
    if (window.confirm('Are you sure?'))
    {
        var data = {}
        data.up = up;
        data.user = user;
        var xhr = new XMLHttpRequest();
        xhr.open('PATCH', "/admin/permissions/");
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.onreadystatechange = function(){
            if (xhr.readyState === 4 && xhr.status === 200){ create_message("Current permissions: " + xhr.responseText, "info"); }
        }
        xhr.send(JSON.stringify(data));
    }
}

function delete_user(user){
    if (window.confirm('Are you sure?'))
    {
        var xhr = new XMLHttpRequest();
        xhr.open('DELETE', "/admin/user/" + user);
        xhr.onreadystatechange = function(){ if (xhr.readyState === 4 && xhr.status === 200){ create_message("Successful deleted!", "info"); }}
        xhr.send();
    }
}

function create_message(text, class_name){
    var block = document.createElement("div");
    block.setAttribute("class", class_name);
    block.textContent = text;
    alert_box.appendChild(block);
    setTimeout(remove_message, 8000, block);
}

function remove_message(block){ block.remove(); }

$(document).ready(function() {
    page = localStorage.getItem("current_page")
    if (page == null){ localStorage.setItem("current_page", "1"); }
    else{
        if (page === "2") { untracked(); }
        else if (page === "3") { logs(); }
        else if (page === "4") { errors(); }
        else if (page === "5") { users(); }
        else if (page === "6") { swagger(); }
        else if (page === "7") { heroku(); }
    }
});