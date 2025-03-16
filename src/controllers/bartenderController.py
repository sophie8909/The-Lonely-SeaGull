from dataclasses import dataclass
from typing import List
from copy import deepcopy
from tkinter import messagebox

from controllers.base import BaseController
from views.bartenderView import BartenderView

from models.menu import menu as menu_data
from models.filters import allergens_dict, beverage_filter_data
from models.language import LANGUAGE
from tkinter.simpledialog import askinteger




class BartenderController(BaseController):
    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        super().__init__(tk_root, current_language, current_resolution)

        self.frame = None
        self.table_count = 3
        self.table_data = []
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
        self.table_data = [[] for _ in range(self.table_count)]
        self.frame.bartender_pannel.set_value_changed_command(self.table_data_changed)
        self.frame.bartender_pannel.set_remove_command(self.item_removed)
        self.frame.bartender_pannel.panic_button.config(command=self.panic_alert)
        self.frame.bartender_pannel.single_payment_button.config(command=self.single_payment)
        self.frame.bartender_pannel.group_payment_button.config(command=self.group_payment)


        self.load_menu()
        self.update_menu()
        self.frame.bartender_pannel.update_table(self.table_data)
        

    

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

    def table_data_changed(self, event):
        self.table_data = self.frame.bartender_pannel.get_values()
        print("Table data changed", self.table_data)
        self.frame.bartender_pannel.update_value(self.table_data)

    def item_removed(self, table_id, item_id):
        self.table_data[table_id].pop(item_id)
        self.frame.bartender_pannel.update_table(self.table_data)
        



    # TODO
    def add_cart_item(self, product_card):
        print("Add to cart", product_card.product["Name"])
        table_id = self.frame.bartender_pannel.current_table
        item_name = product_card.product["Name"]
        item_amount = 1
        item_price = float(product_card.product["Price"].replace(" SEK", ""))
        item_reason = "Normal"
        item_comment = ""
        self.table_data[table_id].append({"item": item_name, "amount": item_amount, "price": item_price, "reason": item_reason, "comment": item_comment})
        self.frame.bartender_pannel.update_table(self.table_data, table_id)


    def panic_alert(self):
        """Handle panic"""
        messagebox.showinfo(LANGUAGE[self.current_language]["panic"], LANGUAGE[self.current_language]["panic"])

    def single_payment(self):
        table_id = self.frame.bartender_pannel.current_table
        msg = LANGUAGE[self.current_language]["total"] + " " + str(sum([item["price"] for item in self.table_data[table_id]])) + " SEK"
        messagebox.showinfo(LANGUAGE[self.current_language]["checkout"], msg)

    def group_payment(self):
        table_id = self.frame.bartender_pannel.current_table
        total_amount = sum(item["price"] for item in self.table_data[table_id])
        people_count = askinteger("Group Payment", "Enter number of people:", parent=self.tk_root, minvalue=1)
        if people_count:
            share = total_amount / people_count
            messagebox.showinfo("Group Payment", f"Total: {total_amount:.2f} SEK\nEach pays: {share:.2f} SEK")

    def search_product(self):
        search_text = self.frame.search_entry.get()
        print("Searching for", search_text)
        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            products_list = [product for product in self.food_list if search_text.lower() in product["Name"].lower()]
        else:
            products_list = [product for product in self.beer_list + self.wine_list + self.cocktail_list if search_text.lower() in product["Name"].lower()]
        self.frame.update_menu(products_list, self.select_item_click)


        
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
        self.frame.update_menu(products_list, self.add_cart_item)
        for filter_btn in self.frame.filter_buttons:
            filter_text = filter_btn.cget("text")  # 立即存下當前的文本
            filter_btn.config(command=lambda text=filter_text: self.switch_filter(text))
