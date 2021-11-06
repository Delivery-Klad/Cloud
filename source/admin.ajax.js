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

function open_dashboard(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/admin/dashboard/');

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
			alert("success");
        }
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(xhr.responseText);
        }
    }
    xhr.send()
}