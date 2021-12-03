import os

from fastapi import APIRouter, Cookie, Request
from typing import Optional
from pydantic import BaseModel

from funcs.utils import is_root_user, log, error_log, check_cookies, create_new_folder

router = APIRouter(prefix="/folder")


class Folder(BaseModel):
    path: str
    arg: str
    access: str


@router.post("/")
async def create_folder(data: Folder, request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"POST Request to '/folder' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
    try:
        try:
            if not is_root_user(auth_psw):
                return {"res": False}
        except AttributeError:
            return {"res": False}
        return create_new_folder(data.path, data.arg, data.access)
    except FileNotFoundError:
        return {"res": False}


@router.patch("/")
async def config_folder(data: Folder, auth_psw: Optional[str] = Cookie(None)):
    try:
        if not is_root_user(auth_psw):
            return {"res": False}
        new_path = data.path.split("/")[:-1]
        new_path = "/".join(new_path) + f"/{data.arg}"
        os.rename(f"temp/{data.path}", f"temp/{new_path}")
        files = os.listdir(f"temp/{new_path}")
        if "hidden" in files:
            os.remove(f"temp/{new_path}/hidden")
        elif "viewer" in files:
            os.remove(f"temp/{new_path}/viewer")
        elif "init" in files:
            os.remove(f"temp/{new_path}/init")
        if data.access == "root":
            with open(f"temp/{new_path}/hidden", "w") as hidden:
                hidden.write("init")
        elif data.access == "auth":
            with open(f"temp/{new_path}/viewer", "w") as viewer:
                viewer.write("init")
        else:
            with open(f"temp/{new_path}/init", "w") as init:
                init.write("init")
        return {"res": True}
    except AttributeError:
        return {"res": False}
    except Exception as er:
        error_log(str(er))
        return {"res": False}
