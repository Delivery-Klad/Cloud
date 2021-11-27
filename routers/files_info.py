import os
import json

from typing import Optional
from fastapi import APIRouter, Request, Cookie
from funcs.utils import log, error_log, check_cookies


router = APIRouter(prefix="/meta")


@router.get("/")
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
                meta_json = json.load(meta_file)
                return {"res": [f"Дата создания: {meta_json['create']}", f"Дата изменения: {meta_json['modif']}",
                                f"Размер: {size}"]}
        except FileNotFoundError:
            return {"res": [f"Размер: {size}"]}
    except Exception as e:
        error_log(str(e))
