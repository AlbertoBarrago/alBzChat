""" List of Class Interface"""
from datetime import datetime

class User:
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return self.username


class UserLoggedIn(User):
    def __init__(self, username: str, password: str):
        super().__init__(username)
        self.password = password

    def __str__(self):
        return f'{self.username} {self.password}'

class Message:
    def __init__(self, sender: User, content: str, timestamp=None):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.now()

    def __str__(self):
        return f"[{self.timestamp}] {self.sender}: {self.content}"
