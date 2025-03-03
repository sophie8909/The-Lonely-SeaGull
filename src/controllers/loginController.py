from src.models.services import UsersService
from src.views.loginView import LoginView
from src.controllers.base import BaseController

class LoginController(BaseController):
    def __init__(self):
        super().__init__()
        self.users = UsersService()
        self.frame = [LoginView(self)]

    def login(self, username, password):
        # Do something
        return True

    def logout(self):
        # Do something
        return True