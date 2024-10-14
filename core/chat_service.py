from mysql.connector import Error
from db.db import get_db_connection
from adapters.network import send_message_to_network
from adapters.persistence import save_message, load_messages
from core.entities import User, Message
import hashlib


def register_user_call(username, password):
    connection = get_db_connection()
    if connection is None:
        return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the password
    try:
        cursor = connection.cursor()  # Create a single cursor
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        connection.commit()
        cursor.close()
        print("User registered successfully.")
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        connection.close()


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
            print("Login successful!")
            return "Login successful!"
    except Error as e:
        print(f"The error '{e}' occurred")
        return "Login failed"


class ChatService:
    def __init__(self, user: User):
        self.user = user

    def send_message(self, content: str):
        message = Message(sender=self.user, content=content)
        save_message(message)
        send_message_to_network(str(message))

    def load_history(self):
        print("Charge history user:", self.user.username)
        return load_messages()
