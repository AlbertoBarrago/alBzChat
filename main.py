import socket
from datetime import datetime

from fastapi import FastAPI, Request, Form, HTTPException

from adapters.persistence import save_message
from core.chat_service import ChatService
from core.entities import User, Message
import uvicorn
from threading import Thread
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from adapters.network import start_socket_server, send_message_to_network

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

@app.post("/send", response_class=HTMLResponse)
async def send_message(request: Request):
    form = await request.form()
    message_content = form.get("message")
    sender = User("alBz")
    message = Message(sender, message_content)
    send_message_to_network(message_content)
    save_message(message)

    return f'<li class="bg-white border border-gray-200 rounded-lg p-2 shadow-sm transition duration-300 ease-in-out hover:shadow-md"><strong>{message.sender.username}:</strong> {message.content} <em>{message.timestamp}</em></li>'

@app.get("/history")
def get_history():
    messages = chat_service.load_history()
    list_items = "".join(f"<li>{msg}</li>" for msg in messages)
    response_html = f"<ul>{list_items}</ul>".strip().replace('"', ' ')
    return HTMLResponse(content=response_html)

def start_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    socket_thread = Thread(target=start_socket_server)
    socket_thread.start()

    start_fastapi()
