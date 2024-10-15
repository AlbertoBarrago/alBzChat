from adapters.messages_adapter import load_messages
from core.user_entities import User


class ChatService:
    def __init__(self, user: User):
        self.user = user

    def load_history(self):
        return load_messages(self.user)
