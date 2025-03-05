from controllers.base import BaseController
from views.customerView import CustomerView


class CustomerController(BaseController):
    def __init__(self, root, current_language):
        super().__init__(root, current_language)
        self.frame = CustomerView(root, current_language)
        self.shopping_cart = None
        self.order_history = []
        self.redo_stack = []
        self.ordered_list = []