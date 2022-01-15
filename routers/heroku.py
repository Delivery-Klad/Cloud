from os import environ

import heroku3
from fastapi import APIRouter, Request, Cookie
from fastapi.responses import JSONResponse
from typing import Optional

from funcs.utils import error_log, log, check_cookies, is_root_user


router = APIRouter(prefix="/heroku")

keys = environ.get("keys").split(", ")


def get_test_projects():
    result = []
    for i in range(len(keys)):
        cloud = heroku3.from_key(keys[i])
        print(cloud.account().email)
        temp = []
        apps = cloud.apps()
        for j in range(len(apps)):
            enable = "ON"
            if not apps[j].process_formation():
                dyn_type = "database"
            elif "web" in apps[j].process_formation():
                dyn_type = "web"
            elif "worker" in apps[j].process_formation():
                dyn_type = "bot"
            if len(apps[j].dynos()) == 0:
                enable = "OFF"
            temp.append({"name": apps[j].name, "type": dyn_type, "enable": enable, "args": f"{i}, {j}"})
        result.append({"email": cloud.account().email, "apps": temp})
    return result
# app.process_formation()['web'].scale(1)


@router.get("/")
async def get_projects(request: Request, auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/heroku/' from '{request.client.host}' with cookies "
        f"'{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            return {"res": get_test_projects()}
        else:
            return {"res": "Failed"}
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
