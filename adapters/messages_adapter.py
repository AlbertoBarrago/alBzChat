import os
import json

from core.messages_entities import Message
from core.user_entities import User
from datetime import datetime
from db.create import get_db_connection

connection = get_db_connection()

FILE_PATH = 'chat_history.json'


def save_message(message: Message, user: User):
    """ Persist message on db """
    print(message, user)
    try:
        cursor = connection.cursor()
        query = "INSERT INTO messages (user_id, content) VALUES (%s, %s)"
        cursor.execute(query, (user, message))
        operation = cursor.lastrowid
        if operation:
            print(operation)
        connection.commit()
        resp = {
            "message": "Message stored"
        }
        return resp
    except Exception as e:
        print(f"The error '{e}' occurred")
        resp = {
            "message": f"The error '{e}' occurred",
        }
        return resp


def load_messages(user: User):
    # TODO: retrieve message after make the call
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, 'r') as file:
        history = json.load(file)
        return [Message(sender=msg['sender'], content=msg['content'],
                        timestamp=datetime.fromisoformat(msg['timestamp']))
                for msg in history]
