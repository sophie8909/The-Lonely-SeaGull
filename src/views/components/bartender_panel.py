if __name__ == "__main__":
    import sys
    sys.path.append(sys.path[0]+"/../..")
import tkinter as tk
from tkinter import ttk
from models.language import LANGUAGE
from views.baseView import BaseView

class TableFrame(tk.Frame):
    def __init__(self, parent, table_number, table_data=[], total=0, remove_command=None, **kwargs):
        super().__init__(parent, bg='lightgray', **kwargs)

        tk.Label(self, text=f"Table {table_number}", font=("Arial", 10, "bold"), bg='lightgray').pack(anchor='w', pady=5)
        
        # Items, Prices, Comments Headers
        headers_frame = tk.Frame(self, bg='lightgray')
        headers_frame.pack(fill='x')
        
        tk.Label(headers_frame, text="Items", bg='lightgray').pack(side='left', padx=5, expand=True)
        tk.Label(headers_frame, text="Prices", bg='lightgray').pack(side='left', padx=5, expand=True)
        tk.Label(headers_frame, text="Comments", bg='lightgray').pack(side='left', padx=5, expand=True)
        for row, data in enumerate(table_data):
            item_frame = tk.Frame(self, bg='lightgray')
            item_frame.pack(fill='x', pady=5)
            tk.Label(item_frame, text=data['item'], bg='lightgray').pack(side='left', padx=5, expand=True)
            tk.Label(item_frame, text=data['price'], bg='lightgray').pack(side='left', padx=5, expand=True)
            tk.Label(item_frame, text=data['comment'], bg='lightgray').pack(side='left', padx=5, expand=True)
            tk.Button(item_frame, text="X", command=remove_command).pack(side='right', padx=5)

        
        # Total Payment
        tk.Label(self, text=f"Total payment: {total:.2f} SEK", bg='lightgray').pack(anchor='w', pady=5)

class BartenderPanel(BaseView):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent, current_language, current_resolution)

        self.current_language = current_language
        
        # User Info and Panic Button in Horizontal Layout
        user_panic_frame = tk.Frame(self)
        user_panic_frame.pack(fill='x', pady=5)
        
        self.user_label = tk.Label(user_panic_frame, text="Hello, user_name_bartender", font=("Arial", 12))
        self.user_label.pack(side='left', expand=True, fill='both')
        
        self.panic_button = tk.Button(user_panic_frame, text="Panic", bg="red", fg="white", font=("Arial", 12, "bold"))
        self.panic_button.pack(side='left', expand=True, fill='both')
        
        self.table_frames = []
        self.table_frame = tk.Frame(self, bg='white')
        self.table_frame.pack(fill='both', expand=True)
        
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

        # Button at top-left (On house)
        self.on_house_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["on house"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.on_house_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Button at top-right (Compensation)
        self.compensation_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["compensation"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.compensation_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Button at bottom-left (Single Payment)
        self.single_payment_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["single payment"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.single_payment_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Button at bottom-right (Group Payment)
        self.group_payment_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["group payment"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.group_payment_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)


    def _add_table(self, table_number, table_data=[], total=0):
        table_frame = TableFrame(self.table_frame, table_number, table_data, total)
        table_frame.pack(fill='x', pady=10)
        self.table_frames.append(table_frame)

    def _clear_tables(self):
        for table_frame in self.table_frames:
            table_frame.destroy()
        self.table_frames = []

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
    panel = BartenderPanel(root, "English", 1)
    panel.pack(fill='both', expand=True, padx=10, pady=10)
    panel.update([{'data': [{'item': 'item1', 'price': 10, 'comment': 'comment1'}, {'item': 'item2', 'price': 20, 'comment': 'comment2'}], 'total': 30}])
    root.mainloop()
