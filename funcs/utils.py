import os
import re
from datetime import datetime

from fastapi import Request
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import HTMLResponse, RedirectResponse

from funcs.database import get_permissions


def is_root_user(request: Request, cookie: str):
    try:
        if get_jwt_sub(request, cookie).split("://:")[0] == "5":
            return True
        else:
            return False
    except AttributeError:
        return False


def is_privileged_user(request: Request, cookie: str):
    try:
        subject = get_jwt_sub(request, cookie).split("://:")[0]
        if subject == "3" or subject == "5":
            return True
        else:
            return False
    except AttributeError:
        return False


def is_authorized_user(request: Request, cookie: str):
    try:
        if type(get_jwt_sub(request, cookie).split("://:")[0]) == str:
            return True
        else:
            return False
    except AttributeError:
        return False


def fail_response(redirect: str):  # пока не используется
    response = RedirectResponse(redirect)
    response.delete_cookie("auth_psw")
    return response


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
    with open("templates/500.html", "r") as page:
        return HTMLResponse(page.read())


def clear_log(table: str):
    with open(table, "w") as log_file:
        log_file.write(f"Log cleared {str(datetime.utcnow())[:-7]}")


def sort_dir_files(listdir_files):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    return sorted(listdir_files, key=lambda key: [convert(c) for c in re.split('([0-9]+)', key)])


def create_new_folder(path, arg, access):
    if path[len(path) - 1] == "/":
        path = path[:-1]
    print(path)
    os.mkdir(f"temp/{path}/{arg}")
    if access == "root":
        with open(f"temp/{path}/{arg}/hidden", "w") as access_file:
            access_file.write("init")
    elif access == "auth":
        with open(f"temp/{path}/{arg}/viewer", "w") as access_file:
            access_file.write("init")
    elif access == "privilege":
        with open(f"temp/{path}/{arg}/privilege", "w") as access_file:
            access_file.write("init")
    else:
        with open(f"temp/{path}/{arg}/init", "w") as access_file:
            access_file.write("init")
    if path[len(path) - 1] == "/":
        path = path[:-1]
    return {"res": True}


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
                if not is_root_user(request, auth_psw):
                    return "<li>Access denied</li>"
            except AttributeError:
                return "<li>Access denied</li>"
        elif "privilege" in files:
            try:
                if not is_privileged_user(request, auth_psw):
                    return "<li>Access denied</li>"
            except AttributeError:
                return "<li>Access denied</li>"
        elif "viewer" in files:
            try:
                if not is_authorized_user(request, auth_psw):
                    return f"""<li>Access denied</li> <a href="/auth?redirect=files{directory}" 
                                title="Authorization">Login or register</a>"""
            except AttributeError:
                return f"""<li>Access denied</li> <a href="/auth?redirect=files{directory}" 
                            title="Authorization">Login or register</a>"""
        for i in files:
            if i == "hidden" or i == "init" or i == "viewer" or i == "privilege" or (".meta" in i):
                continue
            if len(i.split(".")) == 1:
                file_class = "folder"
            else:
                file_type = i.split(".")
                file_type = file_type[len(file_type) - 1]
                if file_type.lower() in ["png", "jpg", "bmp", "gif", "jpeg", "heic"]:
                    file_class = "png"
                else:
                    file_class = "file"
            local_files += f"""<li id="{i}">
                <a href="/files{directory}/{i}" title="{i}" 
                class="{file_class}">{i}</a></li>"""
        return local_files
    except FileNotFoundError:
        return HTMLResponse(status_code=404)


def get_folder_access_level(path: str):
    try:
        files = os.listdir(f"temp/{path}")
        if "hidden" in files:
            return {"res": 1}
        elif "viewer" in files:
            return {"res": 2}
        elif "init" in files:
            return {"res": 3}
        elif "privilege" in files:
            return {"res": 4}
        else:
            return {"res": 3}
    except FileNotFoundError:
        return HTMLResponse(status_code=404)


def constructor(icons, upload_path):
    icons += f"""<h1><i><a href="/admin?arg=files{upload_path}" title="Folder settings">
                 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" 
                  fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" 
                  stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line>
                  <line x1="23" y1="11" x2="17" y2="11"></line></svg></a></i></h1>"""
    return icons


def get_menu(index_of, is_root):
    menu = f"""<ul class="hide" id="menu_m" style="top: 22px; left: 179px;">
                  <form method="get">
                      <div id="meta_place_holder"></div>
                      <input type="hidden" id="file_path" name="path" value="/{index_of.replace("root", "files")}">
                      <input type="hidden" id="file_name" name="del_name" value="empty">"""
    if is_root:
        with open("source_admin/context.js", "r") as data:
            admin_script = data.read()
        menu += f"""<div><input id="new_name" name="new_name" size="27"></div>
                <div><input onclick="rename_file();" value="Rename" id="rename_btn" class="button button2"></div>
                <div><input onclick="delete_file();" value="Delete" id="delete_btn" class="button button2"></div>
                <div id="access_holder"></div></form>
                </ul>
                <ul class="hide" id=scnd_menu style="top: 22px; left:179px;"><div>
                <div><input id="folder_name" name="folder_name" size="27"></div>
                <div><input type="hidden" id="folder_path" value="/{index_of.replace("root", "files")}"></div>
                <div><input onclick="create_new_folder();" value="Create" class="button button2"></div>
                <div id="access_holder">
                <div><input id="radio-1" type="radio" name="folder_access" 
                value="root"><label for="radio-1">Root</label></div><div><input id="radio-2" type="radio" 
                name="folder_access" value="auth"><label for="radio-2">Authorized
                </label></div><div><input id="radio-3" type="radio" name="folder_access" value="all" checked><label 
                for="radio-3">All users</label></div><div><input id="radio-4" type="radio" name="folder_access" 
                value="privilege"><label for="radio-4">Privileged</label></div></div>
                <form id="data" enctype="multipart/form-data" 
                method="post">
                    <div class="upload">
                        <label class="label">
                          <input id="upload_path" type="hidden" value="{index_of.replace("root", "files")}/">
                          <input type="file" name="data">
                        </label>
                    </div>
                    <input class="button button2" type="submit" value="Upload">
                </div></form></ul>{admin_script}"""
    else:
        with open("source/context.js", "r") as data:
            script = data.read()
        menu += f"""<input type="hidden" id="new_name" name="new_name" size="27"></form></ul>{script}"""
    return menu


def check_cookies(request: Request, cookie: str):
    try:
        permissions = get_permissions(get_jwt_sub(request, cookie).split("://:")[1])
        if permissions == 5:
            return "Administrator"
        elif permissions is None:
            return "Revoke"
        else:
            return "Authorized user"
    except AttributeError:
        return "Unauthorized"


def get_jwt_sub(request: Request, cookie: str):
    request.headers.__dict__["_list"].append(("authorization".encode(), f"Bearer {cookie}".encode()))
    authorize = AuthJWT(request)
    try:
        return authorize.get_jwt_subject()
    except Exception as e:
        if str(e) == "":
            return None
        else:
            error_log(str(e))
            return None
