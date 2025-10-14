from fastapi import FastAPI
from threading import Thread
from api.messages_api import start_fastapi
from adapters.network_adapter import start_socket_server
from api.home_api import router as home_router
from api.login_api import router as auth_router
from api.messages_api import router as message_router
from db.create import create_database_and_table
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(home_router)
app.include_router(auth_router, prefix="/auth")
app.include_router(message_router, prefix="/message")


def setup_database():
    """
    Ensures the database and tables are created before starting the app.
    """
    logger.info("Starting database initialization...")
    create_database_and_table()
    logger.info("Database initialization completed.")


if __name__ == "__main__":
    setup_database()

    logger.info("Starting WebSocket server thread...")
    socket_thread = Thread(target=start_socket_server, daemon=True)
    socket_thread.start()

    time.sleep(2)
    logger.info("WebSocket thread started")

    logger.info("Starting FastAPI server...")
    start_fastapi()