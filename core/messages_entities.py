""" List of Class Interface for Messages"""
from datetime import datetime
from core.user_entities import User


class Message:
    def __init__(self, sender: User, content: str, timestamp=None):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.now()

    def __str__(self):
        return f"[{self.timestamp}] {self.sender}: {self.content}"
