from os import environ

import heroku3
from fastapi import APIRouter, Request, Cookie
from fastapi.responses import JSONResponse
from typing import Optional

from funcs.utils import error_log, log, check_cookies, is_root_user, get_heroku_projects


router = APIRouter(prefix="/heroku")
keys = environ.get("keys").split(", ")


@router.get("/")
async def get_projects(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/heroku/' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            return {"res": get_heroku_projects(keys)}
        else:
            return JSONResponse({"res": "Access denied"}, status_code=403)
    except Exception as e:
        return error_log(str(e))


@router.patch("/")
async def enable_project(enable: bool, key: int, app: int, request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"PATCH Request to '/heroku/' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            cloud = heroku3.from_key(keys[key])
            app = cloud.apps()[0]
            if "web" in app.process_formation() or "worker" in app.process_formation():
                if "web" in app.process_formation():
                    dyn_type = "web"
                if "worker" in app.process_formation():
                    dyn_type = "worker"
                if enable:
                    scale = 1
                else:
                    scale = 0
                app.process_formation()[dyn_type].scale(scale)
                return JSONResponse({"res": "Project successfully scaled!"}, status_code=200)
            else:
                return JSONResponse({"res": "Project have no worker or web!"}, status_code=404)
        else:
            return {"res": "Failed"}
    except Exception as e:
        return error_log(str(e))
