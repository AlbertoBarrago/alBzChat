from adapters.auth_adapter import register_auth_persistence, login_auth_persistence
from core.user_entities import User


def register_user_impl(user: User):
    """
    Registers a new user
    :param user:
    :return:
    """
    return register_auth_persistence(user)


def login_impl(user: User):
    """ Login User with user and password"""
    return login_auth_persistence(user)


