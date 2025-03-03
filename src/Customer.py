import tkinter as tk
from tkinter import messagebox, ttk
import sys

# Simulated beer data
# Simulated beer data with detailed information
SIMULATED_BEERS = [
    {"name": "Pale Ale", "brewery": "BrewCo", "country": "Sweden", "type": "Ale", "strength": "5.0%",
     "serving_size": "Bottle", "price": 49.99},
    {"name": "Stout", "brewery": "DarkBrew", "country": "Ireland", "type": "Stout", "strength": "6.5%",
     "serving_size": "Tap", "price": 59.99},
    {"name": "Lager", "brewery": "GoldenBrew", "country": "Germany", "type": "Lager", "strength": "4.7%",
     "serving_size": "Bottle", "price": 39.99},
    {"name": "IPA", "brewery": "HopHouse", "country": "USA", "type": "IPA", "strength": "7.2%", "serving_size": "Tap",
     "price": 54.99}
]


class Customer:
    def __init__(self, language, current_language):
        self.shopping_cart = None
        self.language = language
        self.current_language = current_language
        self.order_history = []
        self.redo_stack = []
        self.ordered_list = []

    # Fetch beer data
    def fetch_beers(self):
        return SIMULATED_BEERS

    # region Operations of Shopping Cart
    # Add beer to shopping cart and clear redo stack
    def add_to_cart(self, beer):
        self.shopping_cart.insert(tk.END, f"{beer['name']} ({beer['brewery']}) - {beer['price']} SEK")
        self.order_history.append(beer)
        self.redo_stack.clear()
   
    # Undo the last action
    def undo_last_action(self):
        if self.order_history:
            last_item = self.order_history.pop()
            self.shopping_cart.delete(tk.END)
            self.redo_stack.append(last_item)

    # Redo the last action
    def redo_last_action(self):
        if self.redo_stack:
            item = self.redo_stack.pop()
            self.shopping_cart.insert(tk.END, f"{item['name']} ({item['brewery']}) - {item['price']} SEK")
            self.order_history.append(item)
    # endregion


    
    

    
    #region Customer Interface

    # Close the customer interface
    def close_customer_interface(self):
        self.customer_window.destroy()
        sys.exit()

    def selection_changed(self, event):
        self.current_language = self.combo.get()
        self.update_window()
        
    def update_window(self):
        # Clear the window
        for widget in self.customer_window.winfo_children():


        
            

        



    # main interface for customer
    def open_customer_interface(self):
        
        
        
    
        self.update_window()
        

    #endregion
