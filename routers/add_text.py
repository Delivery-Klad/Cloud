import os

from docx import Document
from docx.shared import Pt
from docx.enum.style import WD_STYLE_TYPE
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
        p = document.add_paragraph()
        font_styles = document.styles
        font_charstyle = font_styles.add_style('CommentsStyle', WD_STYLE_TYPE.CHARACTER)
        font_object = font_charstyle.font
        font_object.size = Pt(14)
        font_object.name = 'Times New Roman'
        p.add_run(arg, style='CommentsStyle')
        document.save(f'{path}/{name}')

        document = Document()
        p = document.add_paragraph()
        font_styles = document.styles
        font_charstyle = font_styles.add_style('CommentsStyle', WD_STYLE_TYPE.CHARACTER)
        font_object = font_charstyle.font
        font_object.size = Pt(14)
        font_object.name = 'Times New Roman'
        p.add_run(f"Количество слов - {len(arg.split(' '))}\nОсновная тематика - {main_theme}\nСмежные"
                  f" тематики - {themes}\nИсточник - {link}", style='CommentsStyle')
        document.save(f'{path}/Справочные карточки/Справочная карточка_{name}')
        return RedirectResponse(f"/files/7%20сем/Информационно-поисковые%20системы", status_code=302)
    except AttributeError:
        return show_forbidden_page()
    except Exception as er:
        print(er)


@router.get("/check/")
async def check_text(arg: str, auth_psw: Optional[str] = Cookie(None)):
    try:
        if not is_authorized_user(auth_psw):
            return show_forbidden_page()
        return f"Words count: {len(arg.split(' '))}"
    except AttributeError:
        return show_forbidden_page()
    except Exception as er:
        print(er)
