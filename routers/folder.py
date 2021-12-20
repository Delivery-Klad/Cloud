import os
from shutil import rmtree

from fastapi import APIRouter, Cookie, Request
from typing import Optional
from pydantic import BaseModel

from funcs.utils import is_root_user, log, error_log, check_cookies, create_new_folder, get_folder_access_level

router = APIRouter(prefix="/folder")


class Folder(BaseModel):
    path: str
    arg: str
    access: str


class DeleteFolder(BaseModel):
    file_path: str


@router.get("/{catchall:path}")
async def get_access(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/folder' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
    try:
        if not is_root_user(request, auth_psw):
            return {"res": False}
        path = request.path_params["catchall"]
        return get_folder_access_level(path)
    except AttributeError:
        return {"res": False}
    except FileNotFoundError:
        return {"res": False}


@router.post("/")
async def create_folder(data: Folder, request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"POST Request to '/folder' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
    try:
        if not is_root_user(request, auth_psw):
            return {"res": False}
        return create_new_folder(data.path, data.arg, data.access)
    except AttributeError:
        return {"res": False}
    except FileNotFoundError:
        return {"res": False}
    except FileExistsError:
        return {"res": False}


@router.patch("/")
async def config_folder(request: Request, data: Folder, auth_psw: Optional[str] = Cookie(None)):
    try:
        if not is_root_user(request, auth_psw):
            return {"res": False}
        new_path = data.path.split("/")[:-1]
        new_path = "/".join(new_path) + f"/{data.arg}"
        os.rename(f"temp/{data.path}", f"temp/{new_path}")
        files = os.listdir(f"temp/{new_path}")
        if "hidden" in files:
            os.remove(f"temp/{new_path}/hidden")
        elif "viewer" in files:
            os.remove(f"temp/{new_path}/viewer")
        elif "privilege" in files:
            os.remove(f"temp/{new_path}/privilege")
        elif "init" in files:
            os.remove(f"temp/{new_path}/init")
        if data.access == "root":
            with open(f"temp/{new_path}/hidden", "w") as access_file:
                access_file.write("init")
        elif data.access == "auth":
            with open(f"temp/{new_path}/viewer", "w") as access_file:
                access_file.write("init")
        elif data.access == "privilege":
            with open(f"temp/{new_path}/privilege", "w") as access_file:
                access_file.write("init")
        else:
            with open(f"temp/{new_path}/init", "w") as access_file:
                access_file.write("init")
        return {"res": True}
    except AttributeError:
        return {"res": False}
    except Exception as er:
        return error_log(str(er))


@router.delete("/")
async def delete_folder(data: DeleteFolder, request: Request, auth_psw: Optional[str] = Cookie(None)):
    try:
        if not is_root_user(request, auth_psw):
            return {"res": False}
        rmtree(f"temp{data.file_path}")
        return
    except AttributeError:
        return {"res": False}
    except Exception as er:
        return error_log(str(er))