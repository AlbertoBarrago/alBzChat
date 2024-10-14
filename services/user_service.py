import hashlib
from mysql.connector import Error

from adapters.auth_persistence import register_auth_persistence
from core.entities import User, UserLoggedIn
from db.db import get_db_connection


def register_user_call(user: UserLoggedIn):
    return register_auth_persistence(user)

def login(username, hashed_password):
    connection = get_db_connection()
    if connection is None:
        return False
    hashed_password = hashlib.sha256(hashed_password.encode()).hexdigest()
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))
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