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

        # Create database if it doesn't exist
        cursor.execute('CREATE DATABASE IF NOT EXISTS CHAT_APP')

        # Create user if it doesn't exist
        cursor.execute('CREATE USER IF NOT EXISTS "alBz"@"localhost" IDENTIFIED BY "password"')

        # Grant privileges to the user
        cursor.execute('GRANT ALL PRIVILEGES ON CHAT_APP.* TO "alBz"@"localhost"')
        cursor.execute('FLUSH PRIVILEGES')

        # Use the new database
        cursor.execute('USE CHAT_APP')

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        print("Database and tables created successfully")
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
    print("Database and tables connect successfully")
    return connection
