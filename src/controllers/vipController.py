from controllers.base import BaseController
from views.customerView import CustomerView
from views.vipView import VIPView
from controllers.custormerController import CustomerController

class VIPController(CustomerController):
    def __init__(self, tk_root, main_controller, current_language):
        super().__init__(tk_root, main_controller, current_language)

    def create_widgets(self):
        self.frame = VIPView(self.tk_root, self.current_language)
        self.frame.pack(expand=True, fill='both')
        self.customer_view_setup()

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    controller = CustomerController(root, None, "English")
    controller.create_widgets()
    root.mainloop()