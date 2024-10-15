from fastapi import FastAPI
from api.messages_api import start_fastapi
from threading import Thread
from adapters.network_adapter import start_socket_server
from api.home_api import router as home_router
from api.login_api import router as auth_router
from api.messages_api import router as message_router

app = FastAPI()

app.include_router(home_router)
app.include_router(auth_router, prefix="/auth")
app.include_router(message_router, prefix="/message")


if __name__ == "__main__":
    socket_thread = Thread(target=start_socket_server)
    socket_thread.start()

    start_fastapi()

