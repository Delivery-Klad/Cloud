import os
import time

from fastapi import Request
from fastapi.responses import FileResponse

from funcs.utils import listdir
from funcs.pages import *
from funcs.utils import is_root_user, constructor, get_menu


def handler(path: str, filename: str, request: Request, auth_psw, download):
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
        return builder(index_of, files, auth_psw)
    except NotADirectoryError:
        file_extension = filename.split(".")[len(filename.split(".")) - 1]
        if not download:
            url = os.environ.get("server_url")
            if file_extension in ["html", "txt", "py", "cs", "java"]:
                with open(f"temp/files{path}", "r") as page:
                    return HTMLResponse(content=page.read(), status_code=200)
            elif file_extension.lower() in ["png", "jpg", "gif", "jpeg", "svg", "bmp", "bmp ico", "png ico"]:
                with open("templates/img_viewer.html", "r") as html_page:
                    return HTMLResponse(content=html_page.read().format(filename, f"{url}files{path}"), status_code=200)
            elif file_extension in ["docx", "doc", "pptx", "ppt", "xls", "xlsx"]:
                with open("templates/pdf_viewer.html", "r") as html_page:
                    return HTMLResponse(content=html_page.read().format(filename, f"{url}files{path}"), status_code=200)
        return FileResponse(path=f"temp/files{path}", filename=filename, media_type='application/octet-stream')


def builder(index_of: str, files: str, auth_psw):
    upload_path = "/" if index_of.split("root")[1] == "" else index_of.split("root")[1]
    icons = f"""<h1><i><a href="/auth?redirect=files{upload_path}"
            title="Authorization"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" 
            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4">
            </path></svg></a></i></h1>"""
    back_button, menu, title = "", "", ""
    try:
        if is_root_user(auth_psw):
            icons = constructor(icons, upload_path)
            menu = get_menu(index_of, True)
        else:
            menu = get_menu(index_of, False)
    except AttributeError:
        menu = get_menu(index_of, False)
    index_of = index_of.replace("//", "/")
    if index_of[len(index_of) - 1] == "/":
        index_of = index_of[:-1]
    if index_of != "root":
        back_url = index_of.replace("root", "files", 1).split("/")
        back_url.pop(len(back_url) - 1)
        back_button = f"""<h1><i><a href="/{"/".join(back_url)}" title="Go back">
                    <img src="/source/back_arrow.svg" width="30" height="25" alt="back"></a></i></h1>"""
    index_of = index_of.split("/")
    for i in index_of:
        if len(i) < 10:
            title += i
        else:
            title += i[:10] + "..."
        title += "/"
    with open("templates/files.html", "r") as html_content:
        return HTMLResponse(content=html_content.read().format(back_button, title, icons, files, menu), status_code=200)
