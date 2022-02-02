from os import rename, listdir, remove
from shutil import rmtree, move

from sqlalchemy.orm import Session
from fastapi import APIRouter, Cookie, Request, Depends
from typing import Optional

from app.database import schemas
from app.funcs.pages import show_forbidden_page
from app.funcs.utils import is_root_user, log, error_log, check_cookies, create_new_folder, get_folder_access_level, \
    delete_full_file
from app.dependencies import get_db

router = APIRouter(prefix="/folder")


@router.get("/{catchall:path}")
async def get_access(request: Request,
                     db: Session = Depends(get_db),
                     auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/folder' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if not is_root_user(request, auth_psw):
            return {"res": False}
        path = request.path_params["catchall"]
        return get_folder_access_level(path)
    except NotADirectoryError:
        return {"res": False}
    except AttributeError:
        return {"res": False}
    except FileNotFoundError:
        return {"res": False}


@router.post("/")
async def create_folder(data: schemas.Folder, request: Request,
                        db: Session = Depends(get_db),
                        auth_psw: Optional[str] = Cookie(None)):
    log(f"POST Request to '/folder' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
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
async def config_folder(request: Request, data: schemas.Folder,
                        auth_psw: Optional[str] = Cookie(None)):
    try:
        if not is_root_user(request, auth_psw):
            return {"res": False}
        new_path = data.path.split("/")[:-1]
        new_path = "/".join(new_path) + f"/{data.arg}"
        rename(f"temp/{data.path}", f"temp/{new_path}")
        files = listdir(f"temp/{new_path}")
        if "hidden" in files:
            remove(f"temp/{new_path}/hidden")
        elif "viewer" in files:
            remove(f"temp/{new_path}/viewer")
        elif "privilege" in files:
            remove(f"temp/{new_path}/privilege")
        elif "init" in files:
            remove(f"temp/{new_path}/init")
        file_name = ""
        if data.access == "root":
            file_name = "hidden"
        elif data.access == "auth":
            file_name = "viewer"
        elif data.access == "privilege":
            file_name = "privilege"
        else:
            file_name = "init"
        with open(f"temp/{new_path}/{file_name}", "w") as access_file:
            access_file.write("init")
        return {"res": True}
    except AttributeError:
        return {"res": False}
    except Exception as er:
        return error_log(str(er))


@router.put("/")
async def replace_folder(request: Request, data: schemas.ReplaceFolder,
                         db: Session = Depends(get_db),
                         auth_psw: Optional[str] = Cookie(None)):
    log(f"PUT Request to '/folder/' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        try:
            if not is_root_user(request, auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        move(f"temp{data.old_path}", f"temp{data.new_path}")
        return {"res": True}
    except Exception as er:
        return error_log(str(er))


@router.delete("/")
async def delete_folder(data: schemas.DeleteFolder, request: Request,
                        auth_psw: Optional[str] = Cookie(None)):
    try:
        if not is_root_user(request, auth_psw):
            return {"res": False}
        rmtree(f"temp{data.file_path}")
        return {"res": True}
    except NotADirectoryError:
        delete_full_file(data.file_path)
        return {"res": True}
    except AttributeError:
        return {"res": False}
    except Exception as er:
        return error_log(str(er))
