from cryptography.fernet import Fernet

def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

def encrypt_message(message: str) -> bytes:
    key = load_key()
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes) -> str:
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()
