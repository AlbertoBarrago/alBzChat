from core.messages_entities import Message
from core.user_entities import User
from db.create import get_db_connection

connection = get_db_connection()

FILE_PATH = 'chat_history.json'


def save_message(message: Message):
    """ Persist message on db """
    user_id = message['sender']['user_id']
    message_content = message['content']
    try:
        cursor = connection.cursor()
        query = "INSERT INTO messages (user_id, content) VALUES (%s, %s)"
        cursor.execute(query, (user_id, message_content))
        connection.commit()
        resp = {
            "message": "Message stored"
        }
        return resp
    except Exception as e:
        print(f"The error '{e}' occurred")
        resp = {
            "message": f"The error '{e}' occurred",
        }
        return resp


def load_messages(user: User):
    """ Load messages from db """
    id_request = user['user_id']
    try:
        cursor = connection.cursor()
        query = "SELECT content, timestamp FROM messages WHERE user_id = %s ORDER BY id DESC;"
        cursor.execute(query, (id_request,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")


def get_all_messages():
    """ Get all messages from db for chat user """
    try:
        cursor = connection.cursor()
        query = """
                  SELECT messages.content, messages.timestamp, users.username
                  FROM messages
                  JOIN users ON messages.user_id = users.id
                  ORDER BY messages.id DESC;
              """
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")


def get_new_messages(last_timestamp: float):
    """Get only new messages from the database after the provided timestamp."""
    try:
        cursor = connection.cursor()
        query = """
            SELECT messages.content, messages.timestamp, users.username
            FROM messages
            JOIN users ON messages.user_id = users.id
            WHERE messages.timestamp > %s
            ORDER BY messages.id;
        """
        cursor.execute(query, (last_timestamp,))
        result = cursor.fetchall()

        messages = [
            {"content": row[0], "timestamp": row[1], "username": row[2]}
            for row in result
        ]
        return messages
    except Exception as e:
        print(f"The error '{e}' occurred")
        return []
