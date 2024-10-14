from fastapi import FastAPI
from api.message import start_fastapi
from threading import Thread
from adapters.network import start_socket_server
from api.home import router as home_router
from api.auth import router as auth_router
from api.message import router as message_router

app = FastAPI()

app.include_router(home_router)
app.include_router(auth_router, prefix="/auth")
app.include_router(message_router, prefix="/message")


if __name__ == "__main__":
    socket_thread = Thread(target=start_socket_server)
    socket_thread.start() #Start socker

    start_fastapi() #Start Fastapi

