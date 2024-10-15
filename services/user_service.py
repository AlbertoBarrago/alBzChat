from adapters.auth_adapter import register_auth_persistence, login_auth_persistence
from core.user_entities import UserLoggedIn, User


def register_user_call(user: User):
    """ Register new user if not exists"""
    return register_auth_persistence(user)


def login(user: User):
    """ Login User with user and password"""
    return login_auth_persistence(user)


