# =============================================================================
# ownerView.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao, Darius Loga, Yuxie Liu
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: The owner view with all the widgets for the whole system
# =======================================================

# Import the necessary libraries
import tkinter as tk

# Local imports
from views.components.product_card_manager import ProductCardManager
from views.components.owner_panel import OwnerPanel
from views.components.settings import Settings
from views.baseView import BaseView
from models.language import LANGUAGE


class OwnerView(BaseView):
    """ The owner view class

       Here are all the widgets that are going to be available for the owner view

       Attributes:
           BaseView: the inherited class BaseView
    """

    def __init__(self, parent, current_language, current_resolution, controller):
        """ Initial method

            Args:
                parent: used to get the tk window/frame
                current_language: used to get the current language of the system
                current_resolution: used to get the current resolution of the window
                controller: used to get the owner controller
        """

        super().__init__(parent, current_language, current_resolution) #inherit from BaseView
        self.controller = controller

        self.create_widgets() # separate method to call here to add all the necessary widgets

    def create_widgets(self):
        """Create all widgets for owner view"""

        # Create the main container frame
        self.main_frame = tk.Frame(self, bg=self.background_color)
        self.main_frame.pack(fill="both", expand=True)

        # Container for product and filters
        self.content_frame = tk.Frame(self.main_frame, bg=self.background_color)
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Create search bar
        # Constructor used for the search entry widget
        self.search_entry_name = tk.StringVar()
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

        # Switch menu button food and beer
        self.switch_menu_frame = tk.Frame(self.content_frame, bg=self.background_color)
        self.switch_menu_frame.pack(fill="x", pady=10)

        # Two buttons split the frame in half
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

        # Set the number of columns in the product grid
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

        # Middle frame
        self.middle_frame = tk.Frame(self.main_frame, bg=self.background_color, padx=10, pady=10)
        self.middle_frame.pack(side="left", fill="both", expand=True)

        self.detail_label = tk.Label(self.middle_frame, text=LANGUAGE[self.current_language]["information"], font=self.header_font, bg=self.primary_color, fg="white")
        self.detail_label.pack(side="top", fill="both")

        # Detail info frame
        self.detail_frame = tk.Frame(self.middle_frame, bg=self.background_color, padx=10, pady=10)
        self.detail_frame.pack(side="top", fill="both", expand=True)

        # Right side of the main frame
        self.right_frame = tk.Frame(self.main_frame, bg=self.background_color, padx=10, pady=10)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Added the view for language and display size settings
        self.settings_widget = Settings(self.right_frame, self.current_language, self.current_resolution)
        self.settings_widget.pack(side="top", anchor="e")

        # Owner specific component
        self.owner_panel = OwnerPanel(self.right_frame, self.current_language, self.current_resolution)
        self.owner_panel.pack(fill="both", expand=True)

    def update_owner_language(self, current_lgn):
        """ Update UI text based on selected language

            Args:
                current_lgn: current language of the system
        """

        self.settings_widget.language_label.config(text=LANGUAGE[current_lgn]["language"])
        self.settings_widget.res_label.config(text=LANGUAGE[current_lgn]["resolution"])
        self.settings_widget.logout_button.config(text=LANGUAGE[current_lgn]["logout"])
        self.detail_label.config(text=LANGUAGE[current_lgn]["information"])
        self.food_button.config(text=LANGUAGE[current_lgn]["food"])
        self.beverages_button.config(text=LANGUAGE[current_lgn]["beverages"])
        self.search_entry_name.set(LANGUAGE[current_lgn]["search"])
        self.owner_panel.welcome_label.config(text=LANGUAGE[current_lgn]["welcome"])
        self.owner_panel.add_menu_item_button.config(text=LANGUAGE[current_lgn]["add item to the menu"])
        self.owner_panel.remove_menu_item_button.config(text=LANGUAGE[current_lgn]["remove item from menu"])
        self.owner_panel.hide_menu_item_button.config(text=LANGUAGE[current_lgn]["hide item"])
        self.owner_panel.order_refill_button.config(text=LANGUAGE[current_lgn]["order refill"])
        self.owner_panel.item.item_name_label.config(text=LANGUAGE[current_lgn]["name"])
        self.owner_panel.item.filter_label.config(text=LANGUAGE[current_lgn]["filter"])
        self.owner_panel.item.price_label.config(text=LANGUAGE[current_lgn]["price"])
        self.owner_panel.item.stock_label.config(text=LANGUAGE[current_lgn]["stock"])
        self.owner_panel.item.update_btn.config(text=LANGUAGE[current_lgn]["update"])

    def update_menu(self, products, current_lgn, select_item_callback=None):
        """ Update the product grid based on the products data

            Args:
                products: all the possible products
                current_lgn: current language
                select_item_callback: callback function that will be called when cart is added
        """

        # Clear existing product items
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        # List of product widgets
        self.products_widget=[]

        # Create a grid of product items
        row = 0
        col = 0

        # Create the product card for each of the items in the menu in a grid style
        for product in products:
            product_widget = ProductCardManager(self.product_frame, row, col,
                                         self.background_color, self.primary_color, self.default_font,
                                         product, self.detail_frame,
                                         current_lgn,
                                         click_callback=select_item_callback)

            self.products_widget.append(product_widget)
            col += 1

            # Switch to a new row
            if col >= self.product_card_col_num:
                col = 0
                row += 1

    def update_filter(self, filter_data, current_lgn):
        """Update the filter buttons based on the filter data

            Args:
                filter_data: filter data
                current_lgn: current language of the system
        """

        # Clear existing filter buttons
        for widget in self.filter_frame.winfo_children():
            widget.destroy()

        # List of filter buttons
        self.filter_buttons = []

        # Create a grid of filter buttons
        row = 0
        col = 0

        # Creating the filter label and buttons in a grid style
        for filter_name in list(filter_data):
            btn_frame = tk.Frame(self.filter_frame)
            btn_frame.grid(row=row, column=col, sticky="n", padx=5)

            # Set button colors based on active state
            if filter_data[filter_name]["active"]:
                btn_bg = self.light_primary
                btn_fg = self.primary_color
                icon_color = self.primary_color
            else:
                btn_bg = "#FAFAFA"
                btn_fg = self.dark_text
                icon_color = self.light_icon

            # Create icon label
            icon_label = tk.Label(btn_frame, text=filter_data[filter_name]["icon"], fg=icon_color, bg=btn_bg)
            icon_label.pack(side="left", padx=2)

            # Create filter button
            filter_button = tk.Button(btn_frame, text=LANGUAGE[current_lgn][filter_name],
                                      bg=btn_bg, fg=btn_fg, bd=1, relief="solid",
                                      padx=10, pady=5, font=self.default_font)
            filter_button.pack(side="left")

            self.filter_buttons.append(filter_button)
            col += 1

            # Switch to a new row
            if col >= self.filter_col_num:
                col = 0
                row += 1
