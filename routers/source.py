from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from funcs.pages import show_not_found_page
from funcs.utils import error_log

router = APIRouter(prefix="/source")


@router.get("/{name}")
async def get_source(name: str, request: Request):
    try:
        return FileResponse(f"source/{name}")
    except FileNotFoundError:
        return show_not_found_page()
    except Exception as e:
        return error_log(str(e))
