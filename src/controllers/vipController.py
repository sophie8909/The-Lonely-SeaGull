# =============================================================================
# vipController.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Controller for the VIP user view and model
# =======================================================

# Import the necessary libraries
from random import randint

# Local imports
from controllers.custormerController import CustomerController
from views.vipView import VIPView
from models.menu import menu

class VIPController(CustomerController):
    """ The VIP controller class

        Specific methods available for the VIP user controller.

        Attributes:
            CustomerController: the inherited class CustomerController
    """

    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        """ Initial method

            Args:
                tk_root: used to get the root tk window
                main_controller: used to get the main controller
                current_language: used to get the current language of the system
                current_resolution: used to get the current resolution of the window
        """

        super().__init__(tk_root, main_controller, current_language, current_resolution) # inherit from CustomerController

    def create_vip_widgets(self, current_language, current_resolution):
        self.frame = VIPView(self.tk_root, current_language, current_resolution)
        self.frame.pack(expand=True, fill='both')

        self.customer_view_setup() # add the setup from CustomerController
        self.vip_view_setup()
    
    def vip_view_setup(self):
        """ Set up the VIP view """

        self.frame.name_label.config(text=self.main_controller.current_user.first_name + " " + self.main_controller.current_user.last_name)
        self.frame.vip_balance_amount_label.config(text=self.main_controller.current_user.balance)
        self.frame.add_to_balance_button.config(command=self.add_to_balance)
        self.frame.get_vip_code_button.config(command=self.get_vip_code)

    def add_to_balance(self):
        """ Add an X amount to account balance """
        self.main_controller.current_user.balance += 100
        self.frame.vip_balance_amount_label.config(text=self.main_controller.current_user.balance) # modify the label visually

    def load_menu(self):
        self.menu_list = menu

    def get_vip_code(self):
        """ Get the vip code """
        self.main_controller.current_user.balance -= 100 # Subtract from the current account balance, as you made a purchase from the
        # account balance
        self.frame.vip_balance_amount_label.config(text=self.main_controller.current_user.balance)
        self.frame.vip_code.config(text=randint(10000, 99999)) # generate a random number of 5 digits for the code
        # modify the label visually

# Main function that can be used to run this .py file individually to test some functionalities
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    controller = VIPController(root, None, "English")
    controller.create_vip_widgets()
    root.mainloop()
