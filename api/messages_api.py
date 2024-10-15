import uvicorn
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from core.messages_entities import Message
from services.chat_service import ChatService
from adapters.network_adapter import send_message_to_network
from adapters.messages_adapter import save_message
from core.user_entities import User
from utils.auth_util import get_current_user

router = APIRouter()


@router.post("/send", response_class=HTMLResponse)
async def send_message(request: Request, current_user: User = Depends(get_current_user)):
    form = await request.form()

    username = current_user['username']
    message_content = form.get("message")

    message = Message(sender=current_user, content=message_content)

    send_message_to_network(message_content)
    save_message(message)

    it_hour_and_minute = message.timestamp.strftime('%H:%M:%S')

    return (f'<li class="bg-white rounded-lg p-4 m-4'
            f'shadow-sm transition duration-300 ease-in-out hover:shadow-md">'
            f'<em>{it_hour_and_minute}</em> | <strong>{username}:</strong> {message.content}</li>')


@router.get("/history", response_class=HTMLResponse)
async def get_history(current_user: User = Depends(get_current_user)):
    chat_service = ChatService(current_user)
    messages = chat_service.load_history()


    list_items = "".join(f"<li>{msg[0]}</li>" for msg in messages)

    response_html = f"<ul>{list_items}</ul>".strip().replace('"', ' ')
    return HTMLResponse(content=response_html)


def start_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
