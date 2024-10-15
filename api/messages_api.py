import uvicorn
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from core.messages_entities import Message
from services.chat_service import ChatService
from adapters.network_adapter import send_message_to_network
from adapters.messages_adapter import save_message, get_all_messages
from core.user_entities import User
from utils.auth_util import get_current_user

router = APIRouter()


@router.post("/send", response_class=HTMLResponse)
async def send_message(request: Request, current_user: User = Depends(get_current_user)):
    form = await request.form()

    username = current_user['username']
    message_content = form.get("message")

    message = Message(sender=current_user, content=message_content)
    send_message_to_network(message_content, message)

    # TODO: Add get message from the others users

    resp = get_all_messages()
    formatted_messages = []
    print(resp)
    for el in resp:
        message_data = {
            'message': el[0],
            'ddateTime': el[1].strftime('%H:%M:%S'),
            'sender': el[2],
        }
        formatted_messages.append(message_data)

    list_items = "".join(
        f"<li class='bg-white rounded-lg p-4 m-4 shadow-sm transition duration-300 ease-in-out hover:shadow-md'>"
        f"{msg['ddateTime']} - {msg['sender']}: <b>{msg['message']}</b></li>" for msg in formatted_messages)

    response_html = f"<ul>{list_items}</ul>"
    return HTMLResponse(content=response_html)


@router.get("/history", response_class=HTMLResponse)
async def get_history(current_user: User = Depends(get_current_user)):
    chat_service = ChatService(current_user)
    messages = chat_service.load_history()

    formatted_messages = []
    for el in messages:
        message_data = {
            'ddateTime': el[1].strftime('%H:%M:%S'),
            'message': el[0]
        }
        formatted_messages.append(message_data)

    list_items = "".join(f"<li>{msg['ddateTime']}: <b>{msg['message']}</b></li>" for msg in formatted_messages)

    response_html = f"<ul>{list_items}</ul>"
    return HTMLResponse(content=response_html)


def start_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
