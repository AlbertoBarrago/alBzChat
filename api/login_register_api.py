import hashlib
from datetime import timedelta

from fastapi import Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi import APIRouter

from core.entities import UserLoggedIn
from services.user_service import login, register_user_call
from utils.auth_utils import create_access_token

router = APIRouter()

@router.post("/register")
async def register_user(username: str = Form(...), password: str = Form(...)):
    user_logged_in = UserLoggedIn(username=username, password=password)
    resp = register_user_call(user_logged_in)
    return resp['message']

@router.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...)):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    resp = login(username, hashed_password)
    if resp:
        access_token = create_access_token(
            data={"sub": username}, expires_delta=timedelta(hours=1)
        )
        return {"access_token": access_token, "token_type": "bearer", "message": HTMLResponse(content=resp['message'])}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")