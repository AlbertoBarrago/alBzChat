import uvicorn
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from services.chat_service import ChatService
from adapters.network_adapter import send_message_to_network
from adapters.messages_adapter import save_message
from core.entities import User, Message
from utils.auth_utils import get_current_user

router = APIRouter()


# POST /send endpoint
@router.post("/send", response_class=HTMLResponse)
async def send_message(request: Request, current_user: User = Depends(get_current_user)):
    form = await request.form()
    message_content = form.get("message")
    message = Message(sender=current_user, content=message_content)

    send_message_to_network(message_content)
    save_message(message, user=current_user)

    return (f'<li class="bg-white border border-gray-200 rounded-lg p-2 '
            f'shadow-sm transition duration-300 ease-in-out hover:shadow-md">'
            f'<strong>{current_user}:</strong> {message.content} <em>{message.timestamp}</em></li>')


# GET /history endpoint
@router.get("/history", response_class=HTMLResponse)
async def get_history(current_user: User = Depends(get_current_user)):
    chat_service = ChatService(current_user)
    messages = chat_service.load_history()

    list_items = "".join(f"<li>{msg}</li>" for msg in messages)
    response_html = f"<ul>{list_items}</ul>".strip().replace('"', ' ')
    return HTMLResponse(content=response_html)


def start_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
