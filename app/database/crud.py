from bcrypt import checkpw
from fastapi import Request
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.database import models


def set_default_parameters(db: Session):
    db_data = db.query(models.Controller).first()
    if db_data is None:
        data = models.Controller(enable=0)
        db.add(data)
        db.commit()


def get_controller(db: Session):
    db_data = db.query(models.Controller).first()
    return db_data.enable


def set_controller(value: int, db: Session):
    db_data = db.query(models.Controller).first()
    db_data.enable = value
    db.commit()


def get_permissions(login: str, db: Session):
    try:
        db_data = db.query(models.Users).filter(models.Users.login == login).first()
        return db_data.permissions
    except Exception as e:
        print(e)
        return None


def set_permissions(user_id: int, up: bool, db: Session):
    try:
        db_data = db.query(models.Users).filter(models.Users.id == user_id).first()
        current_permissions = db_data.permissions
        if up:
            if current_permissions >= 5:
                return current_permissions
            current_permissions += 1
        else:
            if current_permissions <= 0:
                return current_permissions
            current_permissions -= 1
        db_data.permissions = current_permissions
        db.commit()
        return current_permissions
    except Exception as e:
        print(e)
        return None


def get_users(db):
    return db.query(models.Users).order_by(models.Users.id).all()


def create_user(login: str, password: str, request: Request, db: Session):
    try:
        agent = request.headers["user-agent"]
        data = models.Users(login=login, password=password,
                            useragent=agent, permissions=0)
        db.add(data)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False


def delete_user(user_id: int, db: Session):
    db.execute(delete(models.Users).where(models.Users.id == user_id))
    db.commit()


def check_password(login: str, password: str, db: Session):
    try:
        db_data = db.query(models.Users).filter(models.Users.login == login).first()
        db_password = db_data.password
        if checkpw(password.encode("utf-8"), db_password.encode("utf-8")):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return None
