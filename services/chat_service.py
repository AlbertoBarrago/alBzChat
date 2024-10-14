from adapters.network import send_message_to_network
from adapters.persistence import save_message, load_messages
from core.entities import User, Message

#TODO User db

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
