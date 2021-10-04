import os
import time

from fastapi import FastAPI, File, UploadFile, Request, Query, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer
from starlette.responses import FileResponse
from typing import Optional
import mammoth

app = FastAPI()
security = HTTPBearer()
max_retries = 10
root_key = os.environ.get("root_psw")
viewer_key = os.environ.get("viewer_key")
token = "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"
url = "https://c1oud.herokuapp.com/"
# url = "http://localhost:8000/"
with open("source/style.css", "r") as file:
    style = file.read()


def listdir(directory: str, request: Request, auth_psw):
    local_files = ""
    try:
        files = sorted(os.listdir(f"temp/files{directory}"))
        print("hidden" in files)
        print(auth_psw)
        if "hidden" in files:
            with open(f"temp/files{directory}/hidden", "r") as hidden:
                if hidden.read() == "root only":
                    print(1)
                    if auth_psw != root_key:
                        return "<li>Access denied</li>"
                else:
                    print(2)
                    print(root_key)
                    print(viewer_key)
                    if auth_psw != root_key and auth_psw != viewer_key:
                        return "<li>Access denied</li>"
        for i in files:
            if i == "hidden":
                continue
            file_class = "folder" if len(i.split(".")) == 1 else "file"
            local_files += f"""<li>
                <a href="/files{directory}/{i}" title="/files{directory}/{i}" 
                class="{file_class}">{i}</a></li>"""
        return local_files
    except FileNotFoundError:
        return HTMLResponse(status_code=404)


def builder(index_of: str, files: str):
    upload_path = "/" if index_of.split("root")[1] == "" else index_of.split("root")[1]
    html_content = f"""<html>
                        <head>
                            <meta name="viewport" content="width=device-width,initial-scale=1">
                            <title>{"Cloud"}</title>{style}
                        </head>
                        <body><main>
                            <header><h1><i>Index of /{index_of}</i></h1>
                            <h1><i><a href="{url}auth"><img src="{url + "source/lock.svg"}" width="30" 
                            height="25" alt="auth"></a></i></h1>
                            <h1><i><a href="{url}upload?arg=files{upload_path}">
                            <img src="{url + "source/upload.svg"}" width="30" 
                            height="25" alt="upload"></a></i></h1></header>
                        <ul id="files">{files}</ul>
                        </main></body></html>"""
    return HTMLResponse(content=html_content, status_code=200)


def handler(path: str, filename: str, request: Request, auth_psw, download):
    try:
        files = listdir(path, request, auth_psw)
        if type(files) != str:
            if path == "":
                time.sleep(4)
                files = listdir(path, request, auth_psw)
                if type(files) != str:
                    time.sleep(3)
                    files = listdir(path, request, auth_psw)
            else:
                return show_not_found_page()
        index_of = "root" if path == "" else f"root{path}"
        return builder(index_of, files)
    except NotADirectoryError:
        file_extension = filename.split(".")[len(filename.split(".")) - 1]
        print(file_extension)
        if not download:
            if file_extension == "html" or file_extension == "txt":
                with open(f"temp/files{path}", "r") as page:
                    return HTMLResponse(content=page.read(), status_code=200)
            elif file_extension == "docx":
                with open(f"temp/files{path}", "rb") as page:
                    res = mammoth.convert_to_html(page)
                    html_page = f"""<head><title>{filename}</title></head>
                    <form>
                    <input type="button" value="Download" onClick='location.href="{url}files{path}?download=true"'>
                    </form>
                    """
                    return HTMLResponse(content=html_page + res.value, status_code=200)
        return FileResponse(path=f"temp/files{path}", filename=filename, media_type='application/octet-stream')


def show_auth_page():
    with open("templates/auth.html", "r") as page:
        return HTMLResponse(content=page.read(), status_code=200)


def show_forbidden_page():
    with open("templates/403.html", "r") as page:
        return HTMLResponse(content=page.read(), status_code=403)


def show_not_found_page():
    with open("templates/404.html", "r") as page:
        return HTMLResponse(content=page.read(), status_code=404)


@app.get("/")
async def homepage():
    return RedirectResponse(url + "files")


@app.get("/{path}")
async def other_page(path: str, request: Request, arg: Optional[str] = None, auth_psw: Optional[str] = Cookie(None),
                     download: Optional[bool] = None):
    if path == "files":
        return handler("", "", request, auth_psw, download)
    elif path == "auth":
        if arg is None:
            return show_auth_page()
        else:
            if arg == root_key or arg == viewer_key:
                response = RedirectResponse("files")
                response.set_cookie(key="auth_psw", value=arg)
                return response
            return show_forbidden_page()
    elif path == "upload":
        if auth_psw != root_key:
            return show_auth_page()
        else:
            with open("templates/upload.html", "r") as page:
                return HTMLResponse(content=page.read().format(arg), status_code=200)
    return show_not_found_page()


@app.post("/upload/")
async def upload_file(request: Request, path: Optional[str] = Query(None), data: UploadFile = File(...),
                      auth_psw: Optional[str] = Cookie(None)):
    try:
        if auth_psw != root_key:
            return show_forbidden_page()
        with open(f"temp/{path}/{data.filename}", "wb") as uploaded_file:
            uploaded_file.write(await data.read())
        from git import Repo
        repo = Repo("temp/.git")
        repo.git.add(f"{path}/{data.filename}")
        repo.index.commit("commit from cloud")
        origin = repo.remote(name='origin')
        origin.push()
        return RedirectResponse(f"{url}{path}", status_code=302)
    except Exception as er:
        print(er)


@app.get("/files/{catchall:path}")
async def get_files(request: Request, auth_psw: Optional[str] = Cookie(None), download: Optional[bool] = None):
    path = request.path_params["catchall"]
    name = path.split("/")
    return handler(f"/{path}", name[len(name) - 1], request, auth_psw, download)


@app.get("/source/{name}")
async def get_source(name: str, request: Request):
    try:
        return FileResponse(f"source/{name}")
    except FileNotFoundError:
        show_not_found_page()


@app.on_event("startup")
async def clone_remote_repo():
    try:
        os.mkdir("temp")
        from git.repo.base import Repo
        Repo.clone_from(f"https://{token}:x-oauth-basic@github.com/Delivery-Klad/files_folder", "temp")
    except FileExistsError:
        pass
