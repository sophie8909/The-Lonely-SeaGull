from controllers.base import BaseController
from views.customerView import CustomerView
from views.vipView import VIPView
from controllers.custormerController import CustomerController

class VIPController(CustomerController):
    def __init__(self, tk_root, main_controller, current_language):
        super().__init__(tk_root, main_controller, current_language)
