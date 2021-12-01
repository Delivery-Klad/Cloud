var place_holder = document.getElementById("place_holder1");
var sidebar1 = document.getElementById("sidebar");

function create_arrow(up, user){
    var a_block = document.createElement("a");
    a_block.setAttribute("href", "javascript:set_permissions(" + up + "," + user + ");");
    var arrow = document.createElement("img");
    if (up === true){
        arrow.setAttribute("src", "source/up_arrow.svg");
    }
    else{
        arrow.setAttribute("src", "source/down_arrow.svg");
    }
    a_block.appendChild(arrow);
    return a_block;
}

function toggle_menu(num){
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

function set_table_attributes(table){
    table.setAttribute("style", "width:100%");
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
}

function open_dashboard(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/dashboard/');

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
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
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(JSON.parse(xhr.responseText).res);
        }
    }
    xhr.send()
}

function untracked(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/dashboard/?arg=true');

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
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
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(JSON.parse(xhr.responseText).res);
        }
    }
    xhr.send()
}

function logs(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/logs/');

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
            toggle_menu(3);
			fill_placeholder(xhr.responseText, "javascript:clear_logs();")
        }
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(xhr.responseText);
        }
    }
    xhr.send()
}

function clear_logs(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/clear_logs/');

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
			fill_placeholder(xhr.responseText, "javascript:clear_logs();")
        }
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(xhr.responseText);
        }
    }
    xhr.send()
}

function errors(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/errors/');

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
            toggle_menu(4);
			fill_placeholder(xhr.responseText, "javascript:clear_errors();")
        }
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(xhr.responseText);
        }
    }
    xhr.send()
}

function clear_errors(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/clear_errors/');

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
			fill_placeholder(xhr.responseText, "javascript:clear_errors();")
        }
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(xhr.responseText);
        }
    }
    xhr.send()
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
            set_table_attributes(table);
            set_table_header(table);
            arr.forEach((element) => {
                if (element === "Users"){
                    let block = document.createElement('div');
                    block.setAttribute("style", "font-weight: bold; font-size: 20px;");
                    block.textContent += element;
                    place_holder.append(block);
                }
                else{
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
                }
            })
            place_holder.append(table);
        }
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(JSON.parse(xhr.responseText).res);
        }
    }
    xhr.send()
}

function push_files(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/push_files/');

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
			alert(xhr.responseText);
        }
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(xhr.responseText);
        }
    }
    xhr.send()
}

function swagger(){
    toggle_menu(6);
    place_holder.textContent = "";
    var docs_page = document.createElement("iframe");
    docs_page.setAttribute("src", "doCUMentation");
    docs_page.setAttribute("width", "100%");
    docs_page.setAttribute("height", "100%");
    docs_page.setAttribute("scrolling", "auto%");
    place_holder.append(docs_page);
}

function hide_sidebar(){
    if(sidebar1.className === "sidebar js-sidebar"){
        sidebar1.className = "sidebar js-sidebar collapsed";
    }
    else{
        sidebar1.className = "sidebar js-sidebar";
    }
}

function set_permissions(up, user){
    if (window.confirm('Are you sure?'))
    {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', "admin/permissions/?up=" + up + "&user=" + user);
        xhr.onreadystatechange = function(){
            if(xhr.readyState === 4 && xhr.status === 200){
                alert("Current permissions: " + xhr.responseText);
            }
        }
        xhr.send();
    }
}
