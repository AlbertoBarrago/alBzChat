import uvicorn
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse

from core.messages_entities import Message
from services.chat_service import ChatService
from adapters.network_adapter import send_message_to_network
from adapters.messages_adapter import get_new_messages, get_all_messages, delete_message
from core.user_entities import User
from services.message_service import make_call_and_handle_all_result, make_call_and_handle_result_history, \
    make_call_and_handle_result
from utils.auth_util import get_current_user

router = APIRouter()


@router.post("/messages")
async def get_messages(request: Request):
    body = await request.json()
    last_timestamp = body.get("last_timestamp", 0.0)
    response_json = await make_call_and_handle_all_result(last_timestamp)
    return HTMLResponse(content=response_json)

@router.get("/all-messages", response_class=HTMLResponse)
async def get_all_messages_endpoint(current_user: User = Depends(get_current_user)):
    """Get all messages for initial chat load"""
    response_html = await make_call_and_handle_result(get_all_messages)
    return HTMLResponse(content=response_html)


@router.post("/send", response_class=HTMLResponse)
async def send_message(request: Request, current_user: User = Depends(get_current_user)):
    form = await request.form()
    message_content = form.get("message")

    # CONTROLLA SE IL MESSAGGIO NON È VUOTO
    if message_content and message_content.strip():
        message = Message(sender=current_user, content=message_content)
        send_message_to_network(message_content, message)

    response_html = await make_call_and_handle_result(get_all_messages)
    return HTMLResponse(content=response_html)

@router.delete("/delete/{message_id}")
async def delete_message_endpoint(message_id: int, current_user: User = Depends(get_current_user)):
    """Delete a message (only if user owns it)"""
    user_id = current_user.id if hasattr(current_user, 'id') else current_user.user_id
    result = delete_message(message_id, user_id)
    return JSONResponse(content=result)


@router.get("/history", response_class=HTMLResponse)
async def get_history(current_user: User = Depends(get_current_user)):
    chat_service = ChatService(current_user)
    response_html = await make_call_and_handle_result_history(chat_service)
    return HTMLResponse(content=response_html)


def start_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
