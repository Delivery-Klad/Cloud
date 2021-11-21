var place_holder = document.getElementById("place_holder1")
var sidebar1 = document.getElementById("sidebar")

function toggle_menu(num){
    document.getElementById("sidebar1").className = "sidebar-item";
    document.getElementById("sidebar2").className = "sidebar-item";
    document.getElementById("sidebar3").className = "sidebar-item";
    document.getElementById("sidebar4").className = "sidebar-item";
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

function open_dashboard(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/dashboard/');

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
            toggle_menu(1)
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
            toggle_menu(2)
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
            toggle_menu(3)
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
            toggle_menu(4)
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

function hide_sidebar(){
    if(sidebar1.className === "sidebar js-sidebar"){
        sidebar1.className = "sidebar js-sidebar collapsed";
    }
    else{
        sidebar1.className = "sidebar js-sidebar";
    }
}
