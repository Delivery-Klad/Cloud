import os

import bcrypt
from fastapi import APIRouter, Cookie
from fastapi.responses import RedirectResponse
from typing import Optional

from funcs.pages import show_forbidden_page

router = APIRouter(prefix="/add_text")


@router.get("/")
async def add_text(main_theme: str, arg: str, themes: str, auth_psw: Optional[str] = Cookie(None)):
    try:
        if not bcrypt.checkpw(os.environ.get("viewer_key").encode("utf-8"), auth_psw.encode("utf-8")) and not \
                bcrypt.checkpw(os.environ.get("root_psw").encode("utf-8"), auth_psw.encode("utf-8")):
            return show_forbidden_page()
        print(main_theme)
        print(arg)
        print(len(arg.split(" ")))
        print(themes)
        return RedirectResponse(f"/files/7%20сем/Информационно-поисковые%20системы", status_code=302)
    except AttributeError:
        return show_forbidden_page()
    except Exception as er:
        print(er)
