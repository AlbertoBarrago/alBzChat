import json
import asyncio
import websockets
from websockets import WebSocketServerProtocol

from adapters.messages_adapter import save_message
from core.messages_entities import Message
from core.user_entities import UserLoggedIn
import logging

HOST = 'localhost'
PORT = 65432

active_connections = set()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_client_connection(websocket: WebSocketServerProtocol, path: str) -> None:
    """Handle WebSocket connections"""
    logger.info(f"WebSocket connected by {websocket.remote_address}")
    active_connections.add(websocket)

    try:
        async for message in websocket:
            try:
                payload = json.loads(message)
                message_content = payload.get("content")
                sender_username = payload.get("user")

                if not message_content or not sender_username:
                    logger.warning("Invalid message format. Missing content or sender.")
                    continue

                logger.info(f"Received message from {sender_username}: {message_content}")

                from db.create import get_db_connection
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM users WHERE username = %s", (sender_username,))
                result = cursor.fetchone()

                if result:
                    user_id = result[0]
                    user_logged_in = UserLoggedIn(user_id=user_id, username=sender_username, password="")
                    message_dto = Message(sender=user_logged_in, content=message_content)

                    save_result = save_message(message_dto)
                    logger.info(f"Save result: {save_result}")

                    await broadcast_message(message, websocket)
                else:
                    logger.error(f"User {sender_username} not found in database")

                await websocket.send("Message received successfully.")

            except json.JSONDecodeError:
                logger.info(f"Received plain text message: {message}")
                plain_payload = json.dumps({
                    "user": "Anonymous",
                    "content": message
                })
                await broadcast_message(plain_payload, websocket)
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    except websockets.exceptions.ConnectionClosed:
        logger.info(f"WebSocket connection closed by {websocket.remote_address}")
    except Exception as e:
        logger.error(f"Error in handle_client_connection: {e}")
    finally:
        active_connections.discard(websocket)


async def broadcast_message(message: str, sender_websocket):
    """Broadcast message to all connected clients except sender"""
    if active_connections:
        logger.info(f"Broadcasting message: {message}")
        for websocket in active_connections.copy():
            if websocket != sender_websocket:
                try:
                    await websocket.send(message)
                    logger.info(f"Message sent to {websocket.remote_address}")
                except Exception as e:
                    logger.error(f"Error sending message to a client: {e}")
                    active_connections.discard(websocket)


def start_socket_server():
    """Start the WebSocket server"""
    try:
        logger.info(f"Starting WebSocket server on ws://{HOST}:{PORT}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        start_server = websockets.serve(handle_client_connection, HOST, PORT)
        loop.run_until_complete(start_server)

        logger.info(f"WebSocket server successfully started on ws://{HOST}:{PORT}")
        loop.run_forever()

    except Exception as e:
        logger.error(f"Failed to start WebSocket server: {e}")
        raise


def persist_message(message: str, message_dto: Message):
    """Send a message to a network-simplified version that just saves to DB"""
    logger.info(f"Saving message from {message_dto.sender.username}: {message}")
    save_message(message_dto)


if __name__ == '__main__':
    start_socket_server()