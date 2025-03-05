# Controller.py
import tkinter as tk
import models.language
from controllers.base import BaseController
from controllers.custormerController import CustomerController
from controllers.loginController import LoginController
from time import sleep

class MainController(BaseController):
    def __init__(self, tk_root, current_language):
        super().__init__(tk_root, current_language)
        self.tk_root.title("Customer Ordering Interface")
        self.tk_root.geometry("1920x1280")
        self.customer_controller = CustomerController(tk_root, self, current_language)
        self.login_controller = LoginController(tk_root, self, current_language)
        self.current_controller = self.login_controller
        self.current_controller.create_widgets()

        self.current_user = None
    

    def switch_controller(self, new_controller):
        print("Switching controller")
        if self.current_controller:
            print("Hiding current controller")
            self.current_controller.destroy_widgets()
        self.current_controller = new_controller
        self.current_controller.create_widgets()
    

if __name__ == "__main__":
    root = tk.Tk()
    controller = MainController(root)
    root.mainloop()