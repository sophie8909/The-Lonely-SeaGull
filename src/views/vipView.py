import tkinter as tk
from tkinter import messagebox, ttk, font
from models.language import LANGUAGE
from views.components.product import ProductCard, ShoppingCart
from views.customerView import CustomerView

class VIPView(CustomerView):
    def __init__(self, parent, current_language):
        super().__init__(parent, current_language)
        # vip info (name and Account balance)
        print("VIP View")
        self.vip_name_label = tk.Label(self.customer_info_frame, text="VIP Name", font=self.default_font)
        self.vip_name_label.pack()

        self.vip_balance_label = tk.Label(self.customer_info_frame, text="Account Balance", font=self.default_font)
        self.vip_balance_label.pack()