from controllers.base import BaseController
from models.models import OwnerData
from views.ownerVIew import OwnerView

from models.language import LANGUAGE

from models.filters import allergens_dict, beverage_filter_data
from models.menu import menu as menu_data


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
        self.frame.owner_panel.name_label.config(text=self.main_controller.current_user.first_name + " " + self.main_controller.current_user.last_name)
        self.frame.owner_panel.item.update_btn.config(command=self.update_item_info)
        self.frame.owner_panel.add_menu_item_button.config(command=self.add_item_to_menu_click)
        self.frame.owner_panel.remove_menu_item_button.config(command=self.remove_item_from_menu_click)
        self.frame.owner_panel.hide_menu_item_button.config(command=self.hide_item_click)
        self.frame.owner_panel.order_refill_button.config(command=self.order_refill_click)

        self.tk_root.bind("<Return>", lambda event: self.search_product())
        self.frame.settings_widget.logout_button.bind("<Button-1>", self.main_controller.logout_button_click)
        self.frame.settings_widget.login_combo.bind("<<ComboboxSelected>>", self.main_controller.update_language)
        self.frame.settings_widget.res_combo.bind("<<ComboboxSelected>>", self.main_controller.change_res)

        self.load_menu()
        self.update_menu()

    def create_owner_widgets(self, current_language, current_resolution):
        print("Create owner widgets")
        self.frame = OwnerView(self.tk_root, current_language, current_resolution)
        self.frame.pack(fill="both", expand=True)

        self.owner_view_setup()


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
            products_list = [product for product in self.menu_list if search_text.lower() in product["Name"].lower()]
        else:
            products_list = [product for product in self.menu_list if search_text.lower() in product["Name"].lower()]

        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.frame.update_menu(products_list, language_window, self.select_item_click)

    def switch_menu(self, menu):
        self.current_menu = menu
        self.update_menu()

    def update_menu(self):
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)

        # Filter data
        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            self.frame.update_filter(self.allergens_dict, language_window)
        else:
            self.frame.update_filter(self.beverage_filter_data, language_window)

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

        self.frame.update_menu(products_list, language_window, self.select_item_click)
        for filter_btn in self.frame.filter_buttons:
            filter_text = filter_btn.cget("text")
            # not to complicate the logic of having too many duplicates in filter's dictionary
            eng_filter_text = [key for key, value in LANGUAGE[language_window].items() if value == filter_text]
            filter_btn.config(command=lambda text=eng_filter_text[0]: self.switch_filter(text))

    def update_item_info(self):
        """Update item in menu_list and refresh the menu"""
        product = self.frame.owner_panel.item.product  # Current selected product
        
        # Get updated product info from the form
        updated_product = self.frame.owner_panel.item.get_product()

        if product is None:
            # ---------- Case 1: New product ----------
            print("Adding new product:", updated_product)
            self.menu_list.append(updated_product)  # Add new product to menu
        else:
            # ---------- Case 2: Update existing product ----------
            print("Updating existing product:", updated_product)
            # Find and update the product in menu_list
            for i, p in enumerate(self.menu_list):
                if p["Name"] == product["Name"]:  # Assuming 'Name' is unique identifier
                    self.menu_list[i] = updated_product  # Update the product in menu_list
                    break  # Stop searching after update

        # Refresh the item detail view (right side)
        self.frame.owner_panel.item.update(updated_product)

        # Clear input fields
        self.frame.owner_panel.item.price_entry.delete(0, 'end')
        self.frame.owner_panel.item.stock_entry.delete(0, 'end')

        # Refresh the whole menu list (left side)
        self.update_menu()

    def add_item_to_menu_click(self):
        self.frame.owner_panel.item.product = None
        self.frame.owner_panel.item.set_add_active(True)

    def remove_item_from_menu_click(self):
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.frame.owner_panel.pop_up_window(
            title=LANGUAGE[language_window]["remove_item"],
            message="{}\n{}".format(self.frame.owner_panel.item.product["Name"], LANGUAGE[language_window]["remove_item_message"]),
            confirm_text=LANGUAGE[language_window]["remove"],
            confirm_command=self.remove_item
        )

    def remove_item(self):
        product = self.frame.owner_panel.item.product
        if product in self.menu_list:
            self.menu_list.remove(product)
        self.frame.owner_panel.item.update(None)
        self.update_menu()

    def hide_item_click(self):
        product = self.frame.owner_panel.item.product
        product["Hidden"] = not product["Hidden"]
        self.update_menu()
        self.frame.owner_panel.item.update(product)

    def order_refill_click(self):
        product = self.frame.owner_panel.item.product
        product["Stock"] = str(int(product["Stock"])+10)
        self.update_menu()
        self.frame.owner_panel.item.update(product)
