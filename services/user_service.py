from datetime import timedelta

from fastapi import HTTPException
from starlette.responses import HTMLResponse

from adapters.auth_adapter import register_auth_persistence, login_auth_persistence
from core.entities import UserLoggedIn
from utils.auth_util import create_access_token


def register_user_call(user: UserLoggedIn):
    """ Register new user if not exists"""
    return register_auth_persistence(user)


def login(user: UserLoggedIn):
    """ Login User with user and password"""
    return login_auth_persistence(user)


