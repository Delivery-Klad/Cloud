import os

from docx import Document
from fastapi import APIRouter, Cookie
from fastapi.responses import RedirectResponse
from typing import Optional

from funcs.pages import show_forbidden_page
from funcs.utils import is_authorized_user

router = APIRouter(prefix="/add_text")
folder_path = "temp/files/7 сем/Информационно-поисковые системы/300 текстов"


@router.get("/")
async def add_text(main_theme: str, arg: str, themes: str, link: str, auth_psw: Optional[str] = Cookie(None)):
    try:
        if not is_authorized_user(auth_psw):
            return show_forbidden_page()
        document = Document()
        if len(arg.split(" ")) < 200:
            path = f"{folder_path}/Short"
        elif 499 < len(arg.split(" ")) < 800:
            path = f"{folder_path}/Middle"
        elif 499 < len(arg.split(" ")) < 800:
            path = f"{folder_path}/Long"
        texts = sorted(os.listdir(path))
        if len(texts) == 1:
            name = "1.docx"
        else:
            name = str(int(texts[len(texts) - 2].split(".")[0]) + 1) + ".docx"
        document.add_paragraph(arg)
        document.save(f'{path}/{name}')
        document = Document()
        document.add_paragraph(f"Количество слов - {len(arg.split(' '))}\nОсновная тематика - {main_theme}\nСмежные "
                               f"тематики - {themes}\nИсточник - {link}")
        document.save(f'{path}/Справочные карточки/Справочная карточка_{name}')
        return RedirectResponse(f"/files/7%20сем/Информационно-поисковые%20системы/300%20текстов", status_code=302)
    except AttributeError:
        return show_forbidden_page()
    except Exception as er:
        print(er)
