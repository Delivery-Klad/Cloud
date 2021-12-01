from fastapi import Request
import psycopg2
import bcrypt


def db_connect():
    try:
        con = psycopg2.connect(host="ec2-52-214-178-113.eu-west-1.compute.amazonaws.com",
                               database="d843ppmbnactup",
                               user="gdbusytrmyeoqa",
                               port=5432,
                               password="e01b3717ac9a5ec8a52d14f89c2483ace413784a7595d5338e72ab5701571c22")
        cur = con.cursor()
        return con, cur
    except Exception as e:
        print(e)
        return None


def create_tables():
    try:
        connect, cursor = db_connect()
        cursor.execute("CREATE TABLE IF NOT EXISTS users(id SERIAL NOT NULL UNIQUE PRIMARY KEY,"
                       "login TEXT NOT NULL UNIQUE,"
                       "password TEXT NOT NULL,"
                       "useragent TEXT NOT NULL,"
                       "permissions INT NOT NULL)")
        connect.commit()
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        connect.close()


def get_permissions(login: str):
    try:
        connect, cursor = db_connect()
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
    try:
        connect, cursor = db_connect()
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
    try:
        connect, cursor = db_connect()
        cursor.execute(f"SELECT * FROM users")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        connect.close()


def check_password(login: str, password: str):
    try:
        connect, cursor = db_connect()
        cursor.execute("""SELECT password FROM users WHERE login=%(login)s""", {"login": login})
        try:
            db_password = cursor.fetchall()[0][0]
        except IndexError:
            print("not found")
            return None
        if bcrypt.checkpw(password.encode("utf-8"), db_password.encode("utf-8")):
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
    try:
        connect, cursor = db_connect()
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
