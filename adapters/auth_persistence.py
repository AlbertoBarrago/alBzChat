import hashlib

from core.entities import UserLoggedIn, User
from db.db import get_db_connection
from mysql.connector import Error

connection = get_db_connection()


def register_auth_persistence(user: UserLoggedIn):
    username = user.username
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    try:
        cursor = connection.cursor()
        check_query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(check_query, (user.username,))
        existing_user = cursor.fetchone()

        if existing_user:
            print("User already exists!")
            cursor.close()
            resp = {
                "user": None,
                "message": "User already exists!"
            }
            return resp


        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        connection.commit()

        print("User registered successfully.")
        resp = {
            "message": "User registered successfully.",
        }
        return resp
    except Error as e:
        print(f"The error '{e}' occurred")
        resp = {
            "message": f"The error '{e}' occurred",
        }
        return resp


def login_auth_persistence(user: UserLoggedIn):
    if connection is None:
        return False
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (user.username, hashed_password))
        user = cursor.fetchone()
        if user:
            print("Login successful!", user)
            resp = {
                "user": User(user[0]),
                "message": "Login Successful!",
            }
            return resp
    except Error as e:
        print(f"The error '{e}' occurred")
        resp = {
            "user": None,
            "message": "Login failed!",
        }
        return resp