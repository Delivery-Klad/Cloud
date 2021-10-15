import os

import bcrypt
from fastapi.responses import RedirectResponse


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
