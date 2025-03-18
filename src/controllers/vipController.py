from controllers.custormerController import CustomerController
from views.vipView import VIPView
from models.menu import menu


class VIPController(CustomerController):
    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        super().__init__(tk_root, main_controller, current_language, current_resolution)

    def create_vip_widgets(self, current_language, current_resolution):
        self.frame = VIPView(self.tk_root, current_language, current_resolution)
        self.frame.pack(expand=True, fill='both')
        self.customer_view_setup()
        self.vip_view_setup()
    
    def vip_view_setup(self):
        self.frame.name_label.config(text=self.main_controller.current_user.first_name + " " + self.main_controller.current_user.last_name)
        self.frame.vip_balance_amount_label.config(text=self.main_controller.current_user.balance)
        self.frame.add_to_balance_button.config(command=self.add_to_balance)

    def add_to_balance(self):
        self.main_controller.current_user.balance += 100
        self.frame.vip_balance_amount_label.config(text=self.main_controller.current_user.balance)

    def load_menu(self):
        self.menu_list = menu


if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    controller = VIPController(root, None, "English")
    controller.create_vip_widgets()
    root.mainloop()
