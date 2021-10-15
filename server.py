import os

import bcrypt
from fastapi import FastAPI, File, UploadFile, Request, Query, Cookie
from fastapi.responses import RedirectResponse
from git import Repo

from funcs.builder import handler
from funcs.pages import *
from funcs.utils import create_new_folder
from routers import source, delete, config, add_text

app = FastAPI()
app.include_router(source.router)
app.include_router(delete.router)
app.include_router(config.router)
app.include_router(add_text.router)
root_key = os.environ.get("root_psw")
viewer_key = os.environ.get("viewer_key")
token = "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"
url = os.environ.get("server_url")
with open("source/style.css", "r") as file:
    style = file.read()
with open("source/context.js", "r") as context:
    context_script = context.read()


@app.get("/")
async def homepage():
    return RedirectResponse(url + "files")


@app.post("/upload_file/")
async def upload_file(path: Optional[str] = Query(None), data: UploadFile = File(...),
                      auth_psw: Optional[str] = Cookie(None)):
    try:
        try:
            if not bcrypt.checkpw(root_key.encode("utf-8"), auth_psw.encode("utf-8")):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        with open(f"temp/{path}/{data.filename}", "wb") as uploaded_file:
            uploaded_file.write(await data.read())
        return RedirectResponse(f"/{path}", status_code=302)
    except Exception as er:
        print(er)


@app.get("/new_folder")
async def create_folder(path: str, arg: str, access: str, auth_psw: Optional[str] = Cookie(None)):
    try:
        try:
            if not bcrypt.checkpw(root_key.encode("utf-8"), auth_psw.encode("utf-8")):
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
        return handler("", "", request, auth_psw, download, context_script, style)
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
            if not bcrypt.checkpw(root_key.encode("utf-8"), auth_psw.encode("utf-8")):
                return show_forbidden_page()
            else:
                return show_upload_page(arg)
        except AttributeError:
            return show_forbidden_page()
    elif path == "create":
        try:
            if not bcrypt.checkpw(root_key.encode("utf-8"), auth_psw.encode("utf-8")):
                return show_forbidden_page()
            else:
                return show_create_page(arg, "Create folder", "new_folder", "", "checked", "", "")
        except AttributeError:
            return show_forbidden_page()
    elif path == "settings":
        try:
            if not bcrypt.checkpw(root_key.encode("utf-8"), auth_psw.encode("utf-8")):
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
                elif "init" in files:
                    all_users = "checked"
                return show_create_page(arg, "Folder settings", "config", name, root, auth, all_users)
        except AttributeError:
            return show_forbidden_page()
    return show_not_found_page()


@app.get("/files/{catchall:path}")
async def get_files(request: Request, auth_psw: Optional[str] = Cookie(None), download: Optional[bool] = None):
    path = request.path_params["catchall"]
    name = path.split("/")
    return handler(f"/{path}", name[len(name) - 1], request, auth_psw, download, context_script, style)


@app.on_event("startup")
async def startup():
    try:
        os.mkdir("temp")
        from git.repo.base import Repo
        Repo.clone_from(f"https://{token}:x-oauth-basic@github.com/Delivery-Klad/files_folder", "temp")
    except FileExistsError:
        pass


@app.on_event("shutdown")
async def shutdown():
    result = []
    repo = Repo("temp/.git")
    for item in repo.untracked_files:
        result.append(item)
    for item in repo.index.diff(None):
        result.append(item)
    if result:
        print("Untracked files detected!")
        repo.git.add(all=True)
        repo.index.commit("commit from cloud")
        origin = repo.remote(name='origin')
        origin.push()
        print("Push success!")
    print("Shutdown...")
