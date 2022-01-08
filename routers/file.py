from os import path as os_path, rename, listdir, replace
from json import dump, load
from datetime import datetime

from fastapi import APIRouter, Cookie, Request, Query, UploadFile, File
from fastapi.responses import HTMLResponse
from typing import Optional
from pydantic import BaseModel

from funcs.pages import show_forbidden_page
from funcs.utils import is_root_user, log, error_log, check_cookies, delete_full_file

router = APIRouter(prefix="/file")


class FileData(BaseModel):
    file_path: str
    file_name: Optional[str] = None
    new_name: Optional[str] = None


class ReplaceFile(BaseModel):
    old_path: str
    new_path: str


@router.post("/")
async def upload_file(request: Request, path: Optional[str] = Query(None), data: UploadFile = File(...),
                      auth_psw: Optional[str] = Cookie(None)):
    log(f"POST Request to '/file/{data.filename}' from '{request.client.host}' "
        f"with cookies '{check_cookies(request, auth_psw)}'")
    if data.filename == "":
        return HTMLResponse(status_code=403)
    try:
        try:
            if not is_root_user(request, auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        file_path = f"temp/{path}/{data.filename}"
        if data.filename in listdir(f"temp/{path}"):
            new_name = data.filename.split(".")
            if len(new_name) < 1:
                file_extension = new_name[len(new_name) - 1]
                new_name = ".".join(new_name[:-1]) + "(1)"
                file_path = f"temp/{path}/{new_name}.{file_extension}"
            else:
                file_path = f"temp/{path}/{data.filename + '(1)'}"
        with open(file_path, "wb") as uploaded_file:
            uploaded_file.write(await data.read())
        date = datetime.now().strftime("%d-%m-%y %H:%M")
        if os_path.exists(f"temp/{path}/{data.filename}.meta"):
            with open(f"temp/{path}/{data.filename}.meta", "r") as meta_file:
                meta_data = load(meta_file)
            with open(f"temp/{path}/{data.filename}.meta", "w") as meta_file:
                dump({"create": str(meta_data["create"]), "modif": str(date)}, meta_file)
        else:
            with open(f"temp/{path}/{data.filename}.meta", "w") as meta_file:
                dump({"create": str(date), "modif": str(date)}, meta_file)
        return HTMLResponse(status_code=201)
    except Exception as er:
        return error_log(str(er))


@router.patch("/")
async def rename_file(request: Request, file: FileData, auth_psw: Optional[str] = Cookie(None)):
    try:
        log(f"PATCH Request to '/file/' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
        try:
            if not is_root_user(request, auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        rename(f"temp/{file.file_path}/{file.file_name}", f"temp/{file.file_path}/{file.new_name}")
        try:
            rename(f"temp/{file.file_path}/{file.file_name}.meta", f"temp/{file.file_path}/{file.new_name}.meta")
        except FileNotFoundError:
            pass
        return {"res": True}
    except Exception as e:
        return error_log(str(e))


@router.put("/")
async def replace_file(request: Request, data: ReplaceFile, auth_psw: Optional[str] = Cookie(None)):
    log(f"PUT Request to '/file/' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
    try:
        try:
            if not is_root_user(request, auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        file_name = data.old_path.split("/")
        file_name = file_name[len(file_name) - 1]
        replace(f"temp{data.old_path}", f"temp{data.new_path}/{file_name}")
        try:
            replace(f"temp{data.old_path}.meta", f"temp{data.new_path}/{file_name}.meta")
        except FileNotFoundError:
            pass
        return {"res": True}
    except Exception as er:
        return error_log(str(er))


@router.delete("/")
async def delete_file(request: Request, file: FileData, auth_psw: Optional[str] = Cookie(None)):
    try:
        log(f"DELETE Request to '/file/' from '{request.client.host}' with cookies "
            f"'{check_cookies(request, auth_psw)}'")
        try:
            if not is_root_user(request, auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        delete_full_file(file.file_path)
        return {"res": True}
    except Exception as e:
        return error_log(str(e))


@router.get("/meta")
async def get_meta(path: str, name: str, request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/meta' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
    try:
        size = round(os_path.getsize(f"temp/{path}{name}") / 1024)
        if size > 1024:
            size = str(round(size / 1024, 1)) + " МБ"
        else:
            size = str(size) + " КБ"
        try:
            with open(f"temp/{path}{name}.meta", "r") as meta_file:
                meta_json = load(meta_file)
                return {"res": [f"Дата создания: {meta_json['create']}", f"Дата изменения: {meta_json['modif']}",
                                f"Размер: {size}"]}
        except FileNotFoundError:
            date = datetime.now().strftime("%d-%m-%y %H:%M")
            with open(f"temp/{path}{name}.meta", "w") as meta_file:
                dump({"create": str(date), "modif": str(date)}, meta_file)
            return {"res": [f"Дата создания: {date}", f"Дата изменения: {date}",
                            f"Размер: {size}"]}
    except Exception as e:
        return error_log(str(e))
