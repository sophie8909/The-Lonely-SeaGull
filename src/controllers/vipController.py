from controllers.custormerController import CustomerController
from views.vipView import VIPView


class VIPController(CustomerController):
    def __init__(self, tk_root, main_controller, current_language):
        super().__init__(tk_root, main_controller, current_language)

    def create_vip_widgets(self):
        self.frame = VIPView(self.tk_root, self.current_language)
        self.frame.pack(expand=True, fill='both')
        self.customer_view_setup()

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    controller = CustomerController(root, None, "English")
    controller.create_customer_widgets()
    root.mainloop()
