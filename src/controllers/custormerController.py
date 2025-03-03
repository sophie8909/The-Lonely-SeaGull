from src.views.customerView import CustomerView

class CustomerController:
    def __init__(self, language, current_language):
        self.frame = CustomerView(self, language, current_language)
        self.shopping_cart = None
        self.language = language
        self.current_language = current_language
        self.order_history = []
        self.redo_stack = []
        self.ordered_list = []