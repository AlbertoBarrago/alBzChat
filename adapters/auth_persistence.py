""" Impl of persistence services"""
import hashlib
from datetime import timedelta

from fastapi import HTTPException
from starlette.responses import HTMLResponse

from core.entities import UserLoggedIn, User
from db.db import get_db_connection
from mysql.connector import Error

from utils.auth_utils import create_access_token

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

        user_model = {
            "user": User(user[0]),
            "message": "Login Successful!",
        }
        if user_model:
            access_token = create_access_token(
                data={"sub": user_model['user'].username}, expires_delta=timedelta(hours=1)
            )
            return {"access_token": access_token,
                    "token_type": "bearer",
                    "message": HTMLResponse(content=user_model['message'])
                    }
        else:
            return {
                "message": HTTPException(status_code=401, detail="Invalid credentials")
            }
    except Error as e:
        print(f"The error '{e}' occurred")
        resp = {
            "user": None,
            "message": "Login failed!",
        }
        return resp