import os
import json
from core.entities import Message
from datetime import datetime

FILE_PATH = 'chat_history.json'

def save_message(message: Message):
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as file:
            json.dump([], file)

    with open(FILE_PATH, 'r+') as file:
        history = json.load(file)
        history.append({
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp.isoformat()
        })
        file.seek(0)
        json.dump(history, file)

def load_messages():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, 'r') as file:
        history = json.load(file)
        return [Message(sender=msg['sender'], content=msg['content'],
                        timestamp=datetime.fromisoformat(msg['timestamp']))
                for msg in history]
