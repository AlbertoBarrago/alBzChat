from datetime import datetime

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Message:
    def __init__(self, sender: User, content: str, timestamp = None):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.now()


    def __str__(self):
        return f"[{self.timestamp}] {self.sender}: {self.content}"
