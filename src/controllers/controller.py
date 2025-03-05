# Controller.py
import tkinter as tk
import models.language
from controllers.base import BaseController
from controllers.custormerController import CustomerController
from controllers.loginController import LoginController


class Controller(BaseController):
    def __init__(self, root, current_language):
        super().__init__(root, current_language)
        self.root.title("Customer Ordering Interface")
        self.root.geometry("1920x1280")
        self.customer_controller = CustomerController(root, current_language)
        self.login_controller = LoginController(root, current_language)
        self.login_controller.frame.pack()
        # self.customer_controller.frame.pack()
        pass


if __name__ == "__main__":
    root = tk.Tk()
    controller = Controller(root)
    root.mainloop()