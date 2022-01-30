from sqlalchemy import Column, Integer, String

from app.database.database import DataBase


class Users(DataBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    message = Column(String(), nullable=False)
