from fastapi import Form
from fastapi import APIRouter

from core.user_entities import User
from services.user_service import login, register_user_call

router = APIRouter()

@router.post("/register")
async def register_user(username: str = Form(...), password: str = Form(...)):
    user_logged_in = User(username=username, password=password)
    return register_user_call(user_logged_in)['message']

@router.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...)):
    user_logged_in = User(username=username, password=password)
    return login(user_logged_in)
