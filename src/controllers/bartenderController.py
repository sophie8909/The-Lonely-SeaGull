from dataclasses import dataclass
from typing import List
from copy import deepcopy

from controllers.base import BaseController
from views.bartenderView import BartenderView

from models.menu import menu as menu_data
from models.filters import allergens_dict, beverage_filter_data
from models.language import LANGUAGE


@dataclass
class BartenderData:
    cart: List[dict]

class BartenderController(BaseController):
    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        super().__init__(tk_root, current_language, current_resolution)

        self.frame = None
        self.data = BartenderData(cart=[])
        
        self.main_controller = main_controller
        self.current_language = current_language
        self.allergens_dict = allergens_dict
        self.beverage_filter_data = beverage_filter_data

        self.current_menu = LANGUAGE[self.current_language]["beverages"]



    def bartender_view_setup(self):
        # Left side
        self.frame.search_button.config(command=self.search_product)
        self.frame.beverages_button.config(command=lambda: self.switch_menu(LANGUAGE[self.current_language]["beverages"]))
        self.frame.food_button.config(command=lambda: self.switch_menu(LANGUAGE[self.current_language]["food"]))

        # Right side


        self.load_menu()
        self.update_menu()
        

    

    def create_bartender_widgets(self, current_language, current_resolution):
        print("Create bartender widgets")
        self.frame = BartenderView(self.tk_root, current_language, current_resolution)
        self.frame.pack(fill="both", expand=True)
        self.bartender_view_setup()

    def hide_widgets(self):
        pass


    def load_menu(self):
        """Load products and update view"""
        self.menu_list = menu_data

    # TODO
    def add_cart_item(self, product_card):
        pass

    def offer_discount(self):
        """Offer discount logic here"""
        print("Offer discount - logic to implement")

    def panic_alert(self):
        """Handle panic"""
        print("Panic button pressed!")

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
            if self.beverage_filter_data["Beer"]["active"]:
                for product in self.menu_list:
                    if product["Tag"] == "beer":
                        products_list.append(product)
            if self.beverage_filter_data["Wine"]["active"]:
                for product in self.menu_list:
                    if product["Tag"] == "wine":
                        products_list.append(product)
            if self.beverage_filter_data["Cocktail"]["active"]:
                for product in self.menu_list:
                    if product["Tag"] == "cocktail":
                        products_list.append(product)

        # TODO: bind the click callback
        self.frame.update_menu(products_list, None)
        for filter_btn in self.frame.filter_buttons:
            filter_text = filter_btn.cget("text")  # 立即存下當前的文本
            filter_btn.config(command=lambda text=filter_text: self.switch_filter(text))
