import os

from fastapi import FastAPI, File, UploadFile, Depends, Request, Security, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
security = HTTPBearer()
root_key = "root"
secret = "secret"
token = "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"
with open("Style/style.css", "r") as file:
    style = file.read()


class JWTSettings(BaseModel):
    authjwt_secret_key: str = secret


@AuthJWT.load_config
def get_config():
    return JWTSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


def listdir(directory: str):
    local_files = ""
    f"""<li><a href="/docs#/default/upload_file_upload__post" title="Add file" class="file"> + Add file</a></li>"""
    try:
        for i in os.listdir(f'files{directory}'):
            file_class = "folder" if len(i.split(".")) == 1 else "file"
            local_files += f"""<li>
                <a href="/files{directory}/{i}" title="/files{directory}/{i}" 
                class="{file_class}">{i}</a></li>"""
        return local_files
    except FileNotFoundError:
        return HTMLResponse(status_code=404)


def builder(index_of: str, files: str):
    html_content = f"""<html><head><title>{"Cloud"}</title>{style}</head><body><main>
                        <header><h1><i>Index of /{index_of}/</i></h1></header>
                        <ul id="files">{files}</ul>
                    </main></body></html>"""
    return HTMLResponse(content=html_content, status_code=200)


def handler(path: str, filename: str):
    try:
        files = listdir(path)
        if type(files) != str:
            with open("404.html", "r") as html:
                return HTMLResponse(content=html.read(), status_code=404)
        index_of = "root" if path == "" else f"root{path}"
        return builder(index_of, files)
    except NotADirectoryError:
        if filename.split(".")[1] == "html":
            with open(f"files{path}", "r") as html:
                return HTMLResponse(content=html.read(), status_code=200)
        return FileResponse(path=f"files{path}", filename=filename, media_type='application/octet-stream')


@app.get("/")
async def homepage():
    with open("index.html", "r") as home_page:
        return HTMLResponse(content=home_page.read(), status_code=200)


@app.get("/{path}")
async def other_page(path: str):
    if path == "files":
        return handler("", "")
    with open("404.html", "r") as home_page:
        return HTMLResponse(content=home_page.read(), status_code=200)


@app.get("/files/{path}")
async def second_level_dir(path: str):
    return handler(f"/{path}", path)


@app.get("/files/{path}/{path_1}")
async def third_level_dir(path: str, path_1: str):
    return handler(f"/{path}/{path_1}", path_1)


@app.get("/files/{path}/{path_1}/{path_2}")
async def fourth_level_dir(path: str, path_1: str, path_2: str):
    return handler(f"/{path}/{path_1}/{path_2}", path_2)


@app.get("/files/{path}/{path_1}/{path_2}/{path_3}")
async def fifth_level_dir(path: str, path_1: str, path_2: str, path_3: str):
    return handler(f"/{path}/{path_1}/{path_2}/{path_3}", path_3)


@app.get("/files/{path}/{path_1}/{path_2}/{path_3}/{path_4}")
async def sixth_level_dir(path: str, path_1: str, path_2: str, path_3: str, path_4: str):
    return handler(f"/{path}/{path_1}/{path_2}/{path_3}/{path_4}", path_4)


@app.get("/files/{path}/{path_1}/{path_2}/{path_3}/{path_4}/{path_5}")
async def seventh_level_dir(path: str, path_1: str, path_2: str, path_3: str, path_4: str, path_5: str):
    return handler(f"/{path}/{path_1}/{path_2}/{path_3}/{path_4}/{path_5}", path_5)


@app.get("/files/{path}/{path_1}/{path_2}/{path_3}/{path_4}/{path_5}/{path_6}")
async def eighth_level_dir(path: str, path_1: str, path_2: str, path_3: str, path_4: str, path_5: str, path_6: str):
    return handler(f"/{path}/{path_1}/{path_2}/{path_3}/{path_4}/{path_5}/{path_6}", path_6)


@app.get("/files/{path}/{path_1}/{path_2}/{path_3}/{path_4}/{path_5}/{path_6}/{path_7}")
async def ninth_level_dir(path: str, path_1: str, path_2: str, path_3: str, path_4: str, path_5: str, path_6: str,
                          path_7: str):
    return handler(f"/{path}/{path_1}/{path_2}/{path_3}/{path_4}/{path_5}/{path_6}/{path_7}", path_7)


@app.get("/files/{path}/{path_1}/{path_2}/{path_3}/{path_4}/{path_5}/{path_6}/{path_7}/{path_8}")
async def tenth_level_dir(path: str, path_1: str, path_2: str, path_3: str, path_4: str, path_5: str, path_6: str,
                          path_7: str, path_8: str):
    return handler(f"/{path}/{path_1}/{path_2}/{path_3}/{path_4}/{path_5}/{path_6}/{path_7}/{path_8}", path_8)


"""@app.get("/auth/")
async def authorization(key: str, Authorize: AuthJWT = Depends()):
    if key == root_key:
        return Authorize.create_access_token(subject=key)
    return HTMLResponse(status_code=404)"""


@app.post("/upload/")
async def upload_file(password: Optional[str] = None, path: Optional[str] = Query(None), data: UploadFile = File(...)):
    if password == root_key:
        return HTMLResponse(status_code=403)
    with open(f"temp/{path}/{data.filename}", "wb") as uploaded_file:
        uploaded_file.write(await data.read())
    from git import Repo
    repo = Repo("temp/.git")
    repo.git.add(update=True)
    repo.index.commit("test")
    origin = repo.remote(name='origin')
    origin.push()
    return True


@app.on_event("startup")
async def create_files():
    try:
        os.mkdir("temp")
        from git.repo.base import Repo
        Repo.clone_from(f"https://{token}:x-oauth-basic@github.com/Delivery-Klad/Cloud", "temp")
    except FileExistsError:
        pass
