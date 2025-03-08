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
        self.beverages_list = []
        self.filter_data = {}
        self.food_list = []
        self.current_menu = "Beverages"
        
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
        
        
    
        # switch menu button food and beer
        self.switch_menu_frame = tk.Frame(self.content_frame, bg=self.background_color)
        self.switch_menu_frame.pack(fill="x", pady=10)

        # two buttons split the frame in half
        self.beverages_button = tk.Button(self.switch_menu_frame, text="Beverages", bg=self.primary_color, fg="white", bd=1,
                                        font=self.default_font, activebackground="#034d91")
        self.beverages_button.pack(side="left", expand=True, fill="both", ipady=6)
        self.food_button = tk.Button(self.switch_menu_frame, text="Food", bg=self.primary_color, fg="white", bd=1,
                                       font=self.default_font, activebackground="#034d91")
        self.food_button.pack(side="right", expand=True, fill="both", ipady=6) 
    



        # Filter buttons frame
        self.filter_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        self.filter_frame.pack(fill="x", pady=10)
        
        
        # Product grid
        self.product_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        self.product_frame.pack(fill="both", expand=True, pady=10)

        
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

    def update_menu(self):
        self.products_widget=[]
        for widget in self.product_frame.winfo_children():
            widget.destroy()
        

        if self.current_menu == "Beverages":
            self.update_filter()
        else:
            for widget in self.filter_frame.winfo_children():
                widget.destroy()

        # Create a grid of product items 
        row = 0
        col = 0
        if self.current_menu == "Food":
            for product in self.food_list:
                product_widget = ProductCard(self.product_frame, row, col, self.background_color, self.primary_color, self.default_font, product)
                self.products_widget.append(product_widget)
                col += 1
                if col >= 3:
                    col = 0
                    row += 1
        else:
            for product in self.beverages_list:
                if self.filter_data[product["type"]]["active"]:
                    product_widget = ProductCard(self.product_frame, row, col, self.background_color, self.primary_color, self.default_font, product)
                    self.products_widget.append(product_widget)
                    col += 1
                    if col >= 3:
                        col = 0
                        row += 1
    


    def update_filter(self):
        """Update the filter buttons based on the filter data"""
        # Clear existing filter buttons
        for widget in self.filter_frame.winfo_children():
            widget.destroy()

        # Filter buttons
        self.filter_buttons = []
        
        print(self.filter_data)
        print(list(self.filter_data))
        for filter_name in list(self.filter_data):
            btn_frame = tk.Frame(self.filter_frame)
            btn_frame.pack(side="left", padx=5)
            
            if self.filter_data[filter_name]["active"]:
                btn_bg = self.light_primary
                btn_fg = self.primary_color
                icon_color = self.primary_color
            else:
                btn_bg = "#FAFAFA"
                btn_fg = self.dark_text
                icon_color = self.light_icon
            
            icon_label = tk.Label(btn_frame, text=self.filter_data[filter_name]["icon"], fg=icon_color, bg=btn_bg)
            icon_label.pack(side="left", padx=2)
            
            filter_button = tk.Button(btn_frame, text=self.filter_data[filter_name]["text"], 
                                     bg=btn_bg, fg=btn_fg, bd=1, relief="solid",
                                     padx=10, pady=5, font=self.default_font)
            filter_button.pack(side="left")
            self.filter_buttons.append(filter_button)
        


    def filter_products(self, filter_type):
        """Filter products based on the selected filter"""
        print(f"Filtering products by {filter_type}")
        self.filter_data[filter_type]["active"] = not self.filter_data[filter_type]["active"]
        


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Customer Ordering Interface")
    root.geometry("1000x800")
    
    ui = CustomerView(root, "English")
    ui.pack(expand=True, fill='both')
    root.mainloop()