from controllers.base import BaseController
from views.customerView import CustomerView


class CustomerController(BaseController):
    def __init__(self, tk_root, main_controller, current_language):
        super().__init__(tk_root, current_language)
        self.frame = None
        self.shopping_cart = None
        self.order_history = []
        self.redo_stack = []
        self.ordered_list = []
    
    def create_widgets(self):
        self.frame = CustomerView(self.tk_root, self.current_language)
        self.frame.pack(expand=True, fill='both')

    def destroy_widgets(self):
        self.frame.destroy()
        self.frame = None

    