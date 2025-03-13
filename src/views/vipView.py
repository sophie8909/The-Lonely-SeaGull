import tkinter as tk
from views.customerView import CustomerView
from models.language import LANGUAGE

class VIPView(CustomerView):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent, current_language, current_resolution)
        # vip info (name and Account balance)
        print("VIP View")
        # name frame
        self.name_frame = tk.Frame(self.customer_info_frame, bg=self.background_color)
        self.name_frame.pack(side="top",fill="both", expand=True, padx=10)
        self.vip_welcome_label = tk.Label(self.name_frame, text=LANGUAGE[self.current_language]["welcome"], font=self.default_font, bg=self.background_color)
        self.vip_welcome_label.pack(side="left", anchor="e")
        self.vip_name_label = tk.Label(self.name_frame, font=self.default_font, bg=self.background_color)
        self.vip_name_label.pack(side="left", anchor="e")

        # balance frame
        self.balance_frame = tk.Frame(self.customer_info_frame, bg=self.background_color)
        self.balance_frame.pack(side="bottom",fill="both", expand=True, padx=10)
        self.vip_balance_label = tk.Label(self.balance_frame, text=LANGUAGE[self.current_language]["account balance"], font=self.default_font, bg=self.background_color)
        self.vip_balance_label.pack(side="left", anchor="e")
        self.vip_balance_amount_label = tk.Label(self.balance_frame, font=self.default_font, bg=self.background_color)
        self.vip_balance_amount_label.pack(side="right", anchor="e")


        self.add_to_balance_button = tk.Button(self.shopping_cart_widget.payment_frame, text=LANGUAGE[self.current_language]["add to balance"], fg="white", font=self.header_font, bg=self.primary_color)
        self.add_to_balance_button.pack(fill="x", pady=10)
