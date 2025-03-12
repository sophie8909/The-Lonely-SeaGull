from controllers.custormerController import CustomerController

class VIPController(CustomerController):
    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        super().__init__(tk_root, main_controller, current_language, current_resolution)
