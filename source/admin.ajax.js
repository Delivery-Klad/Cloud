var place_holder = document.getElementById("place_holder1");
var sidebar1 = document.getElementById("sidebar");

function create_arrow(up, user){
    var a_block = document.createElement("a");
    a_block.setAttribute("href", "javascript:set_permissions(" + up + "," + user + ");");
    var arrow = document.createElement("img");
    if (up === true){ arrow.setAttribute("src", "source/up_arrow.svg"); }
    else{ arrow.setAttribute("src", "source/down_arrow.svg"); }
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
    document.getElementById("sidebar" + num).className = "sidebar-item active";
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
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/dashboard/');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            toggle_menu(1);
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
        if (xhr.readyState === 4 && xhr.status === 403){ alert(JSON.parse(xhr.responseText).res); }
    }
    xhr.send();
}

function untracked(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/dashboard/?arg=true');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            toggle_menu(2);
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
        if (xhr.readyState === 4 && xhr.status === 403){ alert(JSON.parse(xhr.responseText).res); }
    }
    xhr.send();
}

function logs(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/logs');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            toggle_menu(3);
			fill_placeholder(xhr.responseText, "javascript:clear_logs();")
        }
        else if (xhr.readyState === 4 && xhr.status === 403){ alert(xhr.responseText); }
    }
    xhr.send();
}

function clear_logs(){
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/admin/clear_logs');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){ fill_placeholder(xhr.responseText, "javascript:clear_logs();") }
        else if (xhr.readyState === 4 && xhr.status === 403){ alert(xhr.responseText); }
    }
    xhr.send();
}

function errors(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/errors');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            toggle_menu(4);
			fill_placeholder(xhr.responseText, "javascript:clear_errors();")
        }
        else if (xhr.readyState === 4 && xhr.status === 403){ alert(xhr.responseText); }
    }
    xhr.send();
}

function clear_errors(){
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/admin/clear_errors');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){ fill_placeholder(xhr.responseText, "javascript:clear_errors();") }
        else if (xhr.readyState === 4 && xhr.status === 403){ alert(xhr.responseText); }
    }
    xhr.send();
}

function users(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/users');
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
            toggle_menu(5);
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
        else if (xhr.readyState === 4 && xhr.status === 403){ alert(JSON.parse(xhr.responseText).res); }
    }
    xhr.send();
}

function push_files(){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/admin/');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){ alert(xhr.responseText); }
        if (xhr.readyState === 4 && xhr.status === 403){ alert(xhr.responseText); }
    }
    xhr.send();
}

function swagger(){
    toggle_menu(6);
    place_holder.textContent = "";
    var docs_page = document.createElement("iframe");
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/swagger/');
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){ docs_page.setAttribute("src", JSON.parse(xhr.responseText).res); }
    }
    xhr.send();
    docs_page.setAttribute("width", "100%");
    docs_page.setAttribute("height", "100%");
    docs_page.setAttribute("scrolling", "auto%");
    place_holder.append(docs_page);
}

function hide_sidebar(){
    if (sidebar1.className === "sidebar js-sidebar"){ sidebar1.className = "sidebar js-sidebar collapsed"; }
    else{ sidebar1.className = "sidebar js-sidebar"; }
}

function set_permissions(up, user){
    if (window.confirm('Are you sure?'))
    {
        var xhr = new XMLHttpRequest();
        xhr.open('PATCH', "admin/permissions/?up=" + up + "&user=" + user);
        xhr.onreadystatechange = function(){
            if (xhr.readyState === 4 && xhr.status === 200){ alert("Current permissions: " + xhr.responseText); }
        }
        xhr.send();
    }
}

function delete_user(user){
    if (window.confirm('Are you sure?'))
    {
        var xhr = new XMLHttpRequest();
        xhr.open('DELETE', "admin/user/" + user);
        xhr.onreadystatechange = function(){ if (xhr.readyState === 4 && xhr.status === 200){ alert("Successful deleted!"); }}
        xhr.send();
    }
}

$(document).ready(function() {
    page = localStorage.getItem("current_page")
    if (page == null){ localStorage.setItem("current_page", 1); }
    else{
        if (page === "2") { untracked(); }
        else if (page === "3") { logs(); }
        else if (page === "4") { errors(); }
        else if (page === "5") { users(); }
        else if (page === "6") { swagger(); }
    }
});