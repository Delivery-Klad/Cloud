var alert_box = document.getElementById("alert-box");

function create_message(text){
    var block = document.createElement("div");
    block.setAttribute("style", "background-color: #D70000; margin: 5px; padding: 10px; font: 12pt sans-serif;");
    block.textContent = text;
    alert_box.appendChild(block);
    setTimeout(remove_message, 5000, block);
}

function login(){
    var user_login = document.getElementById("login");
    var user_password = document.getElementById("password");
    for (let chr of user_login.value) {
        if (123 < chr.charCodeAt(0) || 33 > chr.charCodeAt(0)) {
            create_message("Использованы неподдерживаемые символы");
            return;
        }
    }
    if (user_login.value === "user"){
        create_message("User не может быть использовано в качестве логина");
        return;
    }
    if (user_login.value === "" || user_password.value === ""){
        create_message("Не все поля заполнены");
        return;
    }
    if (user_login.value.length < 4){
        create_message("Логин слишком короткий");
        return;
    }
    if (user_password.value.length < 8){
        create_message("Пароль слишком короткий");
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
            create_message(JSON.parse(xhr.responseText).result);
        }
    }
    xhr.send();
}

function remove_message(block){
    block.remove();
}

$("form").on('submit', function (e) {
   e.preventDefault();
   login();
});