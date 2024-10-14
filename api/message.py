import uvicorn
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from services.chat_service import ChatService
from adapters.network import send_message_to_network
from adapters.persistence import save_message
from core.entities import User, Message

current_user = User(username="alBz", password="<PASSWORD>")
chat_service = ChatService(current_user)

router = APIRouter()
@router.post("/send", response_class=HTMLResponse)
async def send_message(request: Request):
    form = await request.form()
    message_content = form.get("message")
    sender = User("alBz", "<PASSWORD>")
    message = Message(sender, message_content)
    send_message_to_network(message_content)
    save_message(message)

    return f'<li class="bg-white border border-gray-200 rounded-lg p-2 shadow-sm transition duration-300 ease-in-out hover:shadow-md"><strong>{message.sender.username}:</strong> {message.content} <em>{message.timestamp}</em></li>'

@router.get("/history")
def get_history():
    messages = chat_service.load_history()
    list_items = "".join(f"<li>{msg}</li>" for msg in messages)
    response_html = f"<ul>{list_items}</ul>".strip().replace('"', ' ')
    return HTMLResponse(content=response_html)

def start_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)