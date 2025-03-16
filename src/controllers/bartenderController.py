from dataclasses import dataclass
from typing import List
from copy import deepcopy

from controllers.base import BaseController
from views.bartenderView import BartenderView

from models.menu import menu
from models.filters import allergens_dict, beverage_filter_data



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





    def bartender_view_setup(self):
        # self.


        self.load_products()
        

    

    def create_bartender_widgets(self, current_language, current_resolution):
        print("Create bartender widgets")
        self.frame = BartenderView(self.tk_root, current_language, current_resolution)
        self.frame.pack(fill="both", expand=True)
        self.bartender_view_setup()

    def hide_widgets(self):
        pass
        self.frame.pack_forget()


    def load_products(self):
        """Load products and update view"""
        self.products = beers  # 假設目前只賣啤酒
        self.frame.update_products(self.products)

    def add_cart_item(self, product_card):
        """Add product to cart"""
        product = product_card.product
        print(f"Add {product['Name']} to cart")
        found = False
        for item in self.data.cart:
            if item['name'] == product['Name']:
                item['amount'] += 1
                found = True
                break
        if not found:
            self.data.cart.append({"name": product['Name'], "price": product['Price'], "amount": 1})
        self.frame.update_cart(self.data.cart)

    def offer_discount(self):
        """Offer discount logic here"""
        print("Offer discount - logic to implement")

    def panic_alert(self):
        """Handle panic"""
        print("Panic button pressed!")
