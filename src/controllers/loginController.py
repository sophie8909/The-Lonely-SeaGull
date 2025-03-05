# from models.services import UsersService
from views.loginView import LoginView
from controllers.base import BaseController

class LoginController(BaseController):
    def __init__(self, root, current_language):
        super().__init__(root, current_language)
        # self.users = UsersService()
        self.frame = LoginView(root, current_language)

    def login(self, username, password):
        # Do something
        return True

    def logout(self):
        # Do something
        return True