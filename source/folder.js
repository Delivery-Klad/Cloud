function new_folder(){
    var data = {};
    data.path  = document.getElementById("path").value;
    data.arg = document.getElementById("arg").value;
    data.access = document.querySelector('input[name="access"]:checked').value;
    var json = JSON.stringify(data);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/folder/", true);
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.onload = function () {
        var data = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.location.href = document.getElementById("path").value;
        }
    }
    xhr.send(json);
}

function config(){
    var data = {};
    data.path  = document.getElementById("path").value;
    data.arg = document.getElementById("arg").value;
    data.access = document.querySelector('input[name="access"]:checked').value;
    var json = JSON.stringify(data);
    var xhr = new XMLHttpRequest();
    xhr.open("PATCH", "/folder/", true);
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.onload = function () {
        var data = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == 200) {
            var redirect = document.getElementById("path").value.split("/");
            redirect.pop();
            console.log(redirect);
            redirect = redirect.join("/");
            document.location.href = redirect;
        }
    }
    xhr.send(json);
}