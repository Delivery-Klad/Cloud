from fastapi.responses import HTMLResponse
from typing import Optional


def show_admin_index(content: str, redirect: str):
    with open("templates/admin.html", "r") as page:
        return HTMLResponse(content=page.read().format(content, redirect), status_code=200)


def show_auth_page(redirect: Optional[str] = "None"):
    with open("templates/auth.html", "r") as page:
        with open("source/auth.css", "r") as auth_style:
            return HTMLResponse(content=page.read().format(redirect, auth_style.read()), status_code=200)


def show_forbidden_page():
    with open("templates/403.html", "r") as page:
        return HTMLResponse(content=page.read(), status_code=403)


def show_not_found_page():
    with open("templates/404.html", "r") as page:
        return HTMLResponse(content=page.read(), status_code=404)
