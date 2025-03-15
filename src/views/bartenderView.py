import tkinter as tk
from views.components.product_card import ProductCard
from src.views.components.bartender_panel import BartenderPanel
from views.components.settings import Settings
from views.baseView import BaseView
from tkinter import messagebox
from models.language import LANGUAGE


class BartenderView(BaseView):
    def __init__(self, parent, current_language, current_resolution, controller=None):
        super().__init__(parent, current_language, current_resolution)
        self.controller = controller  
        self.create_widgets()

    def create_widgets(self):
        """Create all widgets for bartender view"""

        # Create the main container frame
        self.main_frame = tk.Frame(self, bg=self.background_color)
        self.main_frame.pack(fill="both", expand=True)

        # Container for product and filters
        self.content_frame = tk.Frame(self.main_frame, bg=self.background_color)
        self.content_frame.pack(side="left", fill="both", expand=True)


        self.search_entry_name = tk.StringVar()
        # --- Search Box ---
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

        self.bartender_pannel = BartenderPanel(self.right_frame, self.current_language, self.current_resolution)
        self.bartender_pannel.pack(fill="both", expand=True)



        # # customer info
        # self.customer_info_frame = tk.Frame(self.right_frame, bg=self.background_color, padx=10, pady=10)
        # self.customer_info_frame.pack(side="top", fill="both", expand=True)

        # # name frame
        # self.name_frame = tk.Frame(self.customer_info_frame, bg=self.background_color)
        # self.name_frame.pack(side="top",fill="both", expand=True, padx=10)
        # self.welcome_label = tk.Label(self.name_frame, text=LANGUAGE[self.current_language]["hello"], font=self.default_font, bg=self.background_color)
        # self.welcome_label.pack(side="left", anchor="e")
        # self.name_label = tk.Label(self.name_frame, font=self.default_font, bg=self.background_color)
        # self.name_label.pack(side="left", anchor="e")


        # # --- Panic & Logout Buttons ---
        # self.panic_button = tk.Button(
        #     self.customer_info_frame,
        #     text=LANGUAGE[self.current_language]["panic"],
        #     bg="#AD0000",
        #     fg="white",
        #     font=self.default_font,
        # )
        # self.panic_button.pack(side="right", expand=True, ipady=6)

        # self.table_frame = tk.Frame(self.right_frame, bg=self.background_color, padx=10, pady=10)
        # self.table_frame.pack(side="top", fill="both", expand=True)



        