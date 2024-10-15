""" List of Class Interface for Users"""

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __getitem__(self, key):
        return getattr(self, key)


class UserLoggedIn(User):
    def __init__(self, user_id: int, username: str, password: str):
        super().__init__(username, password)
        self.id = user_id

    def __getitem__(self, key):
        return getattr(self, key)

