import os
import json
from core.entities import Message, User
from datetime import datetime

FILE_PATH = 'chat_history.json'

def save_message(message: Message, user: User):
    """ Persist message on db """
    print(message, user)
    pass



def load_messages(user: User):
    # TODO: retrieve message after make the call
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, 'r') as file:
        history = json.load(file)
        return [Message(sender=msg['sender'], content=msg['content'],
                        timestamp=datetime.fromisoformat(msg['timestamp']))
                for msg in history]
