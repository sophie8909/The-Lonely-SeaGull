from tkinter import messagebox

from controllers.base import BaseController
from views.bartenderView import BartenderView

from models.menu import menu as menu_data
from models.filters import allergens_dict, beverage_filter_data
from models.language import LANGUAGE
from tkinter.simpledialog import askinteger

from views.components.bartender_panel import Notification


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
        self.notification = Notification(self.tk_root, 230,55, "white", self.current_language, "cambria 11", 8)

        # Left side
        self.frame.search_button.config(command=self.search_product)
        self.frame.beverages_button.config(command=lambda: self.switch_menu(LANGUAGE[self.current_language]["beverages"]))
        self.frame.food_button.config(command=lambda: self.switch_menu(LANGUAGE[self.current_language]["food"]))

        # Right side
        self.frame.bartender_panel.name_label.config(text=self.main_controller.current_user.first_name + " " + self.main_controller.current_user.last_name)
        self.table_data = [[] for _ in range(self.table_count)]
        self.frame.bartender_panel.set_value_changed_command(self.table_data_changed)
        self.frame.bartender_panel.set_remove_command(self.item_removed)
        self.frame.bartender_panel.panic_button.config(command=self.notification.show_animation)
        self.frame.bartender_panel.single_payment_button.config(command=self.single_payment)
        self.frame.bartender_panel.group_payment_button.config(command=self.group_payment)

        self.tk_root.bind("<Return>", lambda event: self.search_product())
        self.frame.settings_widget.logout_button.bind("<Button-1>", self.main_controller.logout_button_click)
        self.frame.settings_widget.login_combo.bind("<<ComboboxSelected>>", self.main_controller.update_language)
        self.frame.settings_widget.res_combo.bind("<<ComboboxSelected>>", self.main_controller.change_res)


        self.load_menu()
        self.update_menu()

        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.frame.bartender_panel.update_table(self.table_data, language_window)

    def create_bartender_widgets(self, current_language, current_resolution, current_controller):
        print("Create bartender widgets")
        self.frame = BartenderView(self.tk_root, current_language, current_resolution, current_controller)
        self.frame.pack(fill="both", expand=True)

        self.bartender_view_setup()

    def destroy_widgets(self):
        self.frame.destroy()
        self.frame = None

    def hide_widgets(self):
        pass

    def load_menu(self):
        """Load products and update view"""
        self.menu_list = menu_data

    def table_data_changed(self, event):
        language_window = self.main_controller.update_language(lambda e: self.main_controller.update_language)
        self.table_data = self.frame.bartender_panel.get_values()
        print("Table data changed", self.table_data)
        self.frame.bartender_panel.update_value(self.table_data, language_window)

    def item_removed(self, table_id, item_id):
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.table_data[table_id].pop(item_id)
        self.frame.bartender_panel.update_table(self.table_data, language_window)

    # when click show item detail on the right side and can modify the information
    def add_cart_item(self, product_card):
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        print("Add to cart", product_card.product["Name"])
        table_id = self.frame.bartender_panel.current_table
        item_name = product_card.product["Name"]
        item_amount = 1
        item_price = float(product_card.product["Price"].replace(" SEK", ""))
        item_reason = "Normal"
        item_comment = ""
        self.table_data[table_id].append({"item": item_name, "amount": item_amount, "price": item_price, "reason": item_reason, "comment": item_comment})
        self.frame.bartender_panel.update_table(self.table_data, language_window, table_id)

    def single_payment(self):
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        table_id = self.frame.bartender_panel.current_table
        msg = LANGUAGE[language_window]["total"] + " " + str(sum([item["price"] for item in self.table_data[table_id]])) + " SEK"
        messagebox.showinfo(LANGUAGE[language_window]["checkout"], msg)

    def group_payment(self):
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        table_id = self.frame.bartender_panel.current_table
        total_amount = sum(item["price"] for item in self.table_data[table_id])
        people_count = askinteger("Group Payment", f"{LANGUAGE[language_window]['enter number of people']}:", parent=self.tk_root, minvalue=1)
        messagebox.showinfo(LANGUAGE[language_window]["checkout"], f"{LANGUAGE[language_window]['total']}: {total_amount:.2f} SEK\n{LANGUAGE[language_window]['each pay']}: {total_amount/people_count:.2f} SEK")

    def search_product(self):
        search_text = self.frame.search_entry.get()
        print("Searching for", search_text)
        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            products_list = [product for product in self.menu_list if search_text.lower() in product["Name"].lower()]
        else:
            products_list = [product for product in self.menu_list if search_text.lower() in product["Name"].lower()]
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)
        self.frame.update_menu(products_list, language_window, self.add_cart_item)

    def switch_filter(self, filter_text):
        print("Filtering products for", filter_text)
        if self.current_menu == LANGUAGE[self.current_language]["food"]:
            self.allergens_dict[filter_text]["active"] = not self.allergens_dict[filter_text]["active"]
        else:
            self.beverage_filter_data[filter_text]["active"] = not self.beverage_filter_data[filter_text]["active"]
        self.update_menu()

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

        # TODO: bind the click callback
        self.frame.update_menu(products_list, language_window, self.add_cart_item)
        for filter_btn in self.frame.filter_buttons:
            filter_text = filter_btn.cget("text")  # 立即存下當前的文本
            # not to complicate the logic of having too many duplicates in filter's dictionary
            eng_filter_text = [key for key, value in LANGUAGE[language_window].items() if value == filter_text]
            filter_btn.config(command=lambda text=eng_filter_text[0]: self.switch_filter(text))
