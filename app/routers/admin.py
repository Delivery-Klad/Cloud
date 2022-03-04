from os import environ
from shutil import make_archive
from datetime import datetime

from sqlalchemy.orm import Session
from dropbox import Dropbox
from dropbox.exceptions import AuthError
from fastapi import APIRouter, Cookie, Response, Request, Depends
from git import Repo
from typing import Optional

from app.database import crud, schemas
from app.funcs.utils import is_root_user, log, error_log, check_cookies, \
    clear_log
from app.dependencies import get_db, get_settings

settings = get_settings()
router = APIRouter(prefix="/admin")
dbx_token = settings.dbx_token


@router.get("/dashboard")
async def admin_dashboard(request: Request, arg: bool = False,
                          db: Session = Depends(get_db),
                          auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/dashboard' from '{request.client.host}' "
        f"with cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if is_root_user(request, auth_psw):
            result = ["Untracked files"]
            repo = Repo("temp/.git")
            for item in repo.untracked_files:
                result.append(item)
            for item in repo.index.diff(None):
                result.append(item.a_path)
            if not arg:
                try:
                    dbx = Dropbox(dbx_token)
                    backups = len(dbx.files_list_folder(path='').entries)
                except AuthError:
                    backups = "Not found"
                return {"res": [f"Summary",
                                f"Current session starts in:   "
                                f"{environ.get('start_time')}",
                                f"Untracked files count:       "
                                f"{len(result) - 1}",
                                f"Backup archives count:       {backups}"]}
            else:
                return {"res": result}
        else:
            return {"res": "Failed"}
    except Exception as e:
        print(e)


@router.get("/logs")
async def admin_logs(request: Request, db: Session = Depends(get_db),
                     auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/logs' from '{request.client.host}' "
        f"with cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if is_root_user(request, auth_psw):
            with open("log.txt", "r") as file:
                return {"res": file.read().split("\n")}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.delete("/clear_logs")
async def admin_clear_logs(request: Request,
                           db: Session = Depends(get_db),
                           auth_psw: Optional[str] = Cookie(None)):
    try:
        if is_root_user(request, auth_psw):
            clear_log("log.txt")
            return {"res": [f"Log cleared {str(datetime.utcnow())[:-7]}"]}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.get("/errors")
async def admin_errors(request: Request,
                       db: Session = Depends(get_db),
                       auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/errors' from '{request.client.host}' "
        f"with cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if is_root_user(request, auth_psw):
            with open("error_log.txt", "r") as file:
                return {"res": file.read().split("\n")}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.delete("/clear_errors")
async def admin_clear_errors(request: Request,
                             db: Session = Depends(get_db),
                             auth_psw: Optional[str] = Cookie(None)):
    try:
        if is_root_user(request, auth_psw):
            clear_log("error_log.txt")
            return {"res": [f"Log cleared {str(datetime.utcnow())[:-7]}"]}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.delete("/user/{user}")
async def admin_delete_user(user: int, request: Request,
                            db: Session = Depends(get_db),
                            auth_psw: Optional[str] = Cookie(None)):
    log(f"DELETE Request to '/admin/user' from '{request.client.host}' "
        f"with cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if is_root_user(request, auth_psw):
            crud.delete_user(user, db)
            return {"res": "Success"}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.get("/users")
async def admin_users(request: Request,
                      db: Session = Depends(get_db),
                      auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/users' from '{request.client.host}' "
        f"with cookies '{check_cookies(request, auth_psw, db)}'")
    result = ["Users"]
    try:
        if is_root_user(request, auth_psw):
            for i in crud.get_users(db):
                result.append([i.id, i.login, "Password hash", i.useragent, i.permissions])
            return {"res": result}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.patch("/permissions")
async def admin_permissions(request: Request, data: schemas.UserPermissions,
                            db: Session = Depends(get_db),
                            auth_psw: Optional[str] = Cookie(None)):
    log(f"PATCH Request to '/admin/users' from '{request.client.host}' "
        f"with cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if is_root_user(request, auth_psw):
            return crud.set_permissions(data.user, data.up, db)
        else:
            return "fck u"
    except Exception as e:
        return error_log(str(e))


@router.post("/")
async def admin_push_files(request: Request, db: Session = Depends(get_db),
                           auth_psw: Optional[str] = Cookie(None)):
    log(f"POST Request to '/admin/push_files' from '{request.client.host}' "
        f"with cookies '{check_cookies(request, auth_psw, db)}'")
    if is_root_user(request, auth_psw):
        print("Starting push files process...")
        try:
            result = []
            repo = Repo("temp/.git")
            for item in repo.untracked_files:
                result.append(item)
            for item in repo.index.diff(None):
                result.append(item)
            if result:
                print("Untracked files detected...")
                repo.git.add(all=True)
                repo.index.commit("commit from cloud")
                origin = repo.remote(name='origin')
                origin.push()
                print("Push success!")
            else:
                print("There is no files to push!")
                return Response(content="There is no files to push!",
                                status_code=200)
        except Exception as e:
            error_log(str(e))
            print("Creating archive!")
            dbx = Dropbox(dbx_token)
            make_archive("backup_archive", "zip", "temp/files/7 сем")
            import random
            with open("backup_archive.zip", "rb") as archive:
                print("Upload archive!")
                dbx.files_upload(archive.read(),
                                 f"/backup{random.randint(1, 1000)}.zip")
            print("Archive uploaded!")
        return Response(content="Push files complete!", status_code=200)
    else:
        return Response(content="Unauthorized", status_code=403)
