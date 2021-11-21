from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from funcs.pages import show_not_found_page
from funcs.utils import log, error_log

router = APIRouter(prefix="/source")


@router.get("/{name}")
async def get_source(name: str, request: Request):
    log(f"GET Request to '/source/{name}' from '{request.client.host}'")
    try:
        return FileResponse(f"source/{name}")
    except FileNotFoundError:
        show_not_found_page()
    except Exception as e:
        error_log(str(e))
