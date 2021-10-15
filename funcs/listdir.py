import os

from fastapi import Request
from fastapi.responses import HTMLResponse

from funcs.utils import is_root_user, is_authorized_user


def listdir(directory: str, request: Request, auth_psw):
    local_files = ""
    try:
        files = sorted(os.listdir(f"temp/files{directory}"))
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
            name = i
            if file_class == "file":
                file_extension = i.split(".")
                if file_extension[len(file_extension) - 1] == "pdf":
                    i += "?download=true"
            local_files += f"""<li>
                <a href="/files{directory}/{i}" title="/files{directory}/{i}" 
                class="{file_class}">{name}</a></li>"""
        return local_files
    except FileNotFoundError:
        return HTMLResponse(status_code=404)
