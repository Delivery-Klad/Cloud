import os
import bcrypt

from fastapi import Request
from fastapi.responses import HTMLResponse


def listdir(directory: str, request: Request, auth_psw):
    local_files = ""
    try:
        files = sorted(os.listdir(f"temp/files{directory}"))
        if "hidden" in files:
            try:
                if not bcrypt.checkpw(os.environ.get("root_psw").encode("utf-8"), auth_psw.encode("utf-8")):
                    return "<li>Access denied</li>"
            except AttributeError:
                return "<li>Access denied</li>"
        elif "viewer" in files:
            try:
                if not bcrypt.checkpw(os.environ.get("root_psw").encode("utf-8"), auth_psw.encode("utf-8")) and not \
                        bcrypt.checkpw(os.environ.get("viewer_key").encode("utf-8"), auth_psw.encode("utf-8")):
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
