if __name__ == "__main__":
    import sys
    sys.path.append(sys.path[0] + "/../")

import tkinter as tk
from tkinter import messagebox, ttk, font
from models.language import LANGUAGE
from views.components.product import ProductCard, ShoppingCart
import os




class CustomerView(tk.Frame):
    def __init__(self, parent, current_language):
        super().__init__(parent, bg="#FFFFFF")
        self.current_language = current_language
        self.beers_list = []
        
        # Define colors
        self.primary_color = "#035BAC"
        self.light_primary = "#D5E5F5"  # Approximation of rgba(3, 91, 172, 0.27)
        self.background_color = "#FFFFFF"
        self.light_gray = "#D9D9D9"
        self.dark_text = "#5A5A5A"  # Approximation of rgba(0, 0, 0, 0.65)
        self.light_icon = "#BEBDBD"  # Approximation of rgba(151, 148, 148, 0.5)
        
        # Try to set up fonts (if not available, fallback to system fonts)
        try:
            self.default_font = font.Font(family="Roboto", size=14)
            self.header_font = font.Font(family="Roboto", size=24, weight="normal")
        except:
            self.default_font = font.Font(family="Arial", size=14)
            self.header_font = font.Font(family="Arial", size=24, weight="normal")
            
        # Create the main container frame
        self.main_frame = tk.Frame(self, bg=self.background_color)
        self.main_frame.pack(fill="both", expand=True)


        
        # Container for products and filters
        self.content_frame = tk.Frame(self.main_frame, bg="#D9D9D9", padx=10, pady=10)
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.logout_button = ttk.Button(self.main_frame, text="Log out")
        self.logout_button.pack(side="left", pady=20)
        
        # Create search bar
        self.search_frame = tk.Frame(self.content_frame, bg=self.background_color, height=45)
        self.search_frame.pack(fill="x", pady=10)
        
        self.search_entry = tk.Entry(self.search_frame, font=self.default_font, bd=1, relief="solid")
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.search_entry.insert(0, "Search...")
        self.search_entry.bind("<FocusIn>", lambda event: self.search_entry.delete(0, "end") if self.search_entry.get() == "Search..." else None)
        self.search_entry.bind("<FocusOut>", lambda event: self.search_entry.insert(0, "Search...") if self.search_entry.get() == "" else None)
        
        # Search button
        self.search_button = tk.Button(self.search_frame, text="🔍", bg=self.primary_color, fg="white", bd=0, padx=16, 
                                       font=self.default_font, activebackground="#034d91")
        self.search_button.pack(side="right", ipady=6)
        
        # Filter buttons frame
        self.filter_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        self.filter_frame.pack(fill="x", pady=10)
        
        # Filter buttons
        self.filter_buttons = []
        filter_data = [
            {"text": "magenta", "icon": "♥", "active": True},
            {"text": "iced beer", "icon": "♥", "active": False},
            {"text": "discount", "icon": "♥", "active": False},
            {"text": "alcohol-free", "icon": "♥", "active": False}
        ]
        
        for filter_info in filter_data:
            btn_frame = tk.Frame(self.filter_frame)
            btn_frame.pack(side="left", padx=5)
            
            if filter_info["active"]:
                btn_bg = self.light_primary
                btn_fg = self.primary_color
                icon_color = self.primary_color
            else:
                btn_bg = "#FAFAFA"
                btn_fg = self.dark_text
                icon_color = self.light_icon
            
            icon_label = tk.Label(btn_frame, text=filter_info["icon"], fg=icon_color, bg=btn_bg)
            icon_label.pack(side="left", padx=2)
            
            filter_button = tk.Button(btn_frame, text=filter_info["text"], 
                                     bg=btn_bg, fg=btn_fg, bd=1, relief="solid",
                                     padx=10, pady=5, font=self.default_font)
            filter_button.pack(side="left")
            self.filter_buttons.append(filter_button)
        
        # Product grid
        self.product_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        self.product_frame.pack(fill="both", expand=True, pady=10)

        self.products_widget=[]
        
        # Create a grid of product items (3x2 grid)
        for row in range(2):
            for col in range(3):
                product = ProductCard(self.product_frame, row, col, self.background_color, self.primary_color, self.default_font)
                self.products_widget.append(product)

        
        self.shopping_cart_widget = ShoppingCart(self.main_frame, self.background_color, self.primary_color, self.default_font)
        self.shopping_cart_widget.pack(side="right", fill="both", expand=True, pady=10)



    def add_person(self, remove_command=None):
        self.shopping_cart_widget.add_person(remove_command)

    def add_item(self, item_name, price, amount=1):
        self.shopping_cart_widget.add_item(item_name, price, amount)
    
    def set_person(self, current_person):
        self.shopping_cart_widget.set_person(current_person)

    def remove_person(self, i):
        self.shopping_cart_widget.remove_person(i)

        
    def display_menu_item(self, item, row, col):
        """Display a menu item in the product grid"""
        item_frame = tk.Frame(self.menu_container, relief=tk.RAISED, borderwidth=1)
        item_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        item_label = tk.Label(item_frame, text=item["name"])
        item_label.pack()

        item_price = tk.Label(item_frame, text=item["price"])
        item_price.pack()

        item_button = tk.Button(item_frame, text="Add to Cart")
        item_button.pack()
        
    def update_language(self):
        """Update UI text based on selected language"""
        self.add_friends_btn.config(text=LANGUAGE[self.current_language]["add friends"])
        self.confirm_btn.config(text=LANGUAGE[self.current_language]["confirm"])
        self.undo_btn.config(text=LANGUAGE[self.current_language]["undo"])
        self.redo_btn.config(text=LANGUAGE[self.current_language]["redo"])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Customer Ordering Interface")
    root.geometry("1000x800")
    
    ui = CustomerView(root, "English")
    ui.pack(expand=True, fill='both')
    root.mainloop()