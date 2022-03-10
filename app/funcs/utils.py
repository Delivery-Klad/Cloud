import re
from os import listdir as os_listdir, path as os_path, remove, mkdir
from datetime import datetime

import heroku3
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import HTMLResponse

from app.database import crud, schemas
from app.dependencies import get_settings


settings = get_settings()


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


def log(text: str, code: bool = False):
    print(text)
    with open("log.txt", "a") as log_file:
        if code:
            log_file.write(f" - {text}")
        else:
            log_file.write(f"\n{str(datetime.utcnow())[:-7]} - {text}")


def error_log(text: str):
    print(text)
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"\n{str(datetime.utcnow())[:-7]} - {text}")
    with open("app/templates/500.html", "rb") as page:
        return HTMLResponse(page.read())


def get_app_logs(keys, key: int, app: int):
    cloud = heroku3.from_key(keys[key])
    app = cloud.apps()[app]
    result = []
    for i in app.get_log(lines=10).split("\n"):
        if i == "":
            continue
        i = i.split(": ")
        if len(i) > 1:
            result.append({"title": f"{i[0]}: ", "body": i[1]})
        else:
            result.append({"title": f"{i[0]}: ", "body": ""})
    return result


def get_app_vars(keys, key: int, app: int):
    result = []
    cloud = heroku3.from_key(keys[key])
    app = cloud.apps()[app]
    config = app.config().to_dict()
    for i in config.keys():
        result.append({"title": f"{i}: ", "body": config[i]})
    return result


def update_app_var(keys, data: schemas.UpdateVar):
    try:
        cloud = heroku3.from_key(keys[data.key])
        app = cloud.apps()[data.app]
        config = app.config()
        config[data.var_name] = data.var_value
        return True
    except Exception as e:
        print(e)
        return False


def delete_app_var(keys, data: schemas.DeleteVar):
    try:
        cloud = heroku3.from_key(keys[data.key])
        app = cloud.apps()[data.app]
        config = app.config()
        del config[data.title]
        config[data.title] = None
        return True
    except Exception as e:
        print(e)
        return False


def get_app_addon(keys, key: int, app: int):
    result = []
    cloud = heroku3.from_key(keys[key])
    app = cloud.apps()[app]
    for i in app.addons():
        result.append({"title": "Addon: ", "body": str(i)[8:-2]})
    return result


def get_heroku_projects(keys):
    result = []
    for i in range(len(keys)):
        cloud = heroku3.from_key(keys[i])
        print(f"{cloud.account().email}")
        temp = []
        apps = cloud.apps()
        for j in range(len(apps)):
            enable = "ON"
            if not apps[j].process_formation():
                dyn_type = "database"
            elif "web" in apps[j].process_formation():
                dyn_type = "web"
            elif "worker" in apps[j].process_formation():
                dyn_type = "bot"
            if len(apps[j].dynos()) == 0:
                enable = "OFF"
            temp.append({"name": apps[j].name, "type": dyn_type, "enable": enable, "args": f"{i}, {j}"})
        result.append({"email": cloud.account().email, "apps": temp})
    return result


def clear_log(table: str):
    with open(table, "w") as log_file:
        log_file.write(f"Log cleared {str(datetime.utcnow())[:-7]}")


def sort_dir_files(listdir_files):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    return sorted(listdir_files, key=lambda key: [convert(c) for c in re.split('([0-9]+)', key)])


def create_new_folder(path, arg, access):
    if path[len(path) - 1] == "/":
        path = path[:-1]
    mkdir(f"temp/{path}/{arg}")
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
        files = os_listdir(f"temp/files{directory}")
        if directory == "":
            while "7 сем" not in files or "Other" not in files:
                files = os_listdir(f"temp/files{directory}")
        files = sort_dir_files(os_listdir(f"temp/files{directory}"))
        if "hidden" in files:
            if not is_root_user(request, auth_psw):
                return "<li>Access denied</li>"
        elif "privilege" in files:
            if not is_privileged_user(request, auth_psw):
                return "<li>Access denied</li>"
        elif "viewer" in files:
            if not is_authorized_user(request, auth_psw):
                return f"""<li>Access denied</li> <a href="/auth?redirect=files{directory}" 
                            title="Authorization">Login or register</a>"""
        for i in files:
            if i == "hidden" or i == "init" or i == "viewer" or i == "privilege" or (".meta" in i):
                continue
            if len(i.split(".")) == 1:
                if os_path.isdir(f"temp/files{directory}/{i}"):
                    file_class = "folder"
                else:
                    file_class = "file"
            else:
                if os_path.isdir(f"temp/files{directory}/{i}"):
                    file_class = "folder"
                else:
                    file_type = i.split(".")
                    file_type = file_type[len(file_type) - 1]
                    if file_type.lower() in ["png", "jpg", "bmp", "gif", "heic", "svg", "psd", "tif", "tiff", "ico"]:
                        file_class = "image"
                    else:
                        file_class = "file"
            local_files += f"""<li id="{i}">
                <a href="/files{directory}/{i}" title="{i}" 
                class="{file_class}">{i}</a></li>"""
        return local_files
    except FileNotFoundError:
        return HTMLResponse(status_code=404)


def tree_view(folder, html, _path, i):
    link = os_path.abspath(folder).replace("\\", "/").split("temp/files")[1]
    folder_name = ["", "files"] if link == "" else link.split("/")
    href = f"""<a href='javascript:replace("{_path}", "/files{link}");' 
            class="text">{folder_name[len(folder_name) - 1]}</a>"""
    details = " open" if folder_name[1] == "files" else ""
    html += f"""<div>{href}<details{details}><summary></summary>"""
    for file in os_listdir(folder):
        i = 0
        path = os_path.join(folder, file)
        if os_path.isdir(path):
            i += 1
            html = tree_view(path, html, _path, 0)
    html += "</details></div>"
    return html


def get_folder_access_level(path: str):
    try:
        files = os_listdir(f"temp/{path}")
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
    icons += f"""<h1><i><a href="/admin?arg=files{upload_path}" title="Admin panel">
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
        with open("app/templates/menu.html", "r") as data:
            menu += data.read().format(index_of.replace("root", "files"))
    else:
        menu += """<input type="hidden" id="new_name" name="new_name" size="27"></form></ul>
                <script src="/source/context.js"></script>"""
    return menu


def delete_full_file(path: str):
    remove(f"temp/{path}")
    try:
        remove(f"temp/{path}.meta")
    except FileNotFoundError:
        pass


def check_cookies(request: Request, cookie: str, db: Session):
    try:
        permissions = crud.get_permissions(get_jwt_sub(request, cookie).split("://:")[1], db)
        if permissions == 5:
            return "Administrator"
        elif permissions is None:
            return "Revoke"
        else:
            return "Authorized user"
    except AttributeError:
        return "Unauthorized"


def get_jwt_sub(request: Request, cookie: str):
    request.headers.__dict__["_list"]\
        .append(("authorization".encode(), f"Bearer {cookie}".encode()))
    authorize = AuthJWT(request)
    try:
        return authorize.get_jwt_subject()
    except Exception as e:
        if str(e) == "":
            return None
        else:
            error_log(str(e))
            return None
