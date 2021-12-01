import os
import re
from datetime import datetime

from fastapi import Request
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import RedirectResponse, HTMLResponse

from funcs.database import get_permissions


def is_root_user(cookie: str):
    try:
        if cookie.split("://:")[0] == "5":
            return True
        else:
            return False
    except AttributeError:
        return False


def is_authorized_user(cookie: str):
    try:
        if type(cookie.split("://:")[0]) == str:
            return True
        else:
            return False
    except AttributeError:
        return False


def log(text: str, code: bool = False):
    with open("log.txt", "a") as log_file:
        if code:
            log_file.write(f" - {text}")
        else:
            log_file.write(f"\n{str(datetime.utcnow())[:-7]} - {text}")


def error_log(text: str):
    print(text)
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"\n{str(datetime.utcnow())[:-7]} - {text}")


def clear_log(table: str):
    with open(table, "w") as log_file:
        log_file.write(f"Log cleared {str(datetime.utcnow())[:-7]}")


def sort_dir_files(listdir_files):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    return sorted(listdir_files, key=lambda key: [convert(c) for c in re.split('([0-9]+)', key)])


def create_new_folder(path, arg, access):
    os.mkdir(f"temp/{path}/{arg}")
    if path == "files/":
        path = path[:-1]
    if access == "root":
        with open(f"temp/{path}/{arg}/hidden", "w") as hidden:
            hidden.write("init")
    elif access == "auth":
        with open(f"temp/{path}/{arg}/viewer", "w") as viewer:
            viewer.write("init")
    else:
        with open(f"temp/{path}/{arg}/init", "w") as init:
            init.write("init")
    if path[len(path) - 1] == "/":
        path = path[:-1]
    return RedirectResponse(f"/{path}", status_code=302)


def listdir(directory: str, request: Request, auth_psw):
    local_files = ""
    try:
        files = os.listdir(f"temp/files{directory}")
        if directory == "":
            while "7 сем" not in files or "Other" not in files:
                files = os.listdir(f"temp/files{directory}")
        files = sort_dir_files(os.listdir(f"temp/files{directory}"))
        if "hidden" in files:
            try:
                if not is_root_user(auth_psw):
                    return "<li>Access denied</li>"
            except AttributeError:
                return "<li>Access denied</li>"
        elif "viewer" in files:
            try:
                if not is_authorized_user(auth_psw):
                    return f"""<li>Access denied</li> <a href="/auth?redirect=files{directory}" 
                                title="Authorization">Login or register</a>"""
            except AttributeError:
                return f"""<li>Access denied</li> <a href="/auth?redirect=files{directory}" 
                            title="Authorization">Login or register</a>"""
        for i in files:
            if i == "hidden" or i == "init" or i == "viewer" or (".meta" in i):
                continue
            file_class = "folder" if len(i.split(".")) == 1 else "file"
            local_files += f"""<li>
                <a href="/files{directory}/{i}" title="/files{directory}/{i}" 
                class="{file_class}">{i}</a></li>"""
        return local_files
    except FileNotFoundError:
        return HTMLResponse(status_code=404)


def constructor(icons, upload_path):
    icons += f"""<h1><i><a href="/upload?arg=files{upload_path}" title="Upload file">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                 viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                 stroke-linecap="round" stroke-linejoin="round">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                <polyline points="17 8 12 3 7 8"></polyline>
                                <line x1="12" y1="3" x2="12" y2="15"></line>
                            </svg></a></i></h1>
                            <h1><i><a href="/create/?arg=files{upload_path}" title="Create folder">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                 viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                 stroke-linecap="round" stroke-linejoin="round">
                                <line x1="12" y1="5" x2="12" y2="19"></line>
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                            </svg></a></i></h1>
                            <h1><i><a href="/settings?arg=files{upload_path}" title="Folder settings">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                 viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="12" cy="12" r="3"></circle>
                                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0
                                0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2
                                2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0
                                0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0
                                0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1
                                2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2
                                0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65
                                0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51
                                1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0
                                2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1
                                2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z">
                                </path>
                            </svg></a></i></h1>
                            <h1><i><a href="/admin?arg=files{upload_path}" title="Folder settings">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" 
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" 
                                stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                <circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line>
                                <line x1="23" y1="11" x2="17" y2="11"></line></svg></a></i></h1>"""
    return icons


def get_menu(index_of, is_root):
    with open("source/context.js", "r") as context:
        script = context.read()
    menu = f"""<ul class="hide" id="menu_m" style="top: 22px; left: 179px;">
                  <form method="get">
                      <div id="meta_place_holder"></div>
                      <input type="hidden" id="path" name="path" value="/{index_of.replace("root", "files")}">
                      <input type="hidden" id="del_name" name="del_name" value="empty">
                    <input type="hidden" id="new_name" name="new_name" size="27" >"""
    if is_root:
        menu += f"""<div><input id="new_name" name="new_name" size="27" ></div>
                <div><input formaction="/rename/" type="submit" value="Rename" class="button button2"></div>
                <div><input formaction="/delete/" type="submit" value="Delete" class="button button2"></div>
                </form>
                </ul>{script}"""
    else:
        menu += f"""</form></ul>{script}"""
    return menu


def check_cookies(request: Request, cookie: str):
    try:
        permissions = get_permissions(get_jwt_sub(request, cookie.split("://:")[1]))
        if permissions == 5:
            return "Administrator"
        else:
            return "Authorized user"
    except AttributeError:
        return "Unauthorized"


def get_jwt_sub(request: Request, cookie: str):
    request.headers.__dict__["_list"].append(("authorization".encode(), f"Bearer {cookie}".encode()))
    authorize = AuthJWT(request)
    return authorize.get_jwt_subject()
