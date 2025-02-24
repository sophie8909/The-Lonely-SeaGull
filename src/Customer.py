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
            if widget != self.combo:
                widget.destroy()

        
            

        tk.Label(self.customer_window, text=self.language[self.current_language]["beer menu"], font=("Arial", 16)).pack(pady=5)
        
        
        self.menu_frame = tk.Frame(self.customer_window, width=300, relief=tk.SUNKEN, borderwidth=2)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.menu_frame, text=self.language[self.current_language]["menu"], font=("Arial", 16)).pack(pady=5)

        for beer in self.fetch_beers():
            self.beer_label = tk.Label(self.menu_frame, text=f"{beer['name']} - {beer['price']} SEK", relief=tk.RAISED, padx=5, pady=5)
            self.beer_label.pack(pady=5)
            self.beer_label.bind("<ButtonPress-1>", lambda e, b=beer: self.add_to_cart(b))

        right_frame = tk.Frame(self.customer_window, relief=tk.SUNKEN, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(right_frame, text=self.language[self.current_language]["cart"], font=("Arial", 14)).pack()
        self.shopping_cart = tk.Listbox(right_frame, width=50, height=20)
        self.shopping_cart.pack()

        tk.Button(right_frame, text=self.language[self.current_language]["checkout"], command=lambda: messagebox.showinfo("Order", "Order placed successfully!")) \
            .pack(pady=10)

        tk.Button(right_frame, text=self.language[self.current_language]["<--"], command=self.undo_last_action).pack()
        tk.Button(right_frame, text=self.language[self.current_language]["-->"], command=self.redo_last_action).pack()



    # main interface for customer
    def open_customer_interface(self, ):
        self.shopping_cart = tk.Listbox()
        self.customer_window = tk.Toplevel()
        self.customer_window.title("Customer Ordering Interface")
        self.customer_window.geometry("600x400")
        self.customer_window.protocol("WM_DELETE_WINDOW", self.close_customer_interface)
        
        # Combo box for selecting different system language
        self.combo = ttk.Combobox(self.customer_window, state="readonly", values=["English", "Swedish", "Chinese"], height=2, width=10)
        self.combo.pack(padx=5)
        self.combo.current(0)
        self.combo.bind("<<ComboboxSelected>>", self.selection_changed)
    
        self.update_window()
        

    #endregion
