from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from funcs.pages import show_not_found_page

router = APIRouter(prefix="/source")


@router.get("/{name}")
async def get_source(name: str, request: Request):
    try:
        return FileResponse(f"source/{name}")
    except FileNotFoundError:
        show_not_found_page()
