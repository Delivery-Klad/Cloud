import os

import bcrypt
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from typing import Optional

from funcs.pages import show_forbidden_page

router = APIRouter(prefix="/delete")


@router.get("/")
async def delete(del_name: Optional[str], path: Optional[str], auth_psw: Optional[str] = Cookie(None)):
    try:
        if not bcrypt.checkpw(os.environ.get("root_psw").encode("utf-8"), auth_psw.encode("utf-8")):
            return show_forbidden_page()
    except AttributeError:
        return show_forbidden_page()
    file_path = f"temp/{path}/{del_name}"
    print(file_path)
    os.remove(file_path)
    return RedirectResponse(path)
