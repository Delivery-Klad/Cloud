function replace(old_path, new_path){
    var data = {};
    data.old_path = old_path;
    data.new_path = new_path;
    var json = JSON.stringify(data);
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", "/" + document.getElementById("type").value + "/", true);
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.location.href = new_path;
        }
    }
    xhr.send(json);
}