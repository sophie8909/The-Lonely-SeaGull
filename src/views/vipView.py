import tkinter as tk
from views.customerView import CustomerView
from models.language import LANGUAGE

class VIPView(CustomerView):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent, current_language, current_resolution)

        # name frame
        self.name_frame = tk.Frame(self.customer_info_frame, bg=self.background_color)
        self.name_frame.pack(side="top",fill="both", expand=True, padx=10)
        self.welcome_label = tk.Label(self.name_frame, text=LANGUAGE[self.current_language]["welcome"], font=self.default_font, bg=self.background_color)
        self.welcome_label.pack(side="left", anchor="e")
        self.name_label = tk.Label(self.name_frame, font=self.default_font, bg=self.background_color)
        self.name_label.pack(side="left", anchor="e")

        # balance frame
        self.balance_frame = tk.Frame(self.customer_info_frame, bg=self.background_color)
        self.balance_frame.pack(side="bottom",fill="both", expand=True, padx=10)
        self.vip_balance_label = tk.Label(self.balance_frame, text=LANGUAGE[self.current_language]["account balance"], font=self.default_font, bg=self.background_color)
        self.vip_balance_label.pack(side="left", anchor="e")
        self.vip_balance_amount_label = tk.Label(self.balance_frame, font=self.default_font, bg=self.background_color)
        self.vip_balance_amount_label.pack(side="right", anchor="e")
        
        # vip code frame
        self.vip_code_frame = tk.Frame(self.customer_info_frame, bg=self.background_color)
        self.vip_code_frame.pack(side="bottom",fill="both", expand=True, padx=10)
        self.vip_code_label = tk.Label(self.vip_code_frame, text=LANGUAGE[self.current_language]["vip code"], font=self.default_font, bg=self.background_color)
        self.vip_code_label.pack(side="left", anchor="e")
        self.vip_code = tk.Label(self.vip_code_frame, font=self.default_font, bg=self.background_color)
        self.vip_code.pack(side="right", anchor="e")

        self.add_to_balance_button = tk.Button(self.shopping_cart_widget.payment_frame, text=LANGUAGE[self.current_language]["add to balance"], fg="white", font=self.header_font, bg=self.primary_color)
        self.add_to_balance_button.pack(fill="x", pady=10)

        self.get_vip_code_button = tk.Button(self.shopping_cart_widget.payment_frame, text=LANGUAGE[self.current_language]["get vip code"], fg="white", font=self.header_font, bg=self.primary_color)
        self.get_vip_code_button.pack(fill="x", pady=10)

    def update_vip_language(self, current_lgn):
        """Update UI text based on selected language"""
        self.settings_widget.language_label.config(text=LANGUAGE[current_lgn]["language"])
        self.settings_widget.res_label.config(text=LANGUAGE[current_lgn]["resolution"])
        self.settings_widget.logout_button.config(text=LANGUAGE[current_lgn]["logout"])
        self.detail_label.config(text=LANGUAGE[current_lgn]["information"])
        self.food_button.config(text=LANGUAGE[current_lgn]["food"])
        self.beverages_button.config(text=LANGUAGE[current_lgn]["beverages"])
        self.search_entry_name.set(LANGUAGE[current_lgn]["search"])
        self.shopping_cart_widget.add_friends_btn.config(text=LANGUAGE[current_lgn]["add friends"])
        self.shopping_cart_widget.confirm_btn.config(text=LANGUAGE[current_lgn]["confirm"])
        self.shopping_cart_widget.undo_btn.config(text=LANGUAGE[current_lgn]["undo"])
        self.shopping_cart_widget.redo_btn.config(text=LANGUAGE[current_lgn]["redo"])
        self.shopping_cart_widget.total_text_label.config(text=LANGUAGE[current_lgn]["total"])
        self.welcome_label.config(text=LANGUAGE[current_lgn]["welcome"])
        self.vip_balance_label.config(text=LANGUAGE[current_lgn]["account balance"])
        self.add_to_balance_button.config(text=LANGUAGE[current_lgn]["add to balance"])
        self.vip_code_label.config(text=LANGUAGE[current_lgn]["vip code"])
        self.get_vip_code_button.config(text=LANGUAGE[current_lgn]["get vip code"])