import os
import shutil
from datetime import datetime

import dropbox
from fastapi import APIRouter, Cookie, Response, Request
from git import Repo
from typing import Optional

from funcs.utils import is_root_user, log, error_log, check_cookies, clear_log

router = APIRouter(prefix="/admin")
dbx_token = "vuMWKf0zPEgAAAAAAAAAAe4Uhy9mh-hSArGSGdU5w7AyUvFE7TKwNzX6h_dpDP4r"


@router.get("/dashboard")
async def admin_dashboard(request: Request, arg: bool = False, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/dashboard' from '{request.client.host}' with cookies '{check_cookies(auth_psw)}'")
    try:
        if is_root_user(auth_psw):
            result = ["Untracked files"]
            repo = Repo("temp/.git")
            for item in repo.untracked_files:
                result.append(item)
            for item in repo.index.diff(None):
                result.append(item.a_path)
            if not arg:
                dbx = dropbox.Dropbox(dbx_token)
                return {"res": [f"Summary",
                                f"Current session starts in:   {os.environ.get('start_time')}",
                                f"Untracked files count:       {len(result) - 1}",
                                f"Backup archives count:       {len(dbx.files_list_folder(path='').entries)}"]}
            else:
                return {"res": result}
        else:
            return {"res": "Failed"}
    except Exception as e:
        error_log(str(e))


@router.get("/logs")
async def admin_logs(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/logs' from '{request.client.host}' with cookies '{check_cookies(auth_psw)}'")
    try:
        if is_root_user(auth_psw):
            with open("log.txt", "r") as log_file:
                result = log_file.read()
            return {"res": result.split("\n")}
        else:
            return {"res": "Failed"}
    except Exception as e:
        error_log(str(e))


@router.get("/clear_logs")
async def admin_clear_logs(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/clear_logs' from '{request.client.host}' with cookies '{check_cookies(auth_psw)}'")
    try:
        if is_root_user(auth_psw):
            pass
        else:
            return {"res": "Failed"}
    except Exception as e:
        error_log(str(e))


@router.get("/errors")
async def admin_errors(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/errors' from '{request.client.host}' with cookies '{check_cookies(auth_psw)}'")
    try:
        if is_root_user(auth_psw):
            clear_log("log.txt")
        else:
            return {"res": "Failed"}
    except Exception as e:
        error_log(str(e))


@router.get("/clear_errors")
async def admin_clear_errors(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/clear_errors' from '{request.client.host}' with cookies '{check_cookies(auth_psw)}'")
    try:
        if is_root_user(auth_psw):
            clear_log("error_log.txt")
        else:
            return {"res": "Failed"}
    except Exception as e:
        error_log(str(e))


@router.get("/push_files")
async def admin_push_files(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/admin/push_files' from '{request.client.host}' with cookies '{check_cookies(auth_psw)}'")
    if is_root_user(auth_psw):
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
            dbx = dropbox.Dropbox(dbx_token)
            shutil.make_archive("aboba", "zip", "temp/files/7 сем")
            import random
            with open("aboba.zip", "rb") as archive:
                print("Upload archive!")
                dbx.files_upload(archive.read(), f"/backup{random.randint(1, 1000)}.zip")
            print("Archive uploaded!")
        return Response(content="Push files complete!", status_code=200)
    else:
        return Response(content="Unauthorized", status_code=403)
