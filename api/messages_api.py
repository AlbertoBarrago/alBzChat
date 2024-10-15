import uvicorn
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from core.messages_entities import Message
from services.chat_service import ChatService
from adapters.network_adapter import send_message_to_network
from adapters.messages_adapter import get_all_messages
from core.user_entities import User
from services.message_service import make_call_and_handle_result, make_call_and_handle_result_history
from utils.auth_util import get_current_user

router = APIRouter()


@router.post("/send", response_class=HTMLResponse)
async def send_message(request: Request, current_user: User = Depends(get_current_user)):
    form = await request.form()

    message_content = form.get("message")

    message = Message(sender=current_user, content=message_content)
    send_message_to_network(message_content, message)

    response_html = await make_call_and_handle_result(get_all_messages)
    return HTMLResponse(content=response_html)


@router.get("/history", response_class=HTMLResponse)
async def get_history(current_user: User = Depends(get_current_user)):
    chat_service = ChatService(current_user)
    response_html = await make_call_and_handle_result_history(chat_service)
    return HTMLResponse(content=response_html)


def start_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
