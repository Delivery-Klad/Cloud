import os
from json import dump, load
from datetime import datetime

from fastapi import APIRouter, Cookie, Request, Query, UploadFile, File
from typing import Optional
from pydantic import BaseModel

from funcs.pages import show_forbidden_page
from funcs.utils import is_root_user, log, error_log, check_cookies

router = APIRouter(prefix="/file")


class FileData(BaseModel):
    file_path: str
    file_name: Optional[str] = None
    new_name: Optional[str] = None


@router.post("/")
async def upload_file(request: Request, path: Optional[str] = Query(None), data: UploadFile = File(...),
                      auth_psw: Optional[str] = Cookie(None)):
    log(f"POST Request to '/upload/{data.filename}' from '{request.client.host}' "
        f"with cookies '{check_cookies(request, auth_psw)}'")
    try:
        try:
            if not is_root_user(request, auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        with open(f"temp/{path}/{data.filename}", "wb") as uploaded_file:
            uploaded_file.write(await data.read())
        date = datetime.now().strftime("%d-%m-%y %H:%M")
        if os.path.exists(f"temp/{path}/{data.filename}.meta"):
            with open(f"temp/{path}/{data.filename}.meta", "r") as meta_file:
                meta_data = load(meta_file)
            with open(f"temp/{path}/{data.filename}.meta", "w") as meta_file:
                dump({"create": str(meta_data["create"]), "modif": str(date)}, meta_file)
        else:
            with open(f"temp/{path}/{data.filename}.meta", "w") as meta_file:
                dump({"create": str(date), "modif": str(date)}, meta_file)
        return True
    except Exception as er:
        return error_log(str(er))


@router.put("/")
async def rename(request: Request, file: FileData, auth_psw: Optional[str] = Cookie(None)):
    try:
        log(f"PUT Request to '/file' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
        try:
            if not is_root_user(request, auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        os.rename(f"temp/{file.file_path}/{file.file_name}", f"temp/{file.file_path}/{file.new_name}")
        try:
            os.rename(f"temp/{file.file_path}/{file.file_name}.meta", f"temp/{file.file_path}/{file.new_name}.meta")
        except FileNotFoundError:
            pass
        return {"res": True}
    except Exception as e:
        return error_log(str(e))


@router.delete("/")
async def delete(request: Request, file: FileData, auth_psw: Optional[str] = Cookie(None)):
    try:
        log(f"DELETE Request to '/file' from '{request.client.host}' with cookies "
            f"'{check_cookies(request, auth_psw)}'")
        try:
            if not is_root_user(request, auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        os.remove(f"temp/{file.file_path}")
        try:
            os.remove(f"temp/{file.file_path}.meta")
        except FileNotFoundError:
            pass
        return {"res": True}
    except Exception as e:
        return error_log(str(e))


@router.get("/meta")
async def get_meta(path: str, name: str, request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/meta' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
    try:
        size = os.path.getsize(f"temp/{path}{name}")
        size /= 1024
        size = round(size)
        if size > 1024:
            size /= 1020
            size = round(size, 1)
            size = str(size) + " МБ"
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
