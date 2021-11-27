from fastapi import Request
import psycopg2
import bcrypt


def db_connect():
    try:
        con = psycopg2.connect(host="ec2-34-254-120-2.eu-west-1.compute.amazonaws.com",
                               database="d1i4fejvtsp4ga",
                               user="pcihdikacxzpgs",
                               port=5432,
                               password="b80966adbbd1850e53829957e573f73b6cb81029d8a13a9eea88b11f6594f951")
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
        # cursor.execute("SELECT * FROM users")
        # print(cursor.fetchall())
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
            db_permissions = cursor.fetchall()[0][0]
        except TypeError:
            return None
        return db_permissions
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
