import os
import time
import shutil

import bcrypt
import dropbox
from fastapi import FastAPI, Request, Cookie
from fastapi.responses import RedirectResponse
from git import Repo

from funcs.builder import handler
from funcs.content_length import LimitUploadSize
from funcs.pages import *
from funcs.utils import create_new_folder, is_root_user
from routers import source, delete, config, add_text, upload, admin


app = FastAPI()
ready = False
app.include_router(admin.router)
app.include_router(source.router)
app.include_router(delete.router)
app.include_router(config.router)
app.include_router(add_text.router)
app.include_router(upload.router)
app.add_middleware(LimitUploadSize, max_upload_size=50_000_000)
root_key = os.environ.get("root_psw")
viewer_key = os.environ.get("viewer_key")
token = "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"
dbx_token = "vuMWKf0zPEgAAAAAAAAAAe4Uhy9mh-hSArGSGdU5w7AyUvFE7TKwNzX6h_dpDP4r"
url = os.environ.get("server_url")
with open("source/style.css", "r") as file:
    style = file.read()
with open("source/context.js", "r") as context:
    context_script = context.read()


@app.get("/")
async def homepage():
    return RedirectResponse(url + "files")


@app.get("/new_folder")
async def create_folder(path: str, arg: str, access: str, auth_psw: Optional[str] = Cookie(None)):
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
    if path == "files":
        print(ready)
        if not ready:
            while not ready:
                time.sleep(1)
        return handler("", "", request, auth_psw, download, context_script, style)
    elif path == "auth":
        print(arg)
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
            return show_admin_index()
        else:
            return show_auth_page("admin")
    return show_not_found_page()


@app.get("/files/{catchall:path}")
async def get_files(request: Request, auth_psw: Optional[str] = Cookie(None), download: Optional[bool] = None):
    path = request.path_params["catchall"]
    name = path.split("/")
    print(ready)
    if not ready:
        while not ready:
            time.sleep(1)
    return handler(f"/{path}", name[len(name) - 1], request, auth_psw, download, context_script, style)


@app.on_event("startup")
def startup():
    global ready
    print("Starting startup process...")
    try:
        print("Cloning repo...")
        os.mkdir("temp")
        from git.repo.base import Repo
        Repo.clone_from(f"https://{token}:x-oauth-basic@github.com/Delivery-Klad/files", "temp")
        print("Cloning success!")
        ready = True
    except FileExistsError:
        ready = True
    print("Startup complete!")


@app.on_event("shutdown")
def shutdown():
    print("Starting shutdown process...")
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
    except Exception as e:
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
