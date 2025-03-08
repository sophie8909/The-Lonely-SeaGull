from models.services import UsersService
from views.loginView import LoginView
from controllers.base import BaseController

class LoginController(BaseController):
    def __init__(self, tk_root, main_controller, current_language):
        super().__init__(tk_root, current_language)
        self.users = UsersService('data/sample_users.json')
        self.frame = None
        self.main_controller = main_controller

    def create_widgets(self):
        self.frame = LoginView(self.tk_root, self.current_language)
        self.set_up_bind()
        self.frame.pack(expand=True, fill='both')

    def hide_widgets(self):
        self.frame.hide_widgets()

    def destroy_widgets(self):
        self.frame.destroy()
        self.frame = None

        
    def set_up_bind(self):
        self.frame.login_button.bind("<Button-1>", self.login_button_click)
        self.frame.password_entry.bind("<Return>", self.login_button_click)
        self.frame.guest_button.bind("<Button-1>", self.guest_button_click)


    def login_button_click(self, event):
        print("Login button clicked")
        username = self.frame.username_entry.get()
        password = self.frame.password_entry.get()
        success, message = self.login(username, password)
        if not success:
            self.frame.show_error_message(message)
            return
        else:
            self.main_controller.switch_controller(self.main_controller.vip_controller)

    def guest_button_click(self, event):
        print("Continue as a guest button")
        self.main_controller.switch_controller(self.main_controller.customer_controller)

    def login(self, username, password):
        user = self.users.get_user(username)
        if user is None:
            return (False, "User not found")
        if user.password != password:
            return (False, "Incorrect password")
        self.main_controller.current_user = user
        return (True, "Login success")

    def logout(self):
        self.main_controller.current_user = None
        return True