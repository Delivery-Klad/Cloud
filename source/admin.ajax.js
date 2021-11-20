var place_holder = document.getElementById("place_holder1")
var sidebar1 = document.getElementById("sidebar")

function open_dashboard(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/dashboard/');

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
            document.getElementById("sidebar2").className = "sidebar-item";
            document.getElementById("sidebar3").className = "sidebar-item";
            document.getElementById("sidebar4").className = "sidebar-item";
            document.getElementById("sidebar1").className = "sidebar-item active";
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
            document.getElementById("sidebar1").className = "sidebar-item";
            document.getElementById("sidebar3").className = "sidebar-item";
            document.getElementById("sidebar4").className = "sidebar-item";
            document.getElementById("sidebar2").className = "sidebar-item active";
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
            document.getElementById("sidebar1").className = "sidebar-item";
            document.getElementById("sidebar2").className = "sidebar-item";
            document.getElementById("sidebar4").className = "sidebar-item";
            document.getElementById("sidebar3").className = "sidebar-item active";
			var arr = JSON.parse(xhr.responseText).res;
            place_holder.textContent = "";
            arr.forEach((element) => {
                let block = document.createElement('div');
                block.textContent += element;
                place_holder.append(block);
            })
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
            document.getElementById("sidebar1").className = "sidebar-item";
            document.getElementById("sidebar2").className = "sidebar-item";
            document.getElementById("sidebar3").className = "sidebar-item";
            document.getElementById("sidebar4").className = "sidebar-item active";
			var arr = JSON.parse(xhr.responseText).res;
            place_holder.textContent = "";
            arr.forEach((element) => {
                let block = document.createElement('div');
                block.textContent += element;
                place_holder.append(block);
            })
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
