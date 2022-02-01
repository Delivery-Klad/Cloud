from os import environ

from bcrypt import checkpw
from psycopg2 import connect as db_connection
from fastapi import Request


def db_connect():
    try:
        con = db_connection(host=environ.get("db_host"),
                            database=environ.get("db_name"),
                            user=environ.get("db_user"),
                            port=environ.get("db_port"),
                            password=environ.get("db_psw"))
        cur = con.cursor()
        return con, cur
    except Exception as e:
        print(e)
        return None


def get_controller():
    connect, cursor = db_connect()
    cursor.execute(f"SELECT * FROM controller")
    return cursor.fetchall()[0][0]


def set_controller(value: int):
    connect, cursor = db_connect()
    cursor.execute(f"UPDATE controller SET enable={value}")
    connect.commit()
    cursor.close()
    connect.close()


def delete_user(user_id: int):
    connect, cursor = db_connect()
    cursor.execute(f"DELETE FROM users WHERE id={user_id}")
    connect.commit()
    cursor.close()
    connect.close()


def get_permissions(login: str):
    connect, cursor = db_connect()
    try:
        cursor.execute("""SELECT permissions FROM users WHERE login=%(login)s""", {"login": login})
        try:
            return cursor.fetchall()[0][0]
        except TypeError:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        connect.close()


def set_permissions(user_id: int, up: bool):
    connect, cursor = db_connect()
    try:
        cursor.execute(f"SELECT permissions FROM users WHERE id={user_id}")
        current_permissions = int(cursor.fetchall()[0][0])
        if up:
            if current_permissions >= 5:
                return current_permissions
            current_permissions += 1
        else:
            if current_permissions <= 0:
                return current_permissions
            current_permissions -= 1
        cursor.execute(f"UPDATE users SET permissions={current_permissions} WHERE id={user_id}")
        connect.commit()
        return current_permissions
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        connect.close()


def get_users():
    connect, cursor = db_connect()
    try:
        cursor.execute(f"SELECT * FROM users ORDER BY id")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        connect.close()


def check_password(login: str, password: str):
    connect, cursor = db_connect()
    try:
        cursor.execute("""SELECT password FROM users WHERE login=%(login)s""", {"login": login})
        try:
            db_password = cursor.fetchall()[0][0]
        except IndexError:
            return None
        if checkpw(password.encode("utf-8"), db_password.encode("utf-8")):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        connect.close()


def create_account(login: str, password: str, request: Request):
    connect, cursor = db_connect()
    try:
        agent = request.headers["user-agent"]
        cursor.execute(f"INSERT INTO users (login, password, useragent, permissions) VALUES (%(login)s, %(password)s,"
                       f"%(agent)s, 0)", {"login": login, "password": password, "agent": agent})
        connect.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()
