from models.language import LANGUAGE
from models.services import UsersService
from views.loginView import LoginView
from controllers.base import BaseController

from tkinter import messagebox


class LoginController(BaseController):
    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        super().__init__(tk_root, current_language, current_resolution)

        # The geometry values might vary for different display sizes, but for a 15.6 inches
        # display should be on a perfect fullscreen
        self.tk_root.title("The Flying Dutchman Pub")
        self.tk_root.geometry(str(tk_root.winfo_screenwidth()) + "x" + str(tk_root.winfo_screenheight()-int(0.036*tk_root.winfo_screenheight())) + "+" + str(-int(0.005*tk_root.winfo_screenwidth())) + "+" + str(0))

        self.users = UsersService('data/sample_users.json')
        self.frame = None
        self.main_controller = main_controller

    def create_login_widgets(self, current_language, current_resolution):
        self.frame = LoginView(self.tk_root, current_language, current_resolution)
        self.frame.pack(expand=True, fill='both')
        self.set_up_bind()

    def hide_login_widgets(self):
        self.frame.settings_widget.logout_button.grid_forget()

    def destroy_widgets(self):
        self.frame.destroy()
        self.frame = None

    def set_up_bind(self):
        self.frame.login_button.bind("<Button-1>", self.login_button_click)
        self.frame.password_entry.bind("<Return>", self.login_button_click)
        self.frame.guest_button.bind("<Button-1>", self.guest_button_click)
        self.frame.settings_widget.login_combo.bind("<<ComboboxSelected>>", self.main_controller.update_language)
        self.frame.settings_widget.res_combo.bind("<<ComboboxSelected>>", self.main_controller.change_res)

    def login_button_click(self, event):
        print("Login button clicked")
        username = self.frame.username_entry.get()
        password = self.frame.password_entry.get()
        success, message = self.login(username, password)

        if not success:
            self.show_message(self, message, "ERROR")
            return
        else:
            self.show_message(self, message, "SUCCESS")
            if self.main_controller.current_user.credentials == 0:
                self.main_controller.switch_controller(self.main_controller.owner_controller)
            elif self.main_controller.current_user.credentials == 1:
                self.main_controller.switch_controller(self.main_controller.bartender_controller)
            elif self.main_controller.current_user.credentials == 2:
                self.main_controller.switch_controller(self.main_controller.vip_controller)

    def guest_button_click(self, event):
        print("Continue as guest button")
        self.main_controller.switch_controller(self.main_controller.customer_controller)

    def login(self, username, password):
        user = self.users.get_user(username)
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)

        if user is None:
            return False, LANGUAGE[language_window]["not_found"]
        if user.password != password:
            return False, LANGUAGE[language_window]["wrong_pass"]
        self.main_controller.current_user = user
        return True, LANGUAGE[language_window]["success"]

    @staticmethod
    def show_message(self, message, type):
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)

        if type == "ERROR":
            messagebox.showerror(LANGUAGE[language_window]["error"], message)
        elif type == "SUCCESS":
            messagebox.showinfo(LANGUAGE[language_window]["success"], message)
