from pydantic import BaseModel
from typing import Optional


class Folder(BaseModel):
    path: str
    arg: str
    access: str


class ReplaceFolder(BaseModel):
    old_path: str
    new_path: str


class DeleteFolder(BaseModel):
    file_path: str


class FileData(BaseModel):
    file_path: str
    file_name: Optional[str] = None
    new_name: Optional[str] = None


class ReplaceFile(BaseModel):
    old_path: str
    new_path: str


class UpdateVar(BaseModel):
    app: int
    key: int
    var_name: str
    var_value: str


class DeleteVar(BaseModel):
    app: int
    key: int
    title: str


class ProjectController(BaseModel):
    enable: bool
    key: int
    app: int


class UserPermissions(BaseModel):
    up: bool
    user: int
