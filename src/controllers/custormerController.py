# =============================================================================
# bartenderController.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Controller for the customer user view and model
# =======================================================

# Import the necessary libraries
from typing import List
from copy import deepcopy

# Local imports
from controllers.base import BaseController
from views.customerView import CustomerView
from models.menu import menu
from models.filters import allergens_dict, beverage_filter_data
from models.language import LANGUAGE
from models.models import CustomerControllerData

class CustomerController(BaseController):
    """ The bartender controller class

        Specific methods available for the customer user controller.
    
        Attributes:
            BaseController: the inherited class BaseController
    """
    
    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        """ Initial method

           Args:
               tk_root: used to get the root tk window
               main_controller: used to get the main controller
               current_language: used to get the current language of the system
               current_resolution: used to get the current resolution of the window
       """
        
        super().__init__(tk_root, current_language, current_resolution) # inherit from BaseController

        self.frame = None
        # Constructor that interacts with the Customer data model
        self.data = CustomerControllerData(person_count=1, current_person=0, shopping_cart=[[]])
        self.undo_stack: List[CustomerControllerData] = []
        self.redo_stack: List[CustomerControllerData] = []
        self.order_history = []

        self.main_controller = main_controller
        self.current_language = current_language
        self.tk_root = tk_root

        self.allergens_dict = allergens_dict
        self.beverage_filter_data = beverage_filter_data

        self.current_menu = LANGUAGE[self.current_language]["beverages"]

    def customer_view_setup(self):
        """ Set up the customer view """

        self.frame.shopping_cart_widget.set_on_drop(self.add_cart_item)
        self.frame.shopping_cart_widget.set_current_person_command(self.set_current_person)
        self.frame.shopping_cart_widget.set_remove_person_command(self.remove_person)
        self.frame.shopping_cart_widget.add_friends_btn.config(command=self.add_person)
        self.frame.shopping_cart_widget.confirm_btn.config(command=self.confirm_order)
        self.frame.shopping_cart_widget.undo_btn.config(command=self.undo)
        self.frame.shopping_cart_widget.redo_btn.config(command=self.redo)
        self.frame.search_button.config(command=self.search_product)
        self.frame.beverages_button.config(command=lambda: self.switch_menu(LANGUAGE[self.current_language]["beverages"]))
        self.frame.food_button.config(command=lambda: self.switch_menu(LANGUAGE[self.current_language]["food"]))

        # added also key shortcuts for the undo/redo functionalities
        self.tk_root.bind('<Control-z>', lambda event: self.undo())
        self.tk_root.bind('<Control-y>', lambda event: self.redo())
        self.tk_root.bind("<Return>", lambda event: self.search_product())
        self.frame.settings_widget.logout_button.bind("<Button-1>", self.main_controller.logout_button_click)
        self.frame.settings_widget.login_combo.bind("<<ComboboxSelected>>", self.main_controller.update_language)
        self.frame.settings_widget.res_combo.bind("<<ComboboxSelected>>", self.main_controller.change_res)

        # fetch data from the database and update the view
        self.load_menu()
        self.update_menu()
        self.update_cart()

    def create_customer_widgets(self, current_lng, current_res):
        """ Create custom widgets """
        self.frame = CustomerView(self.tk_root, current_lng, current_res)
        self.frame.pack(expand=True, fill='both')

        self.customer_view_setup()

    def destroy_widgets(self):
        """ Destroy all widgets """
        self.frame.destroy()
        self.frame = None

    def search_product(self):
        """ Search for a product """
        print("Searching for product")
        search_term = self.frame.search_entry.get()
        products_list = [product for product in self.menu_list if search_term.lower() in product["Name"].lower() and not product["Hidden"] and int(product["Stock"]) > 0]
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)

        self.frame.update_menu(products_list, language_window, self.add_cart_item)

    def update_cart(self):
        """ Update the cart visually """
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.frame.update_cart(self.data.current_person, self.data.person_count, self.data.shopping_cart, language_window)

    def set_current_person(self, person):
        """ Set the current person """
        self.data.current_person = person
        
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.frame.update_cart(self.data.current_person, self.data.person_count, self.data.shopping_cart, language_window)

    def add_person(self):
        """ Add person to the cart """
        self.make_operation()
        self.data.person_count += 1
        self.data.shopping_cart.append([])
        self.data.current_person = self.data.person_count - 1
        
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.frame.update_cart(self.data.current_person, self.data.person_count, self.data.shopping_cart, language_window)

    def remove_person(self, i):
        """ Remove the person from the cart"""
        self.make_operation()
        self.data.person_count -= 1
        self.data.shopping_cart.pop(i)
        
        if self.data.person_count == 0:
            self.add_person()
        elif self.data.current_person == self.data.person_count:
            self.data.current_person -= 1
            
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.frame.update_cart(self.data.current_person, self.data.person_count, self.data.shopping_cart, language_window)

    def add_cart_item(self, product_widget):
        """Add an item to the shopping cart"""
        self.make_operation()
        
        item_name = product_widget.product_name.cget("text")
        item_price = product_widget.product_price.cget("text").split(" ")[0]
        print(f"Adding {item_name} to the Person {self.data.current_person}'s cart")
        
        item_list = [item["name"] for item in self.data.shopping_cart[self.data.current_person]]
        if item_name in item_list:
            self.data.shopping_cart[self.data.current_person][item_list.index(item_name)]["amount"] += 1
        else:
            self.data.shopping_cart[self.data.current_person].append({  "name": item_name,
                                                                        "price": float(item_price),
                                                                        "amount": 1})
            
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.frame.update_cart(self.data.current_person, self.data.person_count, self.data.shopping_cart, language_window)

    def make_operation(self):
        """ When you do/make an operation/event - DO functionality """
        data = deepcopy(self.data) # create a full copy of the whole data
        self.undo_stack.append(data) # put it in the undo stack
        self.redo_stack.clear() # clear the redo stack
        print(self.data)

    def undo(self):
        """ UNDO functionality """
        print("Undoing")
        print(self.undo_stack)
        # Return nothing if the stack is empty
        if len(self.undo_stack) == 0:
            return

        data = deepcopy(self.data) # create a full copy of the whole data
        self.redo_stack.append(data) # add it to the redo stack
        self.data = self.undo_stack.pop() # pop the first item from the undo stack
        self.update_cart() # update the cart visually

    def redo(self):
        """ REDO functionality """
        print("Redoing")
        print(self.redo_stack)
        # Return nothing if the stack is empty
        if len(self.redo_stack) == 0:
            return

        data = deepcopy(self.data) # create a full copy of the whole data
        self.undo_stack.append(data) # add it to the undo stack
        self.data = self.redo_stack.pop() # pop the first item from the redo stack
        self.update_cart() # update the cart visually

    def confirm_order(self):
        """Confirm the order and add it to the order history"""

        # double-check the order with a confirmation pop-up window
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.frame.shopping_cart_widget.double_check_confirm(language_window)
        self.frame.shopping_cart_widget.confirm_yes_btn.config(command=self.confirm_order_yes)
        self.frame.shopping_cart_widget.confirm_no_btn.config(command=self.confirm_order_no)

    def confirm_order_yes(self):
        print("Confirming order")
        order = []
        
        # Add all items in the shopping cart to the order
        for person in self.data.shopping_cart:
            order.append(person)
        self.order_history.append(order)

        print("Order history:")
        for order in self.order_history:
            print(order)

        # reset shopping cart
        self.frame.shopping_cart_widget.clear_cart()
        self.data.shopping_cart = []
        self.data.person_count = 0
        self.add_person()

        # empty the undo stack
        self.undo_stack = []
        self.redo_stack = []

        self.frame.shopping_cart_widget.confirm_window_close()

    def confirm_order_no(self):
        """ Unconfirmed the order and close the window """
        print("Cancelling order")
        self.frame.shopping_cart_widget.confirm_window_close()

    def load_menu(self):
        # load the menu from the database with VIP=true
        self.menu_list = [menu_item for menu_item in menu if menu_item["VIP"] == False]

    def switch_filter(self, filter_text):
        """ Switch between the filters, making them active or not and update menu"""
        print("Filtering products for", filter_text)
        
        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            self.allergens_dict[filter_text]["active"] = not self.allergens_dict[filter_text]["active"]
        else:
            self.beverage_filter_data[filter_text]["active"] = not self.beverage_filter_data[filter_text]["active"]
        self.update_menu()

    def switch_menu(self, menu):
        """ Switch between the beverages and food menus"""
        self.current_menu = menu
        self.update_menu()

    def update_menu(self):
        # Filter data
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            self.frame.update_filter(self.allergens_dict, language_window)
        else:
            self.frame.update_filter(self.beverage_filter_data, language_window)

        # Filter products based on the active filters
        products_list = []
        

        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            for product in self.menu_list:
                if product["Tag"] == "food" and not product["Hidden"] and int(product["Stock"]) > 0:
                    allergens = product["Allergens"]
                    if all([self.allergens_dict[allergen]["active"] for allergen in allergens]):
                        products_list.append(product)
        else:
            if self.beverage_filter_data["Beer"]["active"]:
                for product in self.menu_list:
                    if product["Tag"] == "beer" and not product["Hidden"] and int(product["Stock"]) > 0:
                        products_list.append(product)
            if self.beverage_filter_data["Wine"]["active"]:
                for product in self.menu_list:
                    if product["Tag"] == "wine" and not product["Hidden"] and int(product["Stock"]) > 0:
                        products_list.append(product)
            if self.beverage_filter_data["Cocktail"]["active"]:
                for product in self.menu_list:
                    if product["Tag"] == "cocktail" and not product["Hidden"] and int(product["Stock"]) > 0:
                        products_list.append(product)

        self.frame.update_menu(products_list, language_window, self.add_cart_item)
        for filter_btn in self.frame.filter_buttons:
            filter_text = filter_btn.cget("text")
            # works the same as language_window value but update the filter's button text
            eng_filter_text = [key for key, value in LANGUAGE[language_window].items() if value == filter_text]
            filter_btn.config(command=lambda text=eng_filter_text[0]: self.switch_filter(text))

# Main function that can be used to run this .py file individually to test some functionalities
if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    controller = CustomerController(root, None, "English")
    controller.create_widgets()
    root.mainloop()
