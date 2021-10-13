from fastapi.responses import HTMLResponse
from typing import Optional


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


def show_upload_page(arg):
    with open("templates/upload.html", "r") as page:
        with open("source/upload.css", "r") as upload_style:
            return HTMLResponse(content=page.read().format(arg, upload_style.read()), status_code=200)


def show_create_page(arg, title, arg2, name, root, auth, all_users):
    with open("templates/create.html", "r") as page:
        with open("source/create.css", "r") as create_style:
            return HTMLResponse(content=page.read().format(arg, create_style.read(), title, arg2, name, root, auth,
                                                           all_users), status_code=200)
