from os import path as os_path

from fastapi import APIRouter, Request, Cookie
from fastapi.responses import FileResponse, HTMLResponse
from typing import Optional

from funcs.pages import show_not_found_page, show_forbidden_page
from funcs.utils import error_log, tree_view, log, check_cookies, is_root_user

router = APIRouter(prefix="/source")


@router.get("/tree")
async def get_tree_view(request: Request, path: str, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/source/tree' from '{request.client.host}' "
        f"with cookies '{check_cookies(request, auth_psw)}'")
    try:
        if not is_root_user(request, auth_psw):
            return show_forbidden_page()
    except AttributeError:
        return show_forbidden_page()
    html = ""
    if os_path.isdir(f"temp{path}"):
        replace_type = "folder"
    else:
        replace_type = "file"
    with open("templates/tree.html", "r") as file:
        with open("source_admin/replace.js") as script:
            return HTMLResponse(file.read().format(tree_view("temp/files", html, path, 0), replace_type, script.read()))


@router.get("/{name}")
async def get_source(name: str, request: Request):
    try:
        return FileResponse(f"source/{name}")
    except FileNotFoundError:
        return show_not_found_page()
    except Exception as e:
        return error_log(str(e))
