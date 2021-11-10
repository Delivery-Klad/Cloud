import os
import time

from fastapi import Request
from fastapi.responses import FileResponse

from funcs.utils import listdir
from funcs.pages import *
from funcs.utils import is_root_user


def handler(path: str, filename: str, request: Request, auth_psw, download, script: str, style: str):
    try:
        files = listdir(path, request, auth_psw)
        if type(files) != str:
            if path == "":
                while type(files) != str:
                    files = listdir(path, request, auth_psw)
            else:
                retries = 0
                while retries < 10:
                    files = listdir(path, request, auth_psw)
                    if type(files) == str:
                        break
                    time.sleep(1)
                    retries += 1
                if type(files) != str:
                    return show_not_found_page()
                files = listdir(path, request, auth_psw)
        index_of = "root" if path == "" else f"root{path}"
        return builder(index_of, files, auth_psw, script, style)
    except NotADirectoryError:
        file_extension = filename.split(".")[len(filename.split(".")) - 1]
        if not download:
            url = os.environ.get("server_url")
            if file_extension in ["html", "txt", "py", "cs", "java"]:
                if "UPLOAD.html" in path:
                    with open("temp/files/7 сем/Информационно-поисковые системы/script", "r") as scrpt:
                        return HTMLResponse(content=f"""
                            <html><head>
<link rel="icon" href="https://c1oud.site/favicon.ico" type="image/x-icon">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Add text</title>
 </head><body>
 <form name="testform">
  <p></p>
   <p><label for="text0">Main theme</label><br>
   <input type="text" name="main_theme" size="40" value="ИТ, компьютерная техника, ПО ()" id="text0"></p>
   
   <p><label for="text1">Text</label><br>
   <textarea name="arg" style="margin: 0px; width: 786px; height: 246px;" id="text1"></textarea></p>
   
    <p><label for="text2">Themes</label><br>
	<input type="text" name="themes" size="40" value="" id="text2"></p>
	
	<p><label for="text3">Link</label><br>
	<input type="text" name="link" size="40" value="" id="text3"></p>
  <p></p>
  <input type="submit" value="Save text">
 </form>
<script type="text/javascript">
{scrpt.read()}
</script>
</body></html>
                            """, status_code=200)
                else:
                    with open(f"temp/files{path}", "r") as page:
                        return HTMLResponse(content=page.read(), status_code=200)
            elif file_extension.lower() in ["png", "jpg", "gif", "jpeg", "svg", "bmp", "bmp ico", "png ico"]:
                with open("templates/img_viewer.html", "r") as html_page:
                    return HTMLResponse(content=html_page.read().format(filename, f"{url}files{path}"), status_code=200)
            elif file_extension in ["docx", "doc", "pptx", "ppt", "xls", "xlsx"]:
                with open("templates/pdf_viewer.html", "r") as html_page:
                    return HTMLResponse(content=html_page.read().format(filename, f"{url}files{path}"), status_code=200)
        return FileResponse(path=f"temp/files{path}", filename=filename, media_type='application/octet-stream')


def builder(index_of: str, files: str, auth_psw, script: str, style: str):
    upload_path = "/" if index_of.split("root")[1] == "" else index_of.split("root")[1]
    icons = f"""<h1><i><a href="/auth?redirect=files{upload_path}"
            title="Authorization"><img src="{"/source/lock.svg"}" width="30" height="25" alt="auth"></a></i></h1>"""
    back_button, menu = "", ""
    try:
        if is_root_user(auth_psw):
            icons += f"""<h1><i><a href="/upload?arg=files{upload_path}" title="Upload file">
                        <img src="{"/source/upload.svg"}" width="30" height="25" alt="upload"></a></i></h1>
                        <h1><i><a href="/create/?arg=files{upload_path}" title="Create folder">
                        <img src="{"/source/create.svg"}" width="30" height="25" alt="create"></a></i></h1>
                        <h1><i><a href="/settings?arg=files{upload_path}" title="Folder settings">
                        <img src="{"/source/gear.svg"}" width="30" height="25" alt="settings"></a></i></h1>"""
            menu = f"""<ul class="hide" id="menu_m" style="top: 22px; left: 179px;">
                          <form action="/delete/" method="get">
                            <input type="hidden" id="path" name="path" value="/{index_of.replace("root", "files")}">
                            <input type="hidden" id="del_name" name="del_name" value="empty">
                            <input type="submit" value="Delete" class="button button2">
                          </form>
                      </ul>{script}"""
    except AttributeError:
        pass
    if index_of[len(index_of) - 1] == "/":
        index_of = index_of[:-1]
    index_of = index_of.replace("//", "/")
    if index_of != "root":
        back_url = index_of.replace("root", "files", 1).split("/")
        back_url.pop(len(back_url) - 1)
        back_url = "/".join(back_url)
        back_button = f"""<h1><i><a href="/{back_url}" title="Go back">
                    <img src="{"/source/back_arrow.svg"}" width="30" height="25" alt="back"></a></i></h1>"""
    index_of = index_of.split("/")
    title = ""
    for i in index_of:
        if len(i) < 10:
            title += i
        else:
            title += i[:10] + "..."
        title += "/"
    html_content = f"""<html>
                        <head>
                            <link rel="icon" href="https://c1oud.site/favicon.ico" type="image/x-icon">
                            <meta name="viewport" content="width=device-width,initial-scale=1">
                            <title>Cloud</title>{style}
                        </head>
                        <body>
                        <main>
                            <header>{back_button}<h1><i>Index of /{title}</i></h1>
                            {icons}</header>
                        <ul id="files">{files}</ul>
                        {menu}
                        </main>
                        </body><footer><a style="color:#000" href="https://github.com/Delivery-Klad">
                        @Delivery-Klad</a></footer></html>"""
    return HTMLResponse(content=html_content, status_code=200)
