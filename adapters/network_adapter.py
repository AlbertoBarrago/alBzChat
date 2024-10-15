import socket
from threading import Thread

from adapters.messages_adapter import save_message
from core.messages_entities import Message

HOST = 'localhost'
PORT = 65432

active_connections = []


def handle_client_connection(conn, addr):
    print(f"Connected by {addr}")
    active_connections.append(conn)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Connection closed by {addr}")
                break
            print(f"Received from {addr}: {data.decode('utf-8')}")
            broadcast_message(data, conn)
            conn.sendall(b'Message received great albZ')
    finally:
        conn.close()
        active_connections.remove(conn)


def broadcast_message(message: bytes, sender_conn):
    for conn in active_connections:
        if conn != sender_conn:
            try:
                conn.sendall(message)
            except Exception as e:
                print(f"Error sending message to a client: {e}")


def start_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Socket server started on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = Thread(target=handle_client_connection, args=(conn, addr))
            client_thread.start()


def send_message_to_network(message: str, message_dto: Message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode('utf-8'))
        data = s.recv(1024)
        save_message(message_dto)
    print('Server response:', data.decode('utf-8'))


if __name__ == '__main__':
    start_socket_server()
