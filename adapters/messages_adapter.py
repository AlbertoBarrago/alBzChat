from core.messages_entities import Message
from core.user_entities import User
from db.create import get_db_connection


FILE_PATH = 'chat_history.json'


def save_message(message: Message):
    """ Persist the message on db """
    connection = get_db_connection()

    # Handle different user object types
    sender = message['sender']
    if hasattr(sender, 'id'):
        user_id = sender.id
    elif hasattr(sender, 'user_id'):
        user_id = sender.user_id
    else:
        user_id = sender['user_id']  # Fallback for dict access

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
    connection = get_db_connection()
    # Handle both UserLoggedIn (has 'id') and regular dict (has 'user_id')
    if hasattr(user, 'id'):
        id_request = user.id
    elif hasattr(user, 'user_id'):
        id_request = user.user_id
    else:
        id_request = user['user_id']  # Fallback for dict access

    try:
        cursor = connection.cursor()
        query = "SELECT content, timestamp FROM messages WHERE user_id = %s ORDER BY id DESC;"
        cursor.execute(query, (id_request,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")
        return []


def get_all_messages():
    connection = get_db_connection()
    """ Get all messages from db for chat user """
    try:
        cursor = connection.cursor()
        query = """
                  SELECT messages.id, messages.content, messages.timestamp, users.username, messages.user_id
                  FROM messages
                  JOIN users ON messages.user_id = users.id
                  ORDER BY messages.id ASC;
              """
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")
        return []


def get_new_messages(last_timestamp: float):
    connection = get_db_connection()
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


def delete_message(message_id: int, user_id: int):
    """ Delete a message from db (only if user owns it) """
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = "DELETE FROM messages WHERE id = %s AND user_id = %s"
        cursor.execute(query, (message_id, user_id))
        connection.commit()

        if cursor.rowcount > 0:
            return {"success": True, "message": "Message deleted"}
        else:
            return {"success": False, "message": "Message not found or not yours"}
    except Exception as e:
        print(f"The error '{e}' occurred")
        return {"success": False, "message": f"Error: {e}"}
