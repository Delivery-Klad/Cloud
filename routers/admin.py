import shutil

import dropbox
from fastapi import APIRouter, Cookie, Response
from git import Repo
from typing import Optional

from funcs.utils import is_root_user

router = APIRouter(prefix="/admin")
dbx_token = "vuMWKf0zPEgAAAAAAAAAAe4Uhy9mh-hSArGSGdU5w7AyUvFE7TKwNzX6h_dpDP4r"


@router.get("/home")
async def admin_home(auth_psw: Optional[str] = Cookie(None)):
    if is_root_user(auth_psw):
        return "Success"
    else:
        return "Failed"


@router.get("/dashboard")
async def admin_dashboard(auth_psw: Optional[str] = Cookie(None)):
    if is_root_user(auth_psw):
        return "Success"
    else:
        return "Failed"


@router.get("/push_files")
async def admin_push_files(auth_psw: Optional[str] = Cookie(None)):
    if is_root_user(auth_psw):
        print("Starting push files process...")
        try:
            result = []
            repo = Repo("temp/.git")
            for item in repo.untracked_files:
                result.append(item)
            for item in repo.index.diff(None):
                result.append(item)
            if result:
                print("Untracked files detected...")
                repo.git.add(all=True)
                repo.index.commit("commit from cloud")
                origin = repo.remote(name='origin')
                origin.push()
                print("Push success!")
        except Exception as e:
            print(f"Error: {e}")
            print("Creating archive!")
            dbx = dropbox.Dropbox(dbx_token)
            shutil.make_archive("aboba", "zip", "temp/files/7 сем")
            import random
            with open("aboba.zip", "rb") as archive:
                print("Upload archive!")
                dbx.files_upload(archive.read(), f"/backup{random.randint(1, 1000)}.zip")
            print("Archive uploaded!")
        return Response(content="Push files complete!", status_code=200)
    else:
        return Response(content="Unauthorized", status_code=403)
