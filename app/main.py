from os import mkdir, environ
from shutil import make_archive
from datetime import datetime
from random import randint
from secrets import token_hex

from bcrypt import gensalt, hashpw
from dropbox import Dropbox
from sqlalchemy.orm import Session
from fastapi import FastAPI, Request, Cookie, Depends, Response
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Optional
from pydantic import BaseModel
from git import Repo

from app.funcs.pages import show_auth_page, show_admin_index,\
    show_not_found_page
from app.funcs.builder import handler
from app.funcs.content_length import LimitUploadSize
from app.funcs.utils import is_root_user, log, error_log, check_cookies
from app.routers import source, file
from app.routers import heroku, folder, admin
from app.database import crud, models
from app.database.database import engine, SessionLocal
from app.dependencies import get_db, get_settings


settings = get_settings()
swagger_url = token_hex(randint(10, 15))
app = FastAPI(docs_url=f"/{swagger_url}", redoc_url=None, dependencies=[Depends(get_db)])
app.include_router(admin.router)
app.include_router(heroku.router)
app.include_router(source.router)
app.include_router(folder.router)
app.include_router(file.router)
app.add_middleware(LimitUploadSize, max_upload_size=50_000_000)
token = settings.gh_token
dbx_token = settings.dbx_token
url = settings.server_url


class JWTSettings(BaseModel):
    authjwt_secret_key: str = settings.secret


@AuthJWT.load_config
def get_config():
    return JWTSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code,
                        content={"detail": exc.message})


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/swagger")
async def swagger(request: Request):
    return {"res": swagger_url}


@app.get("/")
async def homepage(request: Request):
    try:
        log(f"GET Request to '/' from '{request.client.host}'")
        return RedirectResponse(url + "files")
    except Exception as e:
        return error_log(str(e))


@app.get("/{path}")
async def other_page(path: str, request: Request, arg: Optional[str] = None,
                     arg2: Optional[str] = None,
                     auth_psw: Optional[str] = Cookie(None),
                     download: Optional[bool] = None,
                     redirect: Optional[str] = None,
                     preview: Optional[bool] = None,
                     db: Session = Depends(get_db)):
    log(f"GET Request to '/{path}' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if path == "files":
            return handler("", "", request, auth_psw, download,
                           preview=preview)
        elif path == "auth":
            if arg is None or arg2 is None:
                return show_auth_page(redirect)
            else:
                result = crud.check_password(arg2, arg, db)
                if result:
                    authorize = AuthJWT()
                    response = JSONResponse({"result": True})
                    perm = crud.get_permissions(arg2, db)
                    response.set_cookie(key="auth_psw",
                                        value=authorize
                                        .create_refresh_token(f"{perm}://:"
                                                              f"{arg2}"),
                                        secure=True)
                    return response
                elif result is None:
                    if len(arg2) < 4 or len(arg) < 8:
                        return JSONResponse({"result": "Wrong input"},
                                            status_code=403)
                    for i in arg2:
                        if ord(i) < 33 or ord(i) > 122:
                            return JSONResponse({"result": "И как ты до этого добрался? Сказано же, что нельзя "
                                                           "использовать эти символы"}, status_code=403)
                    if crud.create_user(arg2, str(hashpw(arg.encode("utf-8"), gensalt()))[2:-1], request, db):
                        authorize = AuthJWT()
                        response = JSONResponse({"result": True})
                        perm = crud.get_permissions(arg2, db)
                        response.set_cookie(key="auth_psw",
                                            value=authorize
                                            .create_refresh_token(f"{perm}://:"
                                                                  f"{arg2}"),
                                            secure=True)
                        return response
                    else:
                        return JSONResponse({"result": "Что-то пошло не так"}, status_code=403)
                elif not result:
                    return JSONResponse({"result": "Неверный пароль"}, status_code=403)
        elif path == "admin":
            if is_root_user(request, auth_psw):
                content = ""
                temp = await admin.admin_dashboard(request, db=db, auth_psw=auth_psw)
                for i in temp['res']:
                    if i == "Summary":
                        content += f"""<div style="font-weight: bold; font-size: 20px;">{i}</div>"""
                    else:
                        content += f"<div>{i}</div>"
                if arg is None:
                    arg = "files"
                if arg[len(arg) - 1] == "/":
                    arg = arg[:-1]
                return show_admin_index(content, arg)
            else:
                return show_auth_page("admin")
        return show_not_found_page()
    except Exception as e:
        return error_log(str(e))


@app.get("/files/{catchall:path}")
async def get_files(request: Request,
                    auth_psw: Optional[str] = Cookie(None),
                    download: Optional[bool] = None,
                    redirects: Optional[int] = None,
                    preview: Optional[bool] = None,
                    db: Session = Depends(get_db)):
    try:
        path = request.path_params["catchall"]
        log(f"GET Request to '/{path}' from '{request.client.host}' with "
            f"cookies '{check_cookies(request, auth_psw, db)}'")
        name = path.split("/")
        if redirects is None:
            return handler(f"/{path}", name[len(name) - 1], request, auth_psw, download, preview=preview)
        else:
            return handler(f"/{path}", name[len(name) - 1], request, auth_psw, download, redirects, preview)
    except Exception as e:
        return error_log(str(e))


@app.on_event("startup")
def startup():
    models.DataBase.metadata.create_all(bind=engine)
    with Session(engine) as db:
        crud.set_default_parameters(db)
    try:
        with open("log.txt", "w") as log_file:
            log_file.write(f"{str(datetime.utcnow())[:-7]} - Application startup")
        with open("error_log.txt", "w") as log_file:
            log_file.write(f"{str(datetime.utcnow())[:-7]} - Application startup")
        heroku.project_controller(db)
        environ["start_time"] = str(datetime.utcnow())[:-7]
        print("Starting startup process...")
        try:
            print("Cloning repo...")
            mkdir("temp")
            from git.repo.base import Repo
            Repo.clone_from(f"https://{token}:x-oauth-basic@github.com/Delivery-Klad/files",
                            "temp")
            print("Cloning success!")
        except FileExistsError:
            pass
        print("Startup complete!")
    except Exception as e:
        return error_log(str(e))


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
        dbx = Dropbox(dbx_token)
        make_archive("backup_archive", "zip", "../temp/files/7 сем")
        import random
        with open("backup_archive.zip", "rb") as archive:
            print("Upload archive!")
            dbx.files_upload(archive.read(), f"/backup{random.randint(1, 1000)}.zip")
        print("Archive uploaded!")
    print("Shutdown complete!")
