import os
import re
from datetime import datetime

import bcrypt
from fastapi import Request
from fastapi.responses import RedirectResponse, HTMLResponse


def is_root_user(password: str):
    try:
        return bcrypt.checkpw(os.environ.get("root_psw").encode("utf-8"), password.encode("utf-8"))
    except AttributeError:
        return False


def is_authorized_user(password: str):
    try:
        return bcrypt.checkpw(os.environ.get("viewer_key").encode("utf-8"), password.encode("utf-8")) or \
               bcrypt.checkpw(os.environ.get("root_psw").encode("utf-8"), password.encode("utf-8"))
    except AttributeError:
        return False


def log(text: str, code: bool = False):
    with open("log.txt", "a") as log_file:
        if code:
            log_file.write(f" - {text}")
        else:
            log_file.write(f"\n{str(datetime.utcnow())[:-7]} - {text}")


def error_log(text: str):
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
                    return "<li>Access denied</li>"
            except AttributeError:
                return "<li>Access denied</li>"
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
                            <img src="/source/upload.svg" width="30" height="25" alt="upload"></a></i></h1>
                            <h1><i><a href="/create/?arg=files{upload_path}" title="Create folder">
                            <img src="/source/create.svg" width="30" height="25" alt="create"></a></i></h1>
                            <h1><i><a href="/settings?arg=files{upload_path}" title="Folder settings">
                            <img src="/source/gear.svg" width="30" height="25" alt="settings"></a></i></h1>"""
    return icons


def get_menu(index_of, is_root):
    with open("source/context.js", "r") as context:
        script = context.read()
    menu = f"""<ul class="hide" id="menu_m" style="top: 22px; left: 179px;">
                  <form action="/delete/" method="get">
                      <div id="meta_place_holder">test</div>
                      <input type="hidden" id="path" name="path" value="/{index_of.replace("root", "files")}">
                      <input type="hidden" id="del_name" name="del_name" value="empty">"""
    if is_root:
        menu += f"""<input type="submit" value="Delete" class="button button2">
                </form>
                </ul>{script}"""
    else:
        menu += f"""</form></ul>{script}"""
    return menu


def check_cookies(cookies):
    try:
        if bcrypt.checkpw(os.environ.get("root_psw").encode("utf-8"), cookies.encode("utf-8")):
            return "Administrator"
        if bcrypt.checkpw(os.environ.get("viewer_key").encode("utf-8"), cookies.encode("utf-8")):
            return "Authorized user"
    except AttributeError:
        return "Unauthorized"
