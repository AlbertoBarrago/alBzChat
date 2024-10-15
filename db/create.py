from mysql.connector import connect, Error
from dotenv import load_dotenv
import os

load_dotenv()

def create_database_and_table():
    connection = None
    cursor = None
    try:
        connection = connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        cursor = connection.cursor()

        cursor.execute('CREATE DATABASE IF NOT EXISTS CHAT_APP')

        cursor.execute('CREATE USER IF NOT EXISTS "alBz"@"localhost" IDENTIFIED BY "password"')

        cursor.execute('GRANT ALL PRIVILEGES ON CHAT_APP.* TO "alBz"@"localhost"')
        cursor.execute('FLUSH PRIVILEGES')

        cursor.execute('USE CHAT_APP')

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

    except Error as e:
        print(f"The error '{e}' occurred.")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def get_db_connection():
    connection = connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    return connection
