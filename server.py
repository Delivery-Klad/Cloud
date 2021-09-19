import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse

app = FastAPI()
token = "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"
with open("Style/style.css", "r") as file:
    style = file.read()


def listdir(directory: str):
    local_files = ""
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
    with open("404.html", "r") as home_page:
        return HTMLResponse(content=home_page.read(), status_code=200)


@app.get("/files/")
async def root_dir():
    return handler("", "")


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


@app.get("/auth/")
async def authorization(key: str):
    return True


@app.post("/upload/")
async def test(data: UploadFile = File(...)):
    with open(f"temp/{data.filename}", "wb") as uploaded_file:
        uploaded_file.write(await data.read())
    from git import Repo
    repo = Repo("temp/.git")
    repo.git.add(update=True)
    repo.index.commit("test")
    origin = repo.remote(name='origin')
    origin.push()


@app.on_event("startup")
async def create_files():
    try:
        os.mkdir("temp")
        from git.repo.base import Repo
        Repo.clone_from(f"https://{token}:x-oauth-basic@github.com/Delivery-Klad/pages", "temp")
    except FileExistsError:
        pass
