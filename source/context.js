<script type="text/javascript">
var place_holder = document.getElementById("meta_place_holder")
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
      document.getElementById("menu_m").className = "show";
      document.getElementById('file_name').value = text;
      document.getElementById("menu_m").style.top = mouseY(event) + 'px';
      document.getElementById("menu_m").style.left = mouseX(event) + 'px';
      setFocusToTextBox();
      window.event.returnValue = false;
    });
  }
});

$(document).bind("click", function(event) {
    if (event.target.name === "new_name"){
        return;
    }
    place_holder.textContent = "";
    document.getElementById("menu_m").className = "hide";
});

function mouseX(evt) {
  if (evt.pageX) {
    return evt.pageX;
  } else if (evt.clientX) {
    return evt.clientX + (document.documentElement.scrollLeft ?
      document.documentElement.scrollLeft :
      document.body.scrollLeft);
  } else {
    return null;
  }
}

function mouseY(evt) {
  if (evt.pageY) {
    return evt.pageY;
  } else if (evt.clientY) {
    return evt.clientY + (document.documentElement.scrollTop ?
      document.documentElement.scrollTop :
      document.body.scrollTop);
  } else {
    return null;
  }
}

function setFocusToTextBox(){
    document.getElementById("new_name").focus();
}
</script>