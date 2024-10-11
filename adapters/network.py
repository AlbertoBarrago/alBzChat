import socket
from threading import Thread

HOST = 'localhost'
PORT = 65432

def handle_client_connection(conn, addr):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            print(f"Connection closed by {addr}")
            break
        print(f"Received: {data.decode('utf-8')}")
        conn.sendall(b'Message received')
    conn.close()

def start_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Socket server started on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = Thread(target=handle_client_connection, args=(conn, addr))
            client_thread.start()

def send_message_to_network(message: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode('utf-8'))
        data = s.recv(1024)
    print('Server response:', data.decode('utf-8'))
