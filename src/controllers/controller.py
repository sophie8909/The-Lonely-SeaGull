# Controller.py
import tkinter as tk
import src.models.language
from src.controllers.base import BaseController
from src.controllers.custormerController import CustomerController



class Controller(BaseController):
    def __init__(self, current_language):
        super().__init__(current_language)
        self.customer_controller = CustomerController()
        pass


if __name__ == "__main__":
    root = tk.Tk()
    controller = Controller(root)
    root.mainloop()