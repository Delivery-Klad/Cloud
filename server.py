import os
import time
import shutil
from datetime import datetime

import bcrypt
import dropbox
from fastapi import FastAPI, Request, Cookie
from fastapi.responses import RedirectResponse
from git import Repo

from funcs.builder import handler
from funcs.content_length import LimitUploadSize
from funcs.pages import *
from funcs.utils import create_new_folder, is_root_user, log, error_log
from routers import source, delete, config, upload, admin, files_info


app = FastAPI()
ready = False
app.include_router(admin.router)
app.include_router(source.router)
app.include_router(delete.router)
app.include_router(config.router)
app.include_router(upload.router)
app.include_router(files_info.router)
app.add_middleware(LimitUploadSize, max_upload_size=50_000_000)
root_key = os.environ.get("root_psw")
viewer_key = os.environ.get("viewer_key")
token = "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"
dbx_token = "vuMWKf0zPEgAAAAAAAAAAe4Uhy9mh-hSArGSGdU5w7AyUvFE7TKwNzX6h_dpDP4r"
url = os.environ.get("server_url")


@app.get("/")
async def homepage(request: Request):
    try:
        log(f"Request to '/' from '{request.client.host}'")
        return RedirectResponse(url + "files")
    except Exception as e:
        error_log(str(e))


@app.get("/new_folder")
async def create_folder(path: str, arg: str, access: str, request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"Request to '/new_folder' from '{request.client.host}'")
    try:
        try:
            if not is_root_user(auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        return create_new_folder(path, arg, access)
    except FileNotFoundError:
        show_not_found_page()


@app.get("/{path}")
async def other_page(path: str, request: Request, arg: Optional[str] = None, auth_psw: Optional[str] = Cookie(None),
                     download: Optional[bool] = None, redirect: Optional[str] = None, access: Optional[str] = None):
    log(f"Request to '{path}' from '{request.client.host}' with cookies '{auth_psw}'")
    try:
        if path == "files":
            if not ready:
                while not ready:
                    time.sleep(1)
            return handler("", "", request, auth_psw, download)
        elif path == "auth":
            if arg is None:
                return show_auth_page(redirect)
            else:
                if arg == root_key or arg == viewer_key:
                    if redirect is None:
                        response = RedirectResponse("files")
                    else:
                        response = RedirectResponse(redirect)
                    response.set_cookie(key="auth_psw", value=str(bcrypt.hashpw(arg.encode("utf-8"),
                                                                                bcrypt.gensalt()))[2:-1])
                    return response
                return show_forbidden_page()
        elif path == "upload":
            try:
                if not is_root_user(auth_psw):
                    return show_forbidden_page()
                else:
                    return show_upload_page(arg)
            except AttributeError:
                return show_forbidden_page()
        elif path == "create":
            try:
                if not is_root_user(auth_psw):
                    return show_forbidden_page()
                else:
                    return show_create_page(arg, "Create folder", "new_folder", "", "checked", "", "")
            except AttributeError:
                return show_forbidden_page()
        elif path == "settings":
            try:
                if not is_root_user(auth_psw):
                    return show_forbidden_page()
                else:
                    name = arg.split("/")
                    name = name[len(name) - 1]
                    files = os.listdir(f"temp/{arg}")
                    root, auth, all_users = "", "", ""
                    if "hidden" in files:
                        root = "checked"
                    elif "viewer" in files:
                        auth = "checked"
                    else:
                        all_users = "checked"
                    return show_create_page(arg, "Folder settings", "config", name, root, auth, all_users)
            except AttributeError:
                return show_forbidden_page()
        elif path == "admin":
            if is_root_user(auth_psw):
                content = ""
                temp = await admin.admin_dashboard(request, auth_psw=auth_psw)
                for i in temp['res']:
                    content += f"<div>{i}</div>"
                return show_admin_index(content)
            else:
                return show_auth_page("admin")
        return show_not_found_page()
    except Exception as e:
        error_log(str(e))


@app.get("/files/{catchall:path}")
async def get_files(request: Request, auth_psw: Optional[str] = Cookie(None), download: Optional[bool] = None):
    try:
        path = request.path_params["catchall"]
        log(f"Request to '{path}' from '{request.client.host}'")
        name = path.split("/")
        if not ready:
            while not ready:
                time.sleep(1)
        return handler(f"/{path}", name[len(name) - 1], request, auth_psw, download)
    except Exception as e:
        error_log(str(e))


@app.on_event("startup")
def startup():
    global ready
    try:
        with open("log.txt", "w") as log_file:
            log_file.write(f"Application startup")
        with open("error_log.txt", "w") as log_file:
            log_file.write(f"Application startup")
        os.environ["start_time"] = str(datetime.utcnow())[:-7]
        print("Starting startup process...")
        try:
            print("Cloning repo...")
            os.mkdir("temp")
            from git.repo.base import Repo
            Repo.clone_from(f"https://{token}:x-oauth-basic@github.com/Delivery-Klad/folder", "temp")
            print("Cloning success!")
            ready = True
        except FileExistsError:
            ready = True
        print("Startup complete!")
    except Exception as e:
        error_log(str(e))


@app.on_event("shutdown")
def shutdown():
    print("Starting shutdown process...")
    try:
        result = []
        repo = Repo("temp/.git")
        for item in repo.untracked_files:
            result.append(item)
        for item in repo.index.diff(None):
            result.append(item.a_path)
        if result:
            print("Untracked files detected...")
            repo.git.add(all=True)
            repo.index.commit("commit from cloud")
            origin = repo.remote(name='origin')
            origin.push()
            print("Push success!")
    except Exception as e:
        error_log(str(e))
        print(f"Error: {e}")
        print("Creating archive!")
        dbx = dropbox.Dropbox(dbx_token)
        shutil.make_archive("aboba", "zip", "temp/files/7 сем")
        import random
        with open("aboba.zip", "rb") as archive:
            print("Upload archive!")
            dbx.files_upload(archive.read(), f"/backup{random.randint(1, 1000)}.zip")
        print("Archive uploaded!")
    print("Shutdown complete!")
