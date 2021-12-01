import os

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import RedirectResponse
from typing import Optional

from funcs.pages import show_forbidden_page
from funcs.utils import is_root_user, log, error_log, check_cookies

router = APIRouter(prefix="/rename")


@router.get("/")
async def rename(request: Request, del_name: str, path: str, new_name: str, auth_psw: Optional[str] = Cookie(None)):
    try:
        log(f"GET Request to '/rename' from '{request.client.host}' with cookies '{check_cookies(request, auth_psw)}'")
        try:
            if not is_root_user(auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        os.rename(f"temp/{path}/{del_name}", f"temp/{path}/{new_name}")
        os.rename(f"temp/{path}/{del_name}.meta", f"temp/{path}/{new_name}.meta")
        return RedirectResponse(path)
    except Exception as e:
        error_log(str(e))
