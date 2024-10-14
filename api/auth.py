import hashlib

from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi import APIRouter

from services.user_service import login, register_user_call

router = APIRouter()

@router.post("/register")
async def register_user(username: str = Form(...), password: str = Form(...)):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    response = register_user_call(username, hashed_password)
    return response

@router.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...)):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    response = login(username, hashed_password)
    return HTMLResponse(content=response)