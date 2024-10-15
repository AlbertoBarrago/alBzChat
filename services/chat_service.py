from adapters.network_adapter import send_message_to_network
from adapters.messages_adapter import save_message, load_messages
from core.messages_entities import Message
from core.user_entities import User


class ChatService:
    def __init__(self, user: User):
        self.user = user

    def send_message(self, content: str):
        message = Message(sender=self.user, content=content)
        save_message(message, self.user)
        send_message_to_network(str(message))

    def load_history(self):
        return load_messages(self.user)
