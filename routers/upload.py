import json
from datetime import datetime

from fastapi import APIRouter, Cookie, Query, UploadFile, File
from fastapi.responses import RedirectResponse
from typing import Optional

from funcs.pages import show_forbidden_page
from funcs.utils import is_root_user

router = APIRouter(prefix="/upload_file")


@router.post("/")
async def upload_file(path: Optional[str] = Query(None), data: UploadFile = File(...),
                      auth_psw: Optional[str] = Cookie(None)):
    try:
        try:
            if not is_root_user(auth_psw):
                return show_forbidden_page()
        except AttributeError:
            return show_forbidden_page()
        with open(f"temp/{path}/{data.filename}", "wb") as uploaded_file:
            uploaded_file.write(await data.read())
        date = datetime.now().strftime("%d-%m-%y %H:%M")
        with open(f"temp/{path}/{data.filename}.meta", "w") as meta_file:
            json.dump({"create": str(date), "modif": str(date)}, meta_file)
        return RedirectResponse(f"/{path}", status_code=302)
    except Exception as er:
        print(er)
