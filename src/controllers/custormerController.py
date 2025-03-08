if __name__ == "__main__":
    import sys
    sys.path.append(sys.path[0] + "/../")

from controllers.base import BaseController
from views.customerView import CustomerView

from models.food import food_menu
from models.beverages import beers, wines, cocktails


class CustomerController(BaseController):
    def __init__(self, tk_root, main_controller, current_language):
        super().__init__(tk_root, current_language)
        self.frame = None
        self.person_count = 0
        self.current_person = 0

        self.shopping_cart = []
        self.order_history = []
        self.undo_stack = []
        self.redo_stack = []
        self.ordered_list = []
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
        self.frame.shopping_cart_widget.add_friends_btn.config(command=self.add_person)
        self.frame.shopping_cart_widget.confirm_btn.config(command=self.confirm_order)
        self.add_person()
        # self.frame.shopping_cart_widget.undo_btn.config(command=self.undo)
        # self.frame.shopping_cart_widget.redo_btn.config(command=self.redo)

        self.frame.food_button.config(command=lambda: self.switch_menu("Food"))
        self.frame.beverages_button.config(command=lambda: self.switch_menu("Beverages"))
        # fetch data from the database and update the view
        self.load_menu()
        self.update_menu()
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

    def add_person(self):
        self.person_count += 1
        self.shopping_cart.append([])
        self.undo_stack.append('add_person')
        self.frame.add_person(remove_command=self.remove_person)
        self.current_person = self.person_count - 1
        self.frame.set_person(self.current_person)

    def remove_person(self, i):
        if isinstance(i, tk.Label):
            i = int(i.cget("text").split(" ")[1]) - 1
        print(i, self.person_count)
        self.person_count -= 1
            
        self.shopping_cart.pop(i)
        self.undo_stack.append('remove_person')
        self.frame.remove_person(i)
        if self.person_count == 0:
            self.add_person()
        elif self.current_person == self.person_count:
            self.current_person -= 1
            print(self.current_person, self.person_count, self.frame.shopping_cart_widget.items)
        self.frame.set_person(self.current_person)
    def add_cart_item(self, product_widget):
        """Add an item to the shopping cart"""
        print("Adding item to cart")
        item_name = product_widget.product_name.cget("text")
        itme_price = product_widget.product_price.cget("text").split(" ")[0]
        self.shopping_cart[self.current_person].append({"name": item_name, "price": itme_price})
        self.frame.shopping_cart_widget.add_item(item_name, itme_price)

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
        for person in self.shopping_cart:
            order.append(person)
        self.order_history.append(order)

        print("Order history:")
        for order in self.order_history:
            print(order)

        # reset shopping cart
        self.frame.shopping_cart_widget.clear_cart()
        self.shopping_cart = []
        self.person_count = 0
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