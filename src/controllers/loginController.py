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

    def change_res_27(self, event):
        # global w,h,x,y
        screen_width = self.tk_root.winfo_screenwidth()
        screen_height = self.tk_root.winfo_screenheight()

        w = screen_width * 0.9
        h = screen_height * 0.9
        x = (screen_width / 2) - (w / 2)
        y = (screen_height / 2) - (h / 2)

        self.tk_root.geometry(str(int(w)) + "x" + str(int(h)) + "+" + str(int(x)) + "+" + str(int(y)))
        print("screen_width:", w)
        print("screen_height:", h)
        print("x:", x)
        print("y:", y)

    def change_res_9(self, event):
        # global w, h,x,y
        screen_width = self.tk_root.winfo_screenwidth()
        screen_height = self.tk_root.winfo_screenheight()

        w = screen_width  * 0.5
        h = screen_height * 0.5
        x = (screen_width/2) - (w/2)
        y = (screen_height/2) - (h/2)

        self.tk_root.geometry(str(int(w)) + "x" + str(int(h)) + "+" + str(int(x)) + "+" + str(int(y)))

        print("screen_width:", w)
        print("screen_height:", h)
        print("x:", x)
        print("y:", y)

        
    def set_up_bind(self):
        self.frame.login_button.bind("<Button-1>", self.login_button_click)
        self.frame.password_entry.bind("<Return>", self.login_button_click)
        self.frame.guest_button.bind("<Button-1>", self.guest_button_click)
        self.frame.button1.bind("<Button-1>", self.change_res_27)
        self.frame.button2.bind("<Button-1>", self.change_res_9)


    def login_button_click(self, event):
        print("Login button clicked")
        username = self.frame.username_entry.get()
        password = self.frame.password_entry.get()
        success, message = self.login(username, password)
        if not success:
            self.frame.show_error_message(message)
            return
        else:
            self.main_controller.switch_controller(self.main_controller.customer_controller)

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

    def logout(self):
        self.main_controller.current_user = None
        return True