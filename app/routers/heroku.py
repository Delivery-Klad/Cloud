import urllib3
from json import load
from datetime import datetime

import heroku3
from fastapi import APIRouter, Request, Cookie
from fastapi.responses import JSONResponse
from typing import Optional

from app.funcs.database import get_controller, set_controller
from app.funcs.utils import error_log, log, check_cookies, is_root_user, get_heroku_projects, get_app_logs, get_app_vars
from app.dependencies import get_db, get_settings


settings = get_settings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
router = APIRouter(prefix="/heroku")
keys = settings.keys.split(", ")


def project_controller():
    day = str(datetime.now().day)
    log(f"Today {day}")
    try:
        if get_controller() == 0:
            log("Start project controller")
            with open("app/source/admin/schedule.json", "r") as file:
                schedule = load(file)[day]
                for i in schedule:
                    cloud = heroku3.from_key(keys[i["key"]])
                    app = cloud.apps()[i["app"]]
                    if "web" in app.process_formation():
                        dyn_type = "web"
                    elif "worker" in app.process_formation():
                        dyn_type = "worker"
                    log(f"{app.name} ({dyn_type}) - scale={i['scale']}")
                    app.process_formation()[dyn_type].scale(i["scale"])
            set_controller(1)
        if day != "1" and day != "21":
            set_controller(0)
    except KeyError:
        log("Skip project controller")
        set_controller(0)


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


@router.get("/logs")
async def get_project_logs(key: int, app: int, request: Request,
                           auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/heroku/logs' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            logs = get_app_logs(keys, key, app)
            if len(logs) > 0 and logs != ['']:
                return {"res": logs}
            else:
                return JSONResponse({"res": "Not found"}, status_code=404)
        else:
            return JSONResponse({"res": "Access denied"}, status_code=403)
    except Exception as e:
        return error_log(str(e))


@router.get("/vars")
async def get_project_vars(key: int, app: int, request: Request,
                           auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/heroku/vars' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            var = get_app_vars(keys, key, app)
            if len(var) > 0:
                return {"res": var}
            else:
                return JSONResponse({"res": "Not found"}, status_code=404)
        else:
            return JSONResponse({"res": "Access denied"}, status_code=403)
    except Exception as e:
        return error_log(str(e))


@router.patch("/")
async def enable_project(enable: bool, key: int, app: int,request: Request,
                         auth_psw: Optional[str] = Cookie(None)):
    log(f"PATCH Request to '/heroku/' from '{request.client.host}' with "
        f"cookies "
        f"'{check_cookies(request, auth_psw)}'")
    try:
        if is_root_user(request, auth_psw):
            cloud = heroku3.from_key(keys[key])
            app = cloud.apps()[app]
            if "web" in app.process_formation() or "worker" \
                    in app.process_formation():
                if "web" in app.process_formation():
                    dyn_type = "web"
                elif "worker" in app.process_formation():
                    dyn_type = "worker"
                if enable:
                    scale = 1
                else:
                    scale = 0
                app.process_formation()[dyn_type].scale(scale)
                return JSONResponse({"res": "Project successfully scaled!"},
                                    status_code=200)
            else:
                return JSONResponse({"res": "Project have no worker or web!"},
                                    status_code=404)
        else:
            return JSONResponse({"res": "Access denied"}, status_code=403)
    except Exception as e:
        return error_log(str(e))
