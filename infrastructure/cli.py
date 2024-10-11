from core.chat_service import ChatService
from core.entities import User


def start_chat():
    username = input("Enter your username: ")
    user = User(username=username)
    chat_service = ChatService(user)
    exit_chat = False

    while not exit_chat:  # Run while exit_chat is False
        command = input("Enter 'send' to send a message, 'history' to view chat history, or 'exit' to quit: ")

        if command == 'send':
            content = input("Enter your message: ")
            chat_service.send_message(content)
        elif command == 'history':
            messages = chat_service.load_history()
            for msg in messages:
                print(msg)
        elif command == 'exit':
            exit_chat = True
        else:
            print("Invalid command. Please enter 'send', 'history', or 'exit'.")
