import os

from fastapi import APIRouter, Cookie
from fastapi.responses import RedirectResponse
from typing import Optional

from funcs.pages import show_forbidden_page
from funcs.utils import is_root_user

router = APIRouter(prefix="/delete")


@router.get("/")
async def delete(del_name: Optional[str], path: Optional[str], auth_psw: Optional[str] = Cookie(None)):
    try:
        if not is_root_user(auth_psw):
            return show_forbidden_page()
    except AttributeError:
        return show_forbidden_page()
    file_path = f"temp/{path}/{del_name}"
    meta_file = f"temp/{path}/{del_name}.meta"
    os.remove(file_path)
    try:
        os.remove(meta_file)
    except FileNotFoundError:
        pass
    return RedirectResponse(path)
