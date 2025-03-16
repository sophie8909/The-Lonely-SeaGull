if __name__ == "__main__":
    import sys
    sys.path.append(sys.path[0]+"/../..")
import tkinter as tk
from tkinter import ttk
from models.language import LANGUAGE
from views.baseView import BaseView

class ItemInfo(tk.Frame):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent)
        self.current_language = current_language
        self.current_resolution = current_resolution
        self.create_widgets()

    def create_widgets(self):
        self.item_label = tk.Label(self, text="", font=("Arial", 12))
        self.item_label.pack(side='top', expand=True, fill='both', anchor='center')

        info_frame = tk.Frame(self)
        info_frame.pack(side='bottom', expand=True, fill='both')

        self.price_frame = tk.Frame(info_frame)
        self.price_frame.pack(side='top', expand=True, fill='both') 
        self.price_label = tk.Label(self.price_frame, text=LANGUAGE[self.current_language]["price"], font=("Arial", 12))
        self.price_label.pack(side='left', anchor='w', padx=5)

        # input price
        self.price_info_label = tk.Label(self.price_frame, font=("Arial", 12))
        self.price_info_label.pack(side='left', anchor='e', padx=5)
        self.price_entry = tk.Entry(self.price_frame, font=("Arial", 12))
        self.currency = tk.Label(self.price_frame, text="SEK", font=("Arial", 12))
        

        stock_frame = tk.Frame(info_frame)
        stock_frame.pack(side='top', expand=True, fill='both')

        self.stock_label = tk.Label(stock_frame, text=LANGUAGE[self.current_language]["stock"], font=("Arial", 12))
        self.stock_label.pack(side='left', anchor='w', padx=5)
        self.stock_info_label = tk.Label(stock_frame, font=("Arial", 12))
        self.stock_info_label.pack(side='left', anchor='e', padx=5)

        # input stock
        self.stock_entry = tk.Entry(stock_frame, font=("Arial", 12))

        # Update btn
        self.update_btn = tk.Button(info_frame, text=LANGUAGE[self.current_language]["update"], font=("Arial", 12))
        

    def update(self, product):
        self.product = product 
        self.item_label.config(text=product["Name"])
        self.price_info_label.config(text=product["Price"])
        self.stock_info_label.config(text=product["Stock"])
        self.currency.pack(side='right', anchor='e', padx=5)
        self.price_entry.pack(side='right', anchor='e', padx=5)
        self.stock_entry.pack(side='right', anchor='e', padx=5)
        self.update_btn.pack(side='bottom', anchor='e', padx=5, pady=5)

    def get_price(self):
        return self.price_entry.get()
    
    def get_stock(self):
        return self.stock_entry.get()
    


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

        # test
        # for i in range(2):
        #     self._add_table(i+1, [{'item': 'item1', 'price': 10, 'comment': 'comment1'}, {'item': 'item2', 'price': 20, 'comment': 'comment2'}], 30)
        
        # Frame for holding 4 action buttons at corners
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", fill="both", expand=True)

        # Configure grid to evenly distribute buttons (2x2)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)

        # Button at top-left (Add item to the menu)
        self.on_house_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["add item to the menu"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.on_house_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Button at top-right (Remove item from the menu)
        self.compensation_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["remove item from menu"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.compensation_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Button at bottom-left (Hide item)
        self.single_payment_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["hide item"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.single_payment_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Button at bottom-right (Order refill)
        self.group_payment_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["order refill"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.group_payment_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)



    def update(self, tables):
        """
        Update the table data
        
        Args:
            tables (list): List of dictionaries containing table data
            e.g. [{'data': [{'item': 'item1', 'price': 10, 'comment': 'comment1'}, {'item': 'item2', 'price': 20, 'comment': 'comment2'}], 'total': 30}]
        """
        self._clear_tables()
        for i, table in enumerate(tables):
            data = table['data']
            total = table['total']
            self._add_table(i+1, data, total)
        
# Example usage
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Bartender Panel")
    panel = OwnerPanel(root, "English", 1)
    panel.pack(fill='both', expand=True, padx=10, pady=10)
    panel.update([{'data': [{'item': 'item1', 'price': 10, 'comment': 'comment1'}, {'item': 'item2', 'price': 20, 'comment': 'comment2'}], 'total': 30}])
    root.mainloop()
