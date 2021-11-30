function login(){
    var user_login = document.getElementById("login");
    var user_password = document.getElementById("password");
    if (user_login.value === "user"){
        alert("User не может быть использовано в качестве логина");
        return;
    }
    if (user_login.value === ""){
        alert("Не все поля заполнены");
        return;
    }
    if (user_login.value === ""){
        alert("Не все поля заполнены");
        return;
    }
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/auth?arg2=' + user_login.value + "&arg=" + user_password.value);

    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
            var redirect = document.getElementById("redir");
            document.location.href = redirect.value;
        }
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(JSON.parse(xhr.responseText).result);
        }
    }
    xhr.send()
}