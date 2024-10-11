import socket

from fastapi import FastAPI, Request, Form
from core.chat_service import ChatService
from core.entities import User
import uvicorn
from threading import Thread
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from adapters.network import start_socket_server

HOST = 'localhost'
PORT = 65432

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

current_user = User(username="alBz")
chat_service = ChatService(current_user)

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send")
async def send_message(request: Request, message: str = Form(...)):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode('utf-8'))
        data = s.recv(1024)

    chat_service.send_message(message)
    return {"response": data.decode('utf-8')}

@app.get("/history")
def get_history():
    messages = chat_service.load_history()
    return {"history": [str(msg) for msg in messages]}

def start_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    socket_thread = Thread(target=start_socket_server)
    socket_thread.start()

    start_fastapi()
