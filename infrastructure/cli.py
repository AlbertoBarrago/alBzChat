from core.chat_service import ChatService
from core.entities import User

def start_chat():
    username = input("Enter your username: ")
    user = User(username=username)
    chat_service = ChatService(user)

    while True:
        command = input("Enter 'send' to send a message or 'history' to view chat history: ")

        if command == 'send':
            content = input("Enter your message: ")
            chat_service.send_message(content)
        elif command == 'history':
            messages = chat_service.load_history()
            for msg in messages:
                print(msg)
        elif command == 'exit':
            print("Exiting chat...")
            break
