if __name__ == "__main__":
    import sys
    sys.path.append(sys.path[0] + "/../")

import tkinter as tk
from tkinter import ttk, font
from models.language import LANGUAGE
from views.baseView import BaseView
from views.components.product_card import ProductCard
from views.components.shopping_cart import ShoppingCart
from views.components.settings import Settings
from views.style import style

class CustomerView(BaseView):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent, current_language, current_resolution)
        self.search_entry_name = tk.StringVar()

        # Create the main container frame
        self.main_frame = tk.Frame(self, bg=self.background_color)
        self.main_frame.pack(fill="both", expand=True)

        # Container for products and filters
        self.content_frame = tk.Frame(self.main_frame, bg="#D9D9D9", padx=10, pady=10)
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        # Create search bar
        self.search_frame = tk.Frame(self.content_frame, bg=self.background_color, height=45)
        self.search_frame.pack(fill="x", pady=10)
        
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_entry_name, font=self.default_font, bd=1, relief="solid")
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.search_entry.insert(0, LANGUAGE[self.current_language]["search"])
        self.search_entry.bind("<FocusIn>", lambda event: self.search_entry.delete(0, "end") if self.search_entry.get() == LANGUAGE[self.current_language]["search"] else None)
        self.search_entry.bind("<FocusOut>", lambda event: self.search_entry.insert(0, LANGUAGE[self.current_language]["search"]) if self.search_entry.get() == "" else None)

        # Search button
        self.search_button = tk.Button(self.search_frame, text="🔍", bg=self.primary_color, fg="white", bd=0, padx=16, 
                                       font=self.default_font, activebackground="#034d91")
        self.search_button.pack(side="right", ipady=6)
    
        # switch menu button food and beer
        self.switch_menu_frame = tk.Frame(self.content_frame, bg=self.background_color)
        self.switch_menu_frame.pack(fill="x", pady=10)

        # two buttons split the frame in half
        self.beverages_button = tk.Button(self.switch_menu_frame, text=LANGUAGE[self.current_language]["beverages"], bg=self.primary_color, fg="white", bd=1,
                                        font=self.default_font, activebackground="#034d91")
        self.beverages_button.pack(side="left", expand=True, fill="both", ipady=6)
        self.food_button = tk.Button(self.switch_menu_frame, text=LANGUAGE[self.current_language]["food"], bg=self.primary_color, fg="white", bd=1,
                                       font=self.default_font, activebackground="#034d91")
        self.food_button.pack(side="right", expand=True, fill="both", ipady=6) 

        # Filter buttons frame
        self.filter_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        self.filter_frame.pack(fill="x", pady=10)

        # --- Product grid with scrollbar ---
        # Create a frame to hold canvas and scrollbar
        self.product_frame_container = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        self.product_frame_container.pack(fill="both", expand=True, pady=10)

        # Add a canvas in that frame
        self.product_canvas = tk.Canvas(self.product_frame_container, bg=self.content_frame["bg"], highlightthickness=0)
        self.product_canvas.pack(side="left", fill="both", expand=True)

        # set the number of columns in the product grid
        self.product_card_col_num = 2
        self.filter_col_num = 4

        # Add a vertical scrollbar linked to the canvas
        self.product_scrollbar = tk.Scrollbar(self.product_frame_container, orient="vertical", command=self.product_canvas.yview)
        self.product_scrollbar.pack(side="right", fill="y")

        # Configure canvas to respond to scrollbar
        self.product_canvas.configure(yscrollcommand=self.product_scrollbar.set)

        # Inner frame to hold actual product widgets
        self.product_frame = tk.Frame(self.product_canvas, bg=self.content_frame["bg"])

        # Create window inside canvas to hold the product frame
        self.product_canvas.create_window((0, 0), window=self.product_frame, anchor="nw")

        # Make sure canvas scrolls properly when frame content changes
        self.product_frame.bind("<Configure>", lambda e: self.product_canvas.configure(scrollregion=self.product_canvas.bbox("all")))

        # Optional: Enable mouse wheel scrolling on canvas (Windows + Mac + Linux)
        def _on_mouse_wheel(event):
            self.product_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind mousewheel to canvas
        self.product_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
        self.product_canvas.bind_all("<Button-4>", lambda e: self.product_canvas.yview_scroll(-1, "units"))  # For Linux
        self.product_canvas.bind_all("<Button-5>", lambda e: self.product_canvas.yview_scroll(1, "units"))   # For Linux

        # --- End of product grid with scrollbar ---

        # middle frame
        self.middle_frame = tk.Frame(self.main_frame, bg=self.background_color, padx=10, pady=10)
        self.middle_frame.pack(side="left", fill="both", expand=True)

        self.detail_label = tk.Label(self.middle_frame, text=LANGUAGE[self.current_language]["information"], font=self.header_font, bg=self.primary_color, fg="white")
        self.detail_label.pack(side="top", fill="both")

        # detail info frame
        self.detail_frame = tk.Frame(self.middle_frame, bg=self.background_color, padx=10, pady=10)
        self.detail_frame.pack(side="top", fill="both", expand=True)

        # left side of the main frame
        self.right_frame = tk.Frame(self.main_frame, bg=self.background_color, padx=10, pady=10)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Added the view for language and display size settings
        self.settings_widget = Settings(self.right_frame, self.background_color, self.primary_color, self.default_font, self.current_language, self.current_resolution)
        self.settings_widget.pack(side="top", anchor="e")
        # customer info
        self.customer_info_frame = tk.Frame(self.right_frame, bg=self.background_color, padx=10, pady=10)
        self.customer_info_frame.pack(fill="both", expand=True)
        
        # needs also to have the current_language as parameter
        self.shopping_cart_widget = ShoppingCart(self.right_frame, self.background_color, self.primary_color, self.default_font, self.current_language, self.current_resolution)
        self.shopping_cart_widget.pack(fill="both", expand=True, pady=10)


    def update_cart(self, current_person, person_count, shopping_cart, current_lgn):
        self.shopping_cart_widget.update_cart(current_person, person_count, shopping_cart, current_lgn)


    # def add_person(self, remove_command=None):
    #     self.shopping_cart_widget.add_person(remove_command)

    # def add_item(self, item_name, price, amount=1):
    #     self.shopping_cart_widget.add_item(item_name, price, amount)
    
    # def set_person(self, current_person):
    #     self.shopping_cart_widget.set_person(current_person)

    # def remove_person(self, i):
    #     self.shopping_cart_widget.remove_person(i)


    def display_menu_item(self, item, row, col):
        """Display a menu item in the product grid"""
        item_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        item_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        item_label = tk.Label(item_frame, text=item["name"])
        item_label.pack()

        item_price = tk.Label(item_frame, text=item["price"])
        item_price.pack()

        item_button = tk.Button(item_frame, text="Add to Cart")
        item_button.pack()


    # def update_language(self):
    #     """Update UI text based on selected language"""
    #     self.add_friends_btn.config(text=LANGUAGE[self.current_language]["add friends"])
    #     self.confirm_btn.config(text=LANGUAGE[self.current_language]["confirm"])
    #     self.undo_btn.config(text=LANGUAGE[self.current_language]["undo"])
    #     self.redo_btn.config(text=LANGUAGE[self.current_language]["redo"])


    def update_menu(self, products, add_to_cart_callback=None):
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        self.products_widget=[]
        # Create a grid of product items
        row = 0
        col = 0

        for product in products:
            product_widget = ProductCard(self.product_frame, row, col,
                                         self.background_color, self.primary_color, self.default_font,
                                         product, self.detail_frame,
                                         self.current_language,
                                         click_callback=add_to_cart_callback)
            self.products_widget.append(product_widget)
            col += 1
            if col >= self.product_card_col_num:
                col = 0
                row += 1


    def update_filter(self, filter_data, current_lgn):
        """Update the filter buttons based on the filter data"""
        # Clear existing filter buttons
        for widget in self.filter_frame.winfo_children():
            widget.destroy()

        # Filter buttons
        self.filter_buttons = []
        row = 0
        col = 0

        for filter_name in list(filter_data):
            btn_frame = tk.Frame(self.filter_frame)
            btn_frame.grid(row=row, column=col, sticky="n", padx=5)
            
            if filter_data[filter_name]["active"]:
                btn_bg = self.light_primary
                btn_fg = self.primary_color
                icon_color = self.primary_color
            else:
                btn_bg = "#FAFAFA"
                btn_fg = self.dark_text
                icon_color = self.light_icon

            icon_label = tk.Label(btn_frame, text=filter_data[filter_name]["icon"], fg=icon_color, bg=btn_bg)
            icon_label.pack(side="left", padx=2)

            filter_button = tk.Button(btn_frame, text=LANGUAGE[current_lgn][filter_name],
                                      bg=btn_bg, fg=btn_fg, bd=1, relief="solid",
                                      padx=10, pady=5, font=self.default_font)
            filter_button.pack(side="left")
            self.filter_buttons.append(filter_button)
            col += 1

            if col >= self.filter_col_num:
                col = 0
                row += 1



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Customer Ordering Interface")
    root.geometry("1000x800")
    
    ui = CustomerView(root, "English")
    ui.pack(expand=True, fill='both')
    root.mainloop()