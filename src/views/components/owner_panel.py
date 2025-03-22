import tkinter as tk
from tkinter import ttk
from models.language import LANGUAGE
from views.baseView import BaseView

class ItemInfo(tk.Frame):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent)
        self.current_language = current_language
        self.current_resolution = current_resolution
        self.dynamic_entries = {}  # Dictionary to hold dynamically created input fields
        self.create_widgets()

    def create_widgets(self):

        # ---------------- Name Frame ----------------
        name_frame = tk.Frame(self)
        name_frame.pack(side='top', expand=True, fill='both')

        # Product name label (view mode)
        self.item_label = tk.Label(name_frame, text="", font=("Arial", 12))
        self.item_label.pack(expand=True, fill='both', anchor='center')

        # Product name and name entry (edit mode)
        self.item_name_label = tk.Label(name_frame, text=LANGUAGE[self.current_language]["name"], font=("Arial", 12))
        self.item_name_label.pack(side='left', anchor='w', padx=5)

        self.item_name_entry = tk.Entry(name_frame, font=("Arial", 12))

        # ---------------- Filter/Category Frame ----------------
        self.filter_frame = tk.Frame(self)
        self.filter_frame.pack(side='top', expand=True, fill='both')

        # Filter label
        self.filter_label = tk.Label(self.filter_frame, text=LANGUAGE[self.current_language]["filter"], font=("Arial", 12))
        self.filter_label.pack(side='left', anchor='w', padx=5)

        # Filter dropdown for selecting type (beer, wine, cocktail, food)
        self.filter_combobox = ttk.Combobox(self.filter_frame, values=["beer", "wine", "cocktail", "food"], font=("Arial", 12))
        self.filter_combobox.pack(side='left', anchor='e', padx=5, pady=5)
        self.filter_combobox.bind("<<ComboboxSelected>>", self.on_filter_selected)  # Bind event to handle filter change

        # ---------------- Dynamic Fields Container ----------------
        self.dynamic_frame = tk.Frame(self)
        self.dynamic_frame.pack(side='top', expand=True, fill='both', pady=5)

        # ---------------- Price and Stock Section ----------------
        info_frame = tk.Frame(self)
        info_frame.pack(side='bottom', expand=True, fill='both')

        # Price field (Entry only)
        self.price_frame = tk.Frame(info_frame)
        self.price_frame.pack(side='top', expand=True, fill='both')
        self.price_label = tk.Label(self.price_frame, text=LANGUAGE[self.current_language]["Price"], font=("Arial", 12))
        self.price_label.pack(side='left', anchor='w', padx=5)
        self.price_entry = tk.Entry(self.price_frame, font=("Arial", 12))  # Direct input
        self.price_entry.pack(side='left', anchor='e', padx=5)
        self.currency = tk.Label(self.price_frame, text="SEK", font=("Arial", 12))
        self.currency.pack(side='left', anchor='e', padx=5)

        # Stock field (Entry only)
        stock_frame = tk.Frame(info_frame)
        stock_frame.pack(side='top', expand=True, fill='both')
        self.stock_label = tk.Label(stock_frame, text=LANGUAGE[self.current_language]["stock"], font=("Arial", 12))
        self.stock_label.pack(side='left', anchor='w', padx=5)
        self.stock_entry = tk.Entry(stock_frame, font=("Arial", 12))  # Direct input
        self.stock_entry.pack(side='left', anchor='e', padx=5)

        # ---------------- Update Button ----------------
        self.update_btn = tk.Button(info_frame, text=LANGUAGE[self.current_language]["update"], font=("Arial", 12))

    def on_filter_selected(self, event=None):
        """Handle dynamic field creation based on selected tag"""
        # Clear old fields
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        self.dynamic_entries.clear()

        # Define dynamic fields based on selected tag
        tag = self.filter_combobox.get()
        fields = []
        if tag == "beer":
            fields = ["Producer/Brewery", "Country", "Type", "Strength", "Serving size", "Alcohol Content", "Tannins"]
        elif tag == "wine":
            fields = ["Year", "Producer", "Type", "Grape", "Serving size", "Alcohol Content", "Tannins"]
        elif tag == "cocktail":
            fields = ["Strength", "Contents/Recipe", "Serving size", "Alcohol Content", "Tannins"]
        elif tag == "food":
            fields = ["Ingredients", "Allergens"]

        # Create fields dynamically
        for field in fields:
            frame = tk.Frame(self.dynamic_frame)
            frame.pack(fill='x', pady=2)
            label = tk.Label(frame, text=field, font=("Arial", 12))
            label.pack(side='left', padx=5)
            entry = tk.Entry(frame, font=("Arial", 12))
            entry.pack(side='right', padx=5, fill='x', expand=True)
            self.dynamic_entries[field] = entry  # Save entry for future use

    def update(self, product):
        """Fill the widget with product data (for edit/view mode)"""
        if product is None:
            self.item_label.config(text="")
            self.filter_combobox.set("")
            self.price_entry.delete(0, tk.END)
            self.stock_entry.delete(0, tk.END)
        else:
            self.product = product
            self.item_label.config(text=product["Name"])
            self.filter_combobox.set(product["Tag"])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, product["Price"].replace(" SEK", ""))  # Remove SEK if exists
            self.stock_entry.delete(0, tk.END)
            self.stock_entry.insert(0, product["Stock"])
        
        self.set_add_active(False)  # Set to view mode
        self.on_filter_selected()  # Load appropriate fields

        # Fill dynamic fields
        for key, entry in self.dynamic_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, product.get(key, ""))

    def get_price(self):
        return self.price_entry.get()

    def get_stock(self):
        return self.stock_entry.get()

    def get_tag(self):
        return self.filter_combobox.get()

    def set_add_active(self, active):
        """Toggle between add/edit mode and view mode"""
        if active:
            # Show input fields for editing
            self.item_name_entry.pack(expand=True, fill='both', anchor='center')
            self.price_entry.pack(side='left', anchor='e', padx=5)
            self.currency.pack(side='left', anchor='e', padx=5)
            self.stock_entry.pack(side='left', anchor='e', padx=5)
            self.update_btn.pack(side='bottom', anchor='e', padx=5, pady=5)
        else:
            # Hide entry, only show label
            self.item_name_entry.pack_forget()
            self.item_label.pack(expand=True, fill='both', anchor='center')
            # keep price and stock entry visible for review and edit anytime

    def get_product(self):
        """Collect all data from user input and return as dictionary"""
        tag = self.filter_combobox.get()
        product = {
            "Name": self.item_name_entry.get(),
            "Price": self.price_entry.get() + " SEK",
            "Stock": self.stock_entry.get(),
            "VIP": False,
            "Hidden": False,
            "Tag": tag
        }
        # Add dynamic fields data
        for field, entry in self.dynamic_entries.items():
            if field == "Allergens":
                if entry.get():
                    product[field] = entry.get().split(",")
                else:
                    product[field] = []
            else:
                product[field] = entry.get()
        return product


