if __name__ == "__main__":
    import sys
    sys.path.append(sys.path[0] + "/../")

from dataclasses import dataclass
from typing import List, Dict
from copy import deepcopy

from controllers.base import BaseController
from views.customerView import CustomerView

from models.food import food_menu
from models.beverages import beers, wines, cocktails

@dataclass
class CustomerControllerData:
    person_count: int
    current_person: int
    shopping_cart: List[List[dict]]
    def __str__(self):
        return f"Person count: {self.person_count}, Current person: {self.current_person}, Shopping cart: {self.shopping_cart}"
    
    def __repr__(self):
        return self.__str__()


class CustomerController(BaseController):
    def __init__(self, tk_root, main_controller, current_language):
        super().__init__(tk_root, current_language)
        self.frame = None
        self.data = CustomerControllerData(person_count=1, current_person=0, shopping_cart=[[]])
        self.undo_stack: List[CustomerControllerData] = []
        self.redo_stack: List[CustomerControllerData] = []
        self.beverage_filter_data = { 
            "Beers":{"text": "Beers", "icon": "🍺", "active": True}, 
            "Wine":{"text": "Wine", "icon": "🍷", "active": True},
            "Cocktails":{"text": "Cocktails", "icon": "🍸", "active": True},
        }
        self.allergens_dict = {
            "Gluten": {"text": "Gluten", "icon": "🌾", "active": True},
            "Lactose": {"text": "Lactose", "icon": "🥛", "active": True},
            "Egg": {"text": "Egg", "icon": "🥚", "active": True},
            "Fish": {"text": "Fish", "icon": "🐟", "active": True},
            "Sesame": {"text": "Sesame", "icon": "🌿", "active": True},
            "Nuts": {"text": "Nuts", "icon": "🌰", "active": True},
            "Coconut": {"text": "Coconut", "icon": "🥥", "active": True},
            "Shellfish": {"text": "Shellfish", "icon": "🦐", "active": True},
            "Soy": {"text": "Soy", "icon": "🌱", "active": True},
            "Peanuts": {"text": "Peanuts", "icon": "🥜", "active": True}
        }

        self.current_menu = "Beverages"

    def customer_view_setup(self):
        self.frame.shopping_cart_widget.set_on_drop(self.add_cart_item)
        self.frame.shopping_cart_widget.set_current_person_command(self.set_current_person)
        self.frame.shopping_cart_widget.set_remove_person_command(self.remove_person)
        self.frame.shopping_cart_widget.add_friends_btn.config(command=self.add_person)
        self.frame.shopping_cart_widget.confirm_btn.config(command=self.confirm_order)
        self.frame.shopping_cart_widget.undo_btn.config(command=self.undo)
        self.frame.shopping_cart_widget.redo_btn.config(command=self.redo)

        self.frame.food_button.config(command=lambda: self.switch_menu("Food"))
        self.frame.beverages_button.config(command=lambda: self.switch_menu("Beverages"))
        # fetch data from the database and update the view
        self.load_menu()
        self.update_menu()
        self.update_cart()
        for filter_btn in self.frame.filter_buttons:
            filter_text = filter_btn.cget("text")  # 立即存下當前的文本
            filter_btn.config(command=lambda text=filter_text: self.switch_filter(text))

    def create_widgets(self):
        self.frame = CustomerView(self.tk_root, self.current_language)
        self.frame.pack(expand=True, fill='both')
        self.customer_view_setup()

    def destroy_widgets(self):
        self.frame.destroy()
        self.frame = None

    def update_cart(self):
        self.frame.update_cart(self.data.current_person, self.data.person_count, self.data.shopping_cart)

    def set_current_person(self, person):
        self.data.current_person = person
        self.frame.update_cart(self.data.current_person, self.data.person_count, self.data.shopping_cart)

    def add_person(self):
        self.make_operation()
        self.data.person_count += 1
        self.data.shopping_cart.append([])
        self.data.current_person = self.data.person_count - 1
        self.frame.update_cart(self.data.current_person, self.data.person_count, self.data.shopping_cart)


    def remove_person(self, i):
        self.make_operation()
        self.data.person_count -= 1
        self.data.shopping_cart.pop(i)
        if self.data.person_count == 0:
            self.add_person()
        elif self.data.current_person == self.data.person_count:
            self.data.current_person -= 1
        self.frame.update_cart(self.data.current_person, self.data.person_count, self.data.shopping_cart)

    def add_cart_item(self, product_widget):
        """Add an item to the shopping cart"""
        self.make_operation()
        item_name = product_widget.product_name.cget("text")
        itme_price = product_widget.product_price.cget("text").split(" ")[0]
        print(f"Adding {item_name} to the Person {self.data.current_person}'s cart")
        item_list = [item["name"] for item in self.data.shopping_cart[self.data.current_person]]
        if item_name in item_list:
            self.data.shopping_cart[self.data.current_person][item_list.index(item_name)]["amount"] += 1
        else:
            self.data.shopping_cart[self.data.current_person].append({"name": item_name, "price": float(itme_price), "amount": 1})
        self.frame.update_cart(self.data.current_person, self.data.person_count, self.data.shopping_cart)

    def make_operation(self):
        data = deepcopy(self.data)
        self.undo_stack.append(data)
        self.redo_stack.clear()
        print(self.data)

    def undo(self):
        print("Undoing")
        print(self.undo_stack)
        if len(self.undo_stack) == 0:
            return
        data = deepcopy(self.data)
        self.redo_stack.append(data)
        self.data = self.undo_stack.pop()
        self.update_cart()

    def redo(self):
        print("Redoing")
        print(self.redo_stack)
        if len(self.redo_stack) == 0:
            return
        data = deepcopy(self.data)
        self.undo_stack.append(data)
        self.data = self.redo_stack.pop()
        self.update_cart()


    """Confirm the order and add it to the order history"""
    def confirm_order(self):
        # double check the order
        self.frame.shopping_cart_widget.double_check_confirm()
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
        print("Cancelling order")
        self.frame.shopping_cart_widget.confirm_window_close()

    def load_menu(self):
        self.beer_list = beers
        self.wine_list = wines
        self.cocktail_list = cocktails
        self.food_list = food_menu

        
    def switch_filter(self, filter_text):
        print("Filtering products for", filter_text)
        if self.current_menu == "Food":
            self.allergens_dict[filter_text]["active"] = not self.allergens_dict[filter_text]["active"]
        else:
            self.beverage_filter_data[filter_text]["active"] = not self.beverage_filter_data[filter_text]["active"]
        self.update_menu()
    
    def switch_menu(self, menu):
        self.current_menu = menu
        self.update_menu()
        

    def update_menu(self):
        # Filter data
        if self.current_menu == "Food":
            self.frame.update_filter(self.allergens_dict)
        else:
            self.frame.update_filter(self.beverage_filter_data)

        # Filter products based on the active filters
        products_list = []
        if self.current_menu == "Food":
            for product in self.food_list:
                allergens = product["Allergens"]
                if all([self.allergens_dict[allergen]["active"] for allergen in allergens]):
                    products_list.append(product)
        else:
            if self.beverage_filter_data["Beers"]["active"]:
                for product in self.beer_list:
                    products_list.append(product)
            if self.beverage_filter_data["Wine"]["active"]:
                for product in self.wine_list:
                    products_list.append(product)
            if self.beverage_filter_data["Cocktails"]["active"]:
                for product in self.cocktail_list:
                    products_list.append(product)

        self.frame.update_menu(products_list)
        for filter_btn in self.frame.filter_buttons:
            filter_text = filter_btn.cget("text")  # 立即存下當前的文本
            filter_btn.config(command=lambda text=filter_text: self.switch_filter(text))

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    controller = CustomerController(root, None, "English")
    controller.create_widgets()
    root.mainloop()