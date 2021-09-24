import os

from fastapi import FastAPI, File, UploadFile, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer
from starlette.responses import FileResponse
from typing import Optional

app = FastAPI()
security = HTTPBearer()
clients = []
root_key = "root"
token = "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"
url = "https://c1oud.herokuapp.com/"
with open("scripts/style.css", "r") as file:
    style = file.read()


def listdir(directory: str, request: Request):
    local_files = ""
    try:
        files = sorted(os.listdir(f'temp/files{directory}'))
        if "hidden" in files:
            if request.client.host not in clients:
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
                            <h1><i><a href="{url}auth"><img src="https://i.ibb.co/tpQDd1P/pngegg.png" width="30" 
                            height="25" alt="Пример"></a></i></h1>
                            <h1><i><a href="{url}upload?arg=files{upload_path}">
                            <img src="https://i.ibb.co/Sm35j4B/upload.png" width="30" 
                            height="25" alt="Пример"></a></i></h1></header>
                        <ul id="files">{files}</ul>
                        </main></body></html>"""
    return HTMLResponse(content=html_content, status_code=200)


def handler(path: str, filename: str, request: Request):
    try:
        files = listdir(path, request)
        if type(files) != str:
            with open("404.html", "r") as page:
                return HTMLResponse(content=page.read(), status_code=404)
        index_of = "root" if path == "" else f"root{path}"
        return builder(index_of, files)
    except NotADirectoryError:
        if filename.split(".")[1] == "html":
            with open(f"temp/files{path}", "r") as page:
                return HTMLResponse(content=page.read(), status_code=200)
        return FileResponse(path=f"temp/files{path}", filename=filename, media_type='application/octet-stream')


def show_auth_page():
    with open("templates/auth.html", "r") as page:
        return HTMLResponse(content=page.read(), status_code=200)


def show_forbidden_page():
    with open("templates/403.html", "r") as page:
        return HTMLResponse(content=page.read(), status_code=403)


@app.get("/")
async def homepage():
    return RedirectResponse(url + "files")


@app.get("/{path}")
async def other_page(path: str, request: Request, arg: Optional[str] = None):
    if path == "files":
        return handler("", "", request)
    elif path == "auth":
        if arg is None:
            return show_auth_page()
        else:
            if arg == root_key:
                clients.append(request.client.host)
                return RedirectResponse("files")
            return show_forbidden_page()
    elif path == "upload":
        if request.client.host not in clients:
            return show_auth_page()
        else:
            with open("templates/upload.html", "r") as page:
                return HTMLResponse(content=page.read().format(arg), status_code=200)
    with open("404.html", "r") as page:
        return HTMLResponse(content=page.read(), status_code=404)


@app.post("/upload/")
async def upload_file(request: Request, path: Optional[str] = Query(None), data: UploadFile = File(...)):
    try:
        if request.client.host not in clients:
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
async def read_index(request: Request):
    path = request.path_params["catchall"]
    name = path.split("/")
    return handler(f"/{path}", name[len(name) - 1], request)


@app.on_event("startup")
def create_files():
    try:
        os.mkdir("temp")
        from git.repo.base import Repo
        Repo.clone_from(f"https://{token}:x-oauth-basic@github.com/Delivery-Klad/files_folder", "temp")
    except FileExistsError:
        pass