class OwnerPanel(BaseView):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent, current_language, current_resolution)

        self.current_language = current_language
        
        # User Info and Panic Button in Horizontal Layout
        user_panic_frame = tk.Frame(self)
        user_panic_frame.pack(fill='x', pady=5)
        
        # name frame
        self.name_frame = tk.Frame(user_panic_frame, bg=self.background_color)
        self.name_frame.pack(side="left",fill="both", expand=True, padx=10)
        self.welcome_label = tk.Label(self.name_frame, text=LANGUAGE[self.current_language]["welcome"], font=self.default_font, bg=self.background_color)
        self.welcome_label.pack(side="left", anchor="e")
        self.name_label = tk.Label(self.name_frame, font=self.default_font, bg=self.background_color)
        self.name_label.pack(side="left", anchor="e")

        # Item Info for modifying the menu
        self.item_info_frame = tk.Frame(self)
        self.item_info_frame.pack(fill='x', pady=5)

        self.item = ItemInfo(self.item_info_frame, self.current_language, self.current_resolution)
        self.item.pack(side='left', expand=True, fill='both')


        # Frame for holding 4 action buttons at corners
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", fill="both", expand=True)

        # Configure grid to evenly distribute buttons (2x2)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)

        # Button at top-left (Add item to the menu)
        self.add_menu_item_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["add item to the menu"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.add_menu_item_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Button at top-right (Remove item from the menu)
        self.remove_menu_item_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["remove item from menu"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.remove_menu_item_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Button at bottom-left (Hide item)
        self.hide_menu_item_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["hide item"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.hide_menu_item_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Button at bottom-right (Order refill)
        self.order_refill_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["order refill"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.order_refill_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    
    # pop_up_window with confirm button
    def pop_up_window(self, title: str, message: str, confirm_text: str, confirm_command: callable):
        """Create a pop-up window with a message and a confirm button"""
        """
        Args:
        title (str): Title of the pop-up window
        message (str): Message to display in the pop-up window
        confirm_text (str): Text to display on the confirm button
        confirm_command (function): Function to execute when the confirm button is clicked
        """

        # Create a new pop-up window
        pop_up = tk.Toplevel()
        pop_up.title(title)
        pop_up.geometry("400x300")
        pop_up.resizable(False, False)

        # center the pop_up window
        pop_up.update_idletasks()
        pop_up_width = pop_up.winfo_width()
        pop_up_height = pop_up.winfo_height()
        screen_width = pop_up.winfo_screenwidth()
        screen_height = pop_up.winfo_screenheight()
        x = (screen_width/2) - (pop_up_width/2)
        y = (screen_height/2) - (pop_up_height/2)
        pop_up.geometry("%dx%d+%d+%d" % (pop_up_width, pop_up_height, x, y))

        # Add message to the pop_up window
        message_label = tk.Label(pop_up, text=message, font=self.default_font)
        message_label.pack(pady=10)

        # after confirming, destroy the pop_up window
        confirm_button = tk.Button(pop_up, 
                                   text=confirm_text, 
                                   font=self.default_font,
                                   bg=self.primary_color,
                                   fg="white")
        confirm_button.pack(side='bottom', anchor='center', pady=10)

        # Bind the confirm button to the confirm_command
        confirm_button.config(command=lambda: [confirm_command(), pop_up.destroy()])
        

# Example usage
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Owner Panel")
    root.geometry("800x600")
    root.resizable(False, False)

    owner_panel = OwnerPanel(root, "en", "800x600")
    owner_panel.pack(fill='both', expand=True)

    root.mainloop()