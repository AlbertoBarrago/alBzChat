import os
from mysql.connector import connect, Error
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def create_database_and_table():
    """
    Create a database and required tables if they do not exist.
    """
    connection = None
    cursor = None

    try:
        connection = connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        logging.info("Database connection established successfully.")

        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS CHAT_APP")
        logging.info("Database 'CHAT_APP' created or already exists.")

        cursor.execute('CREATE USER IF NOT EXISTS "alBz"@"localhost" IDENTIFIED BY "password"')
        cursor.execute('GRANT ALL PRIVILEGES ON CHAT_APP.* TO "alBz"@"localhost"')
        cursor.execute("FLUSH PRIVILEGES")
        logging.info("User 'alBz' with privileges is created or already exists.")

        cursor.execute("USE CHAT_APP")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        logging.info("Table 'users' created or already exists.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        logging.info("Table 'messages' created or already exists.")

    except Error as e:
        logging.error(f"An error occurred while setting up the database and tables: {e}")
    finally:
        if cursor is not None:
            cursor.close()
            logging.info("Database cursor closed.")
        if connection is not None:
            connection.close()
            logging.info("Database connection closed.")

def get_db_connection():
    connection = connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    return connection
