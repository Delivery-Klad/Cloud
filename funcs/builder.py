from os import environ
from json import load
from time import sleep

from fastapi import Request
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse

from funcs.pages import show_not_found_page
from funcs.utils import is_root_user, constructor, get_menu, listdir, get_jwt_sub


def handler(path: str, filename: str, request: Request, auth_psw, download, redirects: int = None):
    try:
        files = listdir(path, request, auth_psw)
        if type(files) != str:
            if path == "":
                sleep(5)
                response = RedirectResponse("/files")
                if get_jwt_sub(request, auth_psw) is None:
                    response.delete_cookie("auth_psw")
                return response
            else:
                if redirects is None:
                    return RedirectResponse(f"/files{path}?redirects=1")
                else:
                    if redirects >= 10:
                        return show_not_found_page()
                    return RedirectResponse(f"/files{path}?redirects={redirects + 1}")
        index_of = "root" if path == "" else f"root{path}"
        return builder(request, index_of, files, auth_psw)
    except NotADirectoryError:
        file_extension = filename.split(".")[len(filename.split(".")) - 1]
        if not download:
            url = environ.get("server_url")
            if file_extension.lower() in ["txt", "py", "cs", "java", "class", "php", "html", "css", "js", "json", "go",
                                          "lua", "luac", "r", "rb", "c", "coffee", "hs", "lhs", "ss", "scm"]:
                with open(f"temp/files{path}", "rb") as page:
                    try:
                        with open("source_admin/languages.json", "r") as file:
                            lang = load(file)[file_extension.lower()]
                    except KeyError:
                        lang = "json"
                    response_text = """<head><title>Cloud - File viewer</title>
                        <link href="/source/rainbow_dark.css" rel="stylesheet" 
                        type="text/css"></head><body><pre><code data-language="{0}">{1}</code></pre><script 
                        src="/source/rainbow-custom.min.js"></script></body>"""
                    try:
                        return HTMLResponse(content=response_text.format(lang, page.read().decode("utf-8")
                                                                         .replace("<", "&lt;").replace(">", "&gt;")),
                                            status_code=200)
                    except UnicodeDecodeError:
                        return FileResponse(path=f"temp/files{path}", filename=filename,
                                            media_type='application/octet-stream')
            elif file_extension.lower() in ["png", "jpg", "gif", "jpeg", "svg", "bmp", "bmp ico", "png ico"]:
                with open("templates/img_viewer.html", "r") as page:
                    return HTMLResponse(content=page.read().format(filename, f"{url}files{path}"), status_code=200)
            elif file_extension.lower() in ["docx", "doc", "pptx", "ppt", "xls", "xlsx", "pdf"]:
                with open("templates/viewer.html", "r") as page:
                    return HTMLResponse(content=page.read().format(filename, f"{url}files{path}"), status_code=200)
        return FileResponse(path=f"temp/files{path}", filename=filename, media_type='application/octet-stream')


def builder(request: Request, index_of: str, files: str, auth_psw):
    upload_path = "/" if index_of.split("root")[1] == "" else index_of.split("root")[1]
    icons = f"""<h1><i><a href="/auth?redirect=files{upload_path}"
            title="Authorization"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                 viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg></a></i></h1>"""
    back_button, menu, title = "", "", ""
    if is_root_user(request, auth_psw):
        icons = constructor(icons, upload_path)
        menu = get_menu(index_of, True)
    else:
        menu = get_menu(index_of, False)
    index_of = index_of.replace("//", "/")
    if index_of[len(index_of) - 1] == "/":
        index_of = index_of[:-1]
    if index_of != "root":
        back_url = index_of.replace("root", "files", 1).split("/")
        back_url.pop(len(back_url) - 1)
        back_button = f"""<h1><i><a href="/{"/".join(back_url)}" title="Go back">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                         stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="15 18 9 12 15 6"></polyline></svg></a></i></h1>"""
    index_of = index_of.split("/")
    for i in index_of:
        if len(i) < 10:
            title += i
        else:
            title += i[:10] + "..."
        title += "/"
    with open("templates/files.html", "r") as html_content:
        return HTMLResponse(content=html_content.read().format(back_button, title, icons, files, menu), status_code=200)
