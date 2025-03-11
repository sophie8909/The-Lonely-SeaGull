from models.services import UsersService
from views.loginView import LoginView
from controllers.base import BaseController

from tkinter import messagebox

def show_error_message(message):
    messagebox.showerror("Error", message)


class LoginController(BaseController):
    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        super().__init__(tk_root, current_language, current_resolution)

        self.tk_root.title("The Flying Dutchman Pub")
        self.tk_root.geometry("%dx%d" % (tk_root.winfo_screenwidth(), tk_root.winfo_screenheight()))

        self.users = UsersService('data/sample_users.json')
        self.frame = None
        self.main_controller = main_controller

    def create_login_widgets(self, current_language, current_resolution):
        self.frame = LoginView(self.tk_root, current_language, current_resolution)
        self.frame.pack(expand=True, fill='both')
        self.frame.settings_login_view()
        self.set_up_bind()

    def hide_login_widgets(self):
        self.frame.logout_button.grid_forget()

    def destroy_widgets(self):
        self.frame.destroy()
        self.frame = None

    def set_up_bind(self):
        self.frame.login_button.bind("<Button-1>", self.login_button_click)
        self.frame.password_entry.bind("<Return>", self.login_button_click)
        self.frame.guest_button.bind("<Button-1>", self.guest_button_click)
        self.frame.login_combo.bind("<<ComboboxSelected>>", self.main_controller.update_language)
        self.frame.res_combo.bind("<<ComboboxSelected>>", self.main_controller.change_res)

    def login_button_click(self, event):
        print("Login button clicked")
        username = self.frame.username_entry.get()
        password = self.frame.password_entry.get()
        success, message = self.login(username, password)
        if not success:
            show_error_message(message)
            return
        else:
            self.main_controller.switch_controller(self.main_controller.vip_controller)

    def guest_button_click(self, event):
        print("Continue as a guest button")
        self.main_controller.switch_controller(self.main_controller.customer_controller)

    def login(self, username, password):
        user = self.users.get_user(username)
        if user is None:
            return False, "User not found"
        if user.password != password:
            return False, "Incorrect password"
        self.main_controller.current_user = user
        return True, "Login success"


