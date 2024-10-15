""" Impl of persistence services"""
import hashlib
from datetime import timedelta

from fastapi import HTTPException
from core.user_entities import UserLoggedIn, User
from db.create import get_db_connection
from mysql.connector import Error

from utils.auth_util import create_access_token

connection = get_db_connection()


def register_auth_persistence(user: User):
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


def login_auth_persistence(user: User):
    if connection is None:
        return {"message": "Database connection is not established."}

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    try:
        cursor = connection.cursor()
        query = "SELECT id, username FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (user.username, hashed_password))
        result = cursor.fetchone()
        print(result)
        if result:
            access_token = create_access_token(
                data={"user_id": result[0], "username": result[1]}, expires_delta=timedelta(hours=1)
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "message": "Login Successful!"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    except Error as e:
        print(f"The error '{e}' occurred")
        return {
            "user": None,
            "message": "Login failed!"
        }
