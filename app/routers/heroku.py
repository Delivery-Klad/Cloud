import urllib3
from json import load
from datetime import datetime

import heroku3
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Cookie, Depends
from fastapi.responses import JSONResponse
from typing import Optional

from app.database import crud, schemas
from app.funcs.utils import error_log, log, check_cookies, is_root_user, \
    get_heroku_projects, get_app_logs, get_app_vars, get_app_addon, update_app_var, delete_app_var
from app.dependencies import get_db, get_settings

settings = get_settings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
router = APIRouter(prefix="/heroku")
keys = settings.keys.split(", ")


def project_controller(db: Session):
    day = str(datetime.now().day)
    log(f"Today {day}")
    try:
        if crud.get_controller(db) == 0:
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
            crud.set_controller(1, db)
        if day != "1" and day != "21":
            crud.set_controller(0, db)
    except KeyError:
        log("Skip project controller")
        crud.set_controller(0, db)


@router.get("/")
async def get_projects(request: Request, db: Session = Depends(get_db),
                       auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/heroku/' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if is_root_user(request, auth_psw):
            return {"res": get_heroku_projects(keys)}
        else:
            return JSONResponse({"res": "Access denied"}, status_code=403)
    except Exception as e:
        return error_log(str(e))


@router.get("/logs")
async def get_project_logs(key: int, app: int, request: Request,
                           db: Session = Depends(get_db),
                           auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/heroku/logs' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if is_root_user(request, auth_psw):
            result = get_app_logs(keys, key, app)
            if len(result) > 0 and result != ['']:
                return {"res": result}
            else:
                return JSONResponse({"res": "Not found"}, status_code=404)
        else:
            return JSONResponse({"res": "Access denied"}, status_code=403)
    except Exception as e:
        return error_log(str(e))


@router.get("/vars")
async def get_project_vars(key: int, app: int, request: Request,
                           db: Session = Depends(get_db),
                           auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/heroku/vars' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if is_root_user(request, auth_psw):
            result = get_app_vars(keys, key, app)
            if len(result) > 0:
                return {"res": result}
            else:
                return JSONResponse({"res": "Not found"}, status_code=404)
        else:
            return JSONResponse({"res": "Access denied"}, status_code=403)
    except Exception as e:
        return error_log(str(e))


@router.get("/addon")
async def get_project_addon(key: int, app: int, request: Request,
                            db: Session = Depends(get_db),
                            auth_psw: Optional[str] = Cookie(None)):
    log(f"GET Request to '/heroku/addon' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if is_root_user(request, auth_psw):
            result = get_app_addon(keys, key, app)
            if len(result) > 0:
                return {"res": result}
            else:
                return JSONResponse({"res": "Not found"}, status_code=404)
        else:
            return JSONResponse({"res": "Access denied"}, status_code=403)
    except Exception as e:
        return error_log(str(e))


@router.patch("/var")
async def update_var(data: schemas.UpdateVar, request: Request,
                     db: Session = Depends(get_db),
                     auth_psw: Optional[str] = Cookie(None)):
    log(f"PATCH Request to '/heroku/var' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
    if data.var_name[-2:] == ": ":
        data.var_name = data.var_name[:-2]
    try:
        if is_root_user(request, auth_psw):
            result = update_app_var(keys, data)
            if result is True:
                return {"res": "Variable successfully set"}
            else:
                return JSONResponse({"res": "Not found"}, status_code=404)
        else:
            return JSONResponse({"res": "Access denied"}, status_code=403)
    except Exception as e:
        return error_log(str(e))


@router.delete("/var")
async def delete_var(data: schemas.DeleteVar, request: Request,
                     db: Session = Depends(get_db),
                     auth_psw: Optional[str] = Cookie(None)):
    log(f"DELETE Request to '/heroku/var' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
    data.title = data.title[:-2]
    try:
        if is_root_user(request, auth_psw):
            result = delete_app_var(keys, data)
            if result is True:
                return {"res": "Variable successfully delete"}
            else:
                return JSONResponse({"res": "Not found"}, status_code=404)
        else:
            return JSONResponse({"res": "Access denied"}, status_code=403)
    except Exception as e:
        return error_log(str(e))


@router.patch("/")
async def enable_project(data: schemas.ProjectController,
                         request: Request,
                         auth_psw: Optional[str] = Cookie(None),
                         db: Session = Depends(get_db)):
    log(f"PATCH Request to '/heroku/' from '{request.client.host}' with "
        f"cookies '{check_cookies(request, auth_psw, db)}'")
    try:
        if is_root_user(request, auth_psw):
            cloud = heroku3.from_key(keys[data.key])
            app = cloud.apps()[data.app]
            if "web" in app.process_formation() or "worker" \
                    in app.process_formation():
                if "web" in app.process_formation():
                    dyn_type = "web"
                elif "worker" in app.process_formation():
                    dyn_type = "worker"
                scale = 1 if data.enable else 0
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
