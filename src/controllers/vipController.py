from controllers.custormerController import CustomerController
from views.vipView import VIPView
from models.food import food_menu
from models.beverages import beers, wines, cocktails
from models.vip_menu import vip_food, vip_beer, vip_wines, vip_cocktails


class VIPController(CustomerController):
    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        super().__init__(tk_root, main_controller, current_language, current_resolution)
        print("VIP Controller")

    def create_vip_widgets(self, current_language, current_resolution):
        self.frame = VIPView(self.tk_root, current_language, current_resolution)
        self.frame.pack(expand=True, fill='both')
        self.customer_view_setup()
        self.vip_view_setup()
    
    def vip_view_setup(self):
        self.frame.name_label.config(text=self.main_controller.current_user.first_name + " " + self.main_controller.current_user.last_name)
        self.frame.vip_balance_amount_label.config(text=self.main_controller.current_user.balance)
        self.frame.add_to_balance_button.config(command=self.add_to_balance)

    def add_to_balance(self):
        self.main_controller.current_user.balance += 100
        self.frame.vip_balance_amount_label.config(text=self.main_controller.current_user.balance)

    def load_menu(self):
        self.beer_list = beers + vip_beer
        self.wine_list = wines + vip_wines
        self.cocktail_list = cocktails + vip_cocktails
        self.food_list = food_menu + vip_food


if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    controller = VIPController(root, None, "English")
    controller.create_vip_widgets()
    root.mainloop()
