from os import environ
from shutil import make_archive

from dropbox import Dropbox
from dropbox.exceptions import AuthError
from fastapi import APIRouter, Cookie, Response, Request
from git import Repo
from typing import Optional

from funcs.database import get_users, set_permissions, delete_user
from funcs.utils import is_root_user, log, error_log, check_cookies, clear_log

router = APIRouter(prefix="/admin")
dbx_token = environ.get("dbx_token")


@router.get("/dashboard")
async def admin_dashboard(request: Request, arg: bool = False, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/dashboard' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
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
                                f"Current session starts in:   {environ.get('start_time')}",
                                f"Untracked files count:       {len(result) - 1}",
                                f"Backup archives count:       {backups}"]}
            else:
                return {"res": result}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.get("/logs")
async def admin_logs(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/logs' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            with open("log.txt", "r") as log_file:
                result = log_file.read()
            return {"res": result.split("\n")}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.delete("/clear_logs")
async def admin_clear_logs(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"DELETE Request to '/admin/clear_logs' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            clear_log("log.txt")
            with open("log.txt", "r") as log_file:
                result = log_file.read()
            return {"res": result.split("\n")}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.get("/errors")
async def admin_errors(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/errors' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            with open("error_log.txt", "r") as log_file:
                result = log_file.read()
            return {"res": result.split("\n")}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.delete("/clear_errors")
async def admin_clear_errors(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"DELETE Request to '/admin/clear_errors' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            clear_log("error_log.txt")
            with open("error_log.txt", "r") as log_file:
                result = log_file.read()
            return {"res": result.split("\n")}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.delete("/user/{user}")
async def admin_delete_user(user: int, request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"DELETE Request to '/admin/user' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            delete_user(user)
            return {"res": "Success"}
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))


@router.get("/users")
async def admin_users(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/users' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
    result = ["Users"]
    try:
        if is_root_user(request, auth_psw):
            for i in get_users():
                result.append([i[0], i[1], "Password hash", i[3], i[4]])
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))
    return {"res": result}


@router.patch("/permissions")
async def admin_permissions(request: Request, up: bool, user: int, auth_psw: Optional[str] = Cookie(None)):
    log(f"PATCH Request to '/admin/users' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            return set_permissions(user, up)
        else:
            return "fck u"
    except Exception as e:
        return error_log(str(e))


@router.post("/")
async def admin_push_files(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"POST Request to '/admin/push_files' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
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
                return Response(content="There is no files to push!", status_code=200)
        except Exception as e:
            error_log(str(e))
            print("Creating archive!")
            dbx = Dropbox(dbx_token)
            make_archive("backup_archive", "zip", "temp/files/7 сем")
            import random
            with open("backup_archive.zip", "rb") as archive:
                print("Upload archive!")
                dbx.files_upload(archive.read(), f"/backup{random.randint(1, 1000)}.zip")
            print("Archive uploaded!")
        return Response(content="Push files complete!", status_code=200)
    else:
        return Response(content="Unauthorized", status_code=403)
