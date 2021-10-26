import os
import time

import bcrypt
from fastapi import Request
from fastapi.responses import RedirectResponse, HTMLResponse


def is_root_user(password: str):
    return bcrypt.checkpw(os.environ.get("root_psw").encode("utf-8"), password.encode("utf-8"))


def is_authorized_user(password: str):
    return bcrypt.checkpw(os.environ.get("viewer_key").encode("utf-8"), password.encode("utf-8")) or \
           bcrypt.checkpw(os.environ.get("root_psw").encode("utf-8"), password.encode("utf-8"))


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
        print(os.environ.get("last_folder") not in os.listdir(f"temp/files{directory}"))
        print("Other" not in os.listdir(f"temp/files{directory}"))
        if os.environ.get("last_folder") not in os.listdir(f"temp/files{directory}") or "Other" not in \
                os.listdir(f"temp/files{directory}"):
            time.sleep(2)
        files = sorted(os.listdir(f"temp/files{directory}"),
                       key=lambda x: int(x.split(".")[0]) if x.split(".")[0].isdigit() else 0)
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
            if i == "hidden" or i == "init" or i == "viewer":
                continue
            file_class = "folder" if len(i.split(".")) == 1 else "file"
            local_files += f"""<li>
                <a href="/files{directory}/{i}" title="/files{directory}/{i}" 
                class="{file_class}">{i}</a></li>"""
        return local_files
    except FileNotFoundError:
        return HTMLResponse(status_code=404)
