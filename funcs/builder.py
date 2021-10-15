import os
import time

import mammoth
from fastapi import Request
from fastapi.responses import FileResponse

from funcs.listdir import listdir
from funcs.pages import *
from funcs.utils import is_root_user


def handler(path: str, filename: str, request: Request, auth_psw, download, script: str, style: str):
    try:
        files = listdir(path, request, auth_psw)
        if type(files) != str:
            if path == "":
                for i in range(10):
                    files = listdir(path, request, auth_psw)
                    if type(files) != str:
                        time.sleep(1)
                    else:
                        break
                time.sleep(1)
                if type(files) != str:
                    return show_not_found_page()
            else:
                return show_not_found_page()
        index_of = "root" if path == "" else f"root{path}"
        return builder(index_of, files, auth_psw, script, style)
    except NotADirectoryError:
        file_extension = filename.split(".")[len(filename.split(".")) - 1]
        url = os.environ.get("server_url")
        if not download:
            if file_extension in ["html", "txt", "py", "cs", "java"]:
                with open(f"temp/files{path}", "r") as page:
                    return HTMLResponse(content=page.read(), status_code=200)
            elif file_extension.lower() in ["png", "jpg", "gif", "jpeg", "svg", "bmp", "bmp ico", "png ico"]:
                with open("templates/img_viewer.html", "r") as html_page:
                    return HTMLResponse(content=html_page.read().format(filename, f"{url}files{path}"), status_code=200)
            elif file_extension == "docx":
                with open(f"temp/files{path}", "rb") as page:
                    res = mammoth.convert_to_html(page)
                with open("templates/doc_reader.html", "r") as html_page:
                    return HTMLResponse(content=html_page.read().format(filename, f"{url}files{path}") + res.value,
                                        status_code=200)
            elif file_extension == "pdf":
                return FileResponse(path=f"temp/files{path}", filename=filename,
                                    media_type='application/octet-stream')
        if file_extension == "pdf":
            with open("templates/pdf_viewer.html", "r") as html_page:
                return HTMLResponse(content=html_page.read().format(filename, f"{url}files{path}"), status_code=200)
        return FileResponse(path=f"temp/files{path}", filename=filename, media_type='application/octet-stream')


def builder(index_of: str, files: str, auth_psw, script: str, style: str):
    upload_path = "/" if index_of.split("root")[1] == "" else index_of.split("root")[1]
    icons = f"""<h1><i><a href="/auth?redirect=files{upload_path}"
            title="Authorization"><img src="{"/source/lock.svg"}" width="30 height="25" alt="auth"></a></i></h1>"""
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
    html_content = f"""<html>
                        <head>
                            <meta name="viewport" content="width=device-width,initial-scale=1">
                            <title>{"Cloud"}</title>{style}
                        </head>
                        <body>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
                        <main>
                            <header>{back_button}<h1><i>Index of /{index_of}</i></h1>
                            {icons}</header>
                        <ul id="files">{files}</ul>
                        {menu}
                        </main>
                        </body><footer><a style="color:#000" href="https://github.com/Delivery-Klad">
                        @Delivery-Klad</a></footer></html>"""
    return HTMLResponse(content=html_content, status_code=200)
