<script type="text/javascript">
$(document).ready(function() {

  if ($("#file").addEventListener) {
    $("#file").addEventListener('contextmenu', function(e) {
      alert("You've tried to open context menu");
      e.preventDefault();
    }, false);
  } else {

    $('body').on('contextmenu', 'a.file', function() {
      document.getElementById("menu_m").className = "show";
      var text = $(this).contents()[0].nodeValue.trim();
      document.getElementById('del_name').value = text;
      document.getElementById("menu_m").style.top = mouseY(event) + 'px';
      document.getElementById("menu_m").style.left = mouseX(event) + 'px';
      window.event.returnValue = false;
    });
  }
});

$(document).bind("click", function(event) {
  document.getElementById("menu_m").className = "hide";
});
// 85
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
</script>