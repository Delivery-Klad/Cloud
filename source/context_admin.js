<script type="text/javascript">
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
        } else {
            console.log(data);
        }
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
    xhr.open("PUT", "/file/", true);
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
        } else {
            console.log(data);
        }
    }
    xhr.send(json);
}
</script>