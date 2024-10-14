from adapters.auth_persistence import register_auth_persistence, login_auth_persistence
from core.entities import UserLoggedIn

def register_user_call(user: UserLoggedIn):
    """ Register new user if not exists"""
    return register_auth_persistence(user)

def login(user: UserLoggedIn):
   """ Login User with user and password"""
   return login_auth_persistence(user)