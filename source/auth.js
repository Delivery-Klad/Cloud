function login(){
    var user_login = document.getElementById("login");
    var user_password = document.getElementById("password");
    for (let chr of user_login.value) {
        if (123 < chr.charCodeAt(0) || 33 > chr.charCodeAt(0)) {
            alert("Использованы неподдерживаемые символы");
            return;
        }
    }
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
    if (user_login.value.length < 4){
        alert("Логин слишком короткий");
        return;
    }
    if (user_password.value.length < 8){
        alert("Пароль слишком короткий");
        return;
    }
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/auth?arg2=' + user_login.value + "&arg=" + user_password.value);

    xhr.onreadystatechange = function(){
        console.log(xhr.status);
        if(xhr.readyState === 4 && xhr.status === 200){
            var redirect = document.getElementById("redir").value;
            if (redirect.slice(-1) === "/"){
                redirect = redirect.slice(0, -1);
            }
            document.location.href = redirect;
        }
        if(xhr.readyState === 4 && xhr.status === 403){
            alert(JSON.parse(xhr.responseText).result);
        }
    }
    xhr.send()
}

$("form").on('submit', function (e) {
   e.preventDefault();
   login();
});