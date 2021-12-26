var place_holder = document.getElementById("meta_place_holder")
var menu_element = document.getElementById("menu_m");

$(document).ready(function() {
    if ($("#file").addEventListener) {
        $("#file").addEventListener('contextmenu', function(e) {
            alert("You've tried to open context menu");
            e.preventDefault();
        }, false);
    } else {
        $('body').on('contextmenu', 'a.file', function() {
            var xhr = new XMLHttpRequest();
            var text = $(this).contents()[0].nodeValue.trim();
            xhr.open('GET', '/file/meta?path=' + document.getElementById("file_path").value + '&name=/' + text);
            xhr.onreadystatechange = function(){
                if(xhr.readyState === 4 && xhr.status === 200){
                    var arr = JSON.parse(xhr.responseText).res;
                    place_holder.textContent = "";
                    arr.forEach((element) => {
                        let block = document.createElement('div');
                        block.textContent += element;
                        place_holder.append(block);
                    })
                }
            }
            xhr.send()
            menu_element.className = "show";
            menu_element.value = text;
            menu_element.style.top = mouseY(event) + 'px';
            menu_element.style.left = mouseX(event) + 'px';
            window.event.returnValue = false;
        });
    }
});

$(document).bind("click", function(event) {
    place_holder.textContent = "";
    menu_element.className = "hide";
});

function mouseX(evt) {
    if (evt.pageX) { return evt.pageX; }
    else if (evt.clientX) {
        return evt.clientX + (document.documentElement.scrollLeft ?
        document.documentElement.scrollLeft : document.body.scrollLeft); }
    else { return null; }
}

function mouseY(evt) {
    if (evt.pageY) { return evt.pageY; }
    else if (evt.clientY) {
        return evt.clientY + (document.documentElement.scrollTop ?
        document.documentElement.scrollTop : document.body.scrollTop); }
    else { return null; }
}