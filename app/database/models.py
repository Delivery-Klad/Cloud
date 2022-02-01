from sqlalchemy import Column, Integer, String

from app.database.database import DataBase


class Users(DataBase):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    login = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    useragent = Column(String(300), nullable=False)
    permissions = Column(Integer, nullable=False)


class Controller(DataBase):
    __tablename__ = "controller"
    enable = Column(Integer, primary_key=True)
