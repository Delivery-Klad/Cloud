import os

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import RedirectResponse
from typing import Optional

from funcs.pages import show_forbidden_page
from funcs.utils import is_root_user, log, error_log, check_cookies

router = APIRouter(prefix="/delete")


@router.get("/")
async def delete(request: Request, name: Optional[str], path: Optional[str], auth_psw: Optional[str] = Cookie(None)):
    try:
        log(f"GET Request to '/delete' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
        try:
            if not is_root_user(auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        file_path = f"temp/{path}/{name}"
        meta_file = f"temp/{path}/{name}.meta"
        os.remove(file_path)
        try:
            os.remove(meta_file)
        except FileNotFoundError:
            pass
        return RedirectResponse(path)
    except Exception as e:
        error_log(str(e))
