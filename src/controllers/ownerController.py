from dataclasses import dataclass
from typing import List
from copy import deepcopy
import tkinter as tk
from controllers.base import BaseController
from views.ownerVIew import OwnerView

from models.language import LANGUAGE

from models.filters import allergens_dict, beverage_filter_data
from models.menu import menu as menu_data
# from models.orders import Order

@dataclass
class OwnerData:
    cart: List[dict]

class OwnerController(BaseController):
    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        super().__init__(tk_root, current_language, current_resolution)

        self.frame = None
        self.data = OwnerData(cart=[])
        self.tk_root = tk_root

        self.main_controller = main_controller
        self.current_language = current_language
        self.allergens_dict = allergens_dict
        self.beverage_filter_data = beverage_filter_data

        self.current_menu = LANGUAGE[self.current_language]["beverages"]




    def owner_view_setup(self):
        # Left side
        self.frame.search_button.config(command=self.search_product)
        self.frame.beverages_button.config(command=lambda: self.switch_menu(LANGUAGE[self.current_language]["beverages"]))
        self.frame.food_button.config(command=lambda: self.switch_menu(LANGUAGE[self.current_language]["food"]))

        # Right side
        self.frame.owner_panel.item.update_btn.config(command=self.update_item_info)
        self.frame.owner_panel.add_menu_item_button.config(command=self.add_item_to_menu_click)
        self.frame.owner_panel.remove_menu_item_button.config(command=self.remove_item_from_menu_click)
        self.frame.owner_panel.hide_menu_item_button.config(command=self.hide_item_click)
        self.frame.owner_panel.order_refill_button.config(command=self.order_refill_click)


        self.load_menu()
        self.update_menu()

        

    

    def create_owner_widgets(self, current_language, current_resolution):
        print("Create owner widgets")
        self.frame = OwnerView(self.tk_root, current_language, current_resolution)
        self.frame.pack(fill="both", expand=True)
        self.owner_view_setup()

    def hide_widgets(self):
        pass

    def destroy_widgets(self):
        self.frame.destroy()
        self.frame = None

    def load_menu(self):
        self.menu_list = menu_data

   

    # when click show item detail on the right side and can modify the information
    def select_item_click(self, product_card):
        product = product_card.product
        self.frame.owner_panel.item.update(product)
        self.frame.owner_panel.item.set_add_active(True)

    def switch_filter(self, filter_text):
        print("Filtering products for", filter_text)
        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            self.allergens_dict[filter_text]["active"] = not self.allergens_dict[filter_text]["active"]
        else:
            self.beverage_filter_data[filter_text]["active"] = not self.beverage_filter_data[filter_text]["active"]
        self.update_menu()


    def search_product(self):
        search_text = self.frame.search_entry.get()
        print("Searching for", search_text)
        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            products_list = [product for product in self.food_list if search_text.lower() in product["Name"].lower()]
        else:
            products_list = [product for product in self.beer_list + self.wine_list + self.cocktail_list if search_text.lower() in product["Name"].lower()]
        self.frame.update_menu(products_list, self.select_item_click)

    def offer_discount(self):
        """Offer discount logic here"""
        print("Offer discount - logic to implement")

    def panic_alert(self):
        """Handle panic"""
        print("Panic button pressed!")

        
    def switch_menu(self, menu):
        self.current_menu = menu
        self.update_menu()


    def update_menu(self):
        # Filter data
        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            self.frame.update_filter(self.allergens_dict)
        else:
            self.frame.update_filter(self.beverage_filter_data)

        # Filter products based on the active filters
        products_list = []
        

        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            for product in self.menu_list:
                if product["Tag"] == "food":
                    allergens = product["Allergens"]
                    if all([self.allergens_dict[allergen]["active"] for allergen in allergens]):
                        products_list.append(product)
        else:
            if self.beverage_filter_data["Beers"]["active"]:
                for product in self.menu_list:
                    if product["Tag"] == "beer":
                        products_list.append(product)
            if self.beverage_filter_data["Wine"]["active"]:
                for product in self.menu_list:
                    if product["Tag"] == "wine":
                        products_list.append(product)
            if self.beverage_filter_data["Cocktails"]["active"]:
                for product in self.menu_list:
                    if product["Tag"] == "cocktail":
                        products_list.append(product)

        self.frame.update_menu(products_list, self.select_item_click)
        for filter_btn in self.frame.filter_buttons:
            filter_text = filter_btn.cget("text")  # 立即存下當前的文本
            filter_btn.config(command=lambda text=filter_text: self.switch_filter(text))


    def update_item_info(self):
        product = self.frame.owner_panel.item.product
        if product is None:
            product =self.frame.owner_panel.item.get_product()
            self.menu_list.append(product)
        else:
            product = self.frame.owner_panel.item.get_product()
            
        self.frame.owner_panel.item.update(product)
        self.frame.owner_panel.item.price_entry.delete(0, 'end')
        self.frame.owner_panel.item.stock_entry.delete(0, 'end')
        self.update_menu()
    
    def add_item_to_menu_click(self):
        self.frame.owner_panel.item.product = None
        self.frame.owner_panel.item.set_add_active(True)

    def remove_item_from_menu_click(self):
        self.frame.owner_panel.pop_up_window(
            title=LANGUAGE[self.current_language]["remove_item"],
            message="{}\n{}".format(self.frame.owner_panel.item.product["Name"], LANGUAGE[self.current_language]["remove_item_message"]),
            confirm_text=LANGUAGE[self.current_language]["remove"],
            confirm_command=self.remove_item
        )



    def remove_item(self):
        product = self.frame.owner_panel.item.product
        if product in self.food_list:
            self.food_list.remove(product)
        elif product in self.beer_list:
            self.beer_list.remove(product)
        elif product in self.wine_list:
            self.wine_list.remove(product)
        elif product in self.cocktail_list:
            self.cocktail_list.remove(product)
        self.update_menu()

    def hide_item_click(self):
        product = self.frame.owner_panel.item.product
        product["Hidden"] = not product["Hidden"]
        self.update_menu()
        self.frame.owner_panel.item.update(product)

    def order_refill_click(self):
        product = self.frame.owner_panel.item.product
        product["Stock"] = 10
        self.update_menu()
        self.frame.owner_panel.item.update(product)