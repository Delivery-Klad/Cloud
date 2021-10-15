import os

import bcrypt
from fastapi import APIRouter, Cookie
from fastapi.responses import RedirectResponse
from typing import Optional

from funcs.pages import show_forbidden_page

router = APIRouter(prefix="/config")


@router.get("/")
async def folder_settings(path: str, arg: str, access: str, auth_psw: Optional[str] = Cookie(None)):
    try:
        if not bcrypt.checkpw(os.environ.get("root_psw").encode("utf-8"), auth_psw.encode("utf-8")):
            return show_forbidden_page()
        new_path = path.split("/")[:-1]
        new_path = "/".join(new_path) + f"/{arg}"
        os.rename(f"temp/{path}", f"temp/{new_path}")
        files = os.listdir(f"temp/{new_path}")
        if "hidden" in files:
            os.remove(f"temp/{new_path}/hidden")
        elif "viewer" in files:
            os.remove(f"temp/{new_path}/viewer")
        elif "init" in files:
            os.remove(f"temp/{new_path}/init")
        if access == "root":
            with open(f"temp/{new_path}/hidden", "w") as hidden:
                hidden.write("init")
        elif access == "auth":
            with open(f"temp/{new_path}/viewer", "w") as viewer:
                viewer.write("init")
        else:
            with open(f"temp/{new_path}/init", "w") as init:
                init.write("init")
        return RedirectResponse(f"/{new_path}", status_code=302)
    except AttributeError:
        return show_forbidden_page()
    except Exception as er:
        print(er)
