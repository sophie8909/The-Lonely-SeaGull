if __name__ == "__main__":
    import sys
    sys.path.append(sys.path[0]+"/../..")
import tkinter as tk
from tkinter import ttk
from models.language import LANGUAGE
from views.baseView import BaseView

class TableFrame(tk.Frame):
    def __init__(self, parent, table_number, table_data=[], total=0, value_changed_command=None, remove_command=None, focus_command=None, **kwargs):
        super().__init__(parent, bg='lightgray', **kwargs)

        tk.Label(self, text=f"Table {table_number}", font=("Arial", 10, "bold"), bg='lightgray').pack(anchor='w', pady=5)
        
        # Items, Prices, Comments Headers
        headers_frame = tk.Frame(self, bg='lightgray')
        headers_frame.pack(fill='x')
        headers_frame.grid_columnconfigure(0, weight=1)
        headers_frame.grid_columnconfigure(2, weight=1)
        headers_frame.grid_columnconfigure(3, weight=1)
        headers_frame.grid_columnconfigure(4, weight=1)
        
        # Headers using grid layout
        tk.Label(headers_frame, text="Items", bg='lightgray', font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, sticky="ew")
        tk.Label(headers_frame, text="Amount", bg='lightgray', font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, sticky="ew")
        tk.Label(headers_frame, text="Prices", bg='lightgray', font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, sticky="ew")
        tk.Label(headers_frame, text="Reason", bg='lightgray', font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5, sticky="ew")
        tk.Label(headers_frame, text="Comments", bg='lightgray', font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, sticky="ew")

        self.items = []
        for row, data in enumerate(table_data):
            # Use grid for each item row within its own frame
            # item_frame = tk.Frame(self, bg='lightgray')
            # item_frame.pack(fill='x', pady=2)
            # item_frame.grid_columnconfigure(0, weight=1)
            # item_frame.grid_columnconfigure(2, weight=1)
            # item_frame.grid_columnconfigure(3, weight=1)
            # item_frame.grid_columnconfigure(4, weight=1)

            item = tk.Label(headers_frame, text=data['item'], bg='lightgray')
            item.grid(row=row+1, column=0, padx=5, sticky="ew")

            amount = ttk.Combobox(headers_frame, values=[str(i) for i in range(1, 100)], state='readonly', width=2)
            amount.set("1")
            amount.grid(row=row+1, column=1, padx=5)

            price = tk.Entry(headers_frame, bg='lightgray')
            price.insert(0, f"{data['price']:.2f}")
            price.grid(row=row+1, column=2, padx=5, sticky="ew")

            reason = ttk.Combobox(headers_frame, values=["Normal", "On House", "Compensation"], state='readonly')
            reason.set(data['reason'])
            reason.grid(row=row+1, column=3, padx=5, sticky="ew")

            comment = tk.Entry(headers_frame, bg='lightgray')
            comment.insert(0, data['comment'])
            comment.grid(row=row+1, column=4, padx=5, sticky="ew")

            self.items.append((item, amount, price, reason, comment))
            
            tk.Button(headers_frame, text="X", command=lambda table_id=table_number-1, item_id=row: remove_command(table_id, item_id)).grid(row=row+1, column=5, padx=5)

            if value_changed_command:
                price.bind("<FocusOut>", value_changed_command)
                price.bind("<Return>", value_changed_command)
                amount.bind("<<ComboboxSelected>>", value_changed_command)
                reason.bind("<<ComboboxSelected>>", value_changed_command)
                comment.bind("<FocusOut>", value_changed_command)
                comment.bind("<Return>", value_changed_command)


        self.bind("<Button-1>", lambda event, table_id=table_number-1: focus_command(table_id))
        
        # Total Payment
        self.total = tk.Label(self, text=f"Total payment: {total:.2f} SEK", bg='lightgray')
        self.total.pack(anchor='w', pady=5)

    def get_values(self):
        return [{'item': item[0].cget('text'), 'amount': int(item[1].get()), 'price': float(item[2].get()), 'reason': item[3].get(), 'comment': item[4].get()} for item in self.items]
    
    def set_values(self, table_data, total):
        for i, item in enumerate(self.items):
            item[0].config(text=table_data[i]['item'])
            item[1].set(table_data[i]['amount'])
            item[2].delete(0, tk.END)
            item[2].insert(0, f"{table_data[i]['price']:.2f}")
            item[3].set(table_data[i]['reason'])
            item[4].delete(0, tk.END)
            item[4].insert(0, table_data[i]['comment'])

        self.total.config(text=f"Total payment: {total:.2f} SEK")


class BartenderPanel(BaseView):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent, current_language, current_resolution)

        self.current_language = current_language

        self.current_table = 0
        self.remove_command = None
        self.value_changed_command = None
        
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


        
        self.panic_button = tk.Button(user_panic_frame, text="Panic", bg="red", fg="white", font=("Arial", 12, "bold"))
        self.panic_button.pack(side='right', expand=True, fill='both')
        
        self.table_frames = []
        self.table_frame = tk.Frame(self, bg='white')
        self.table_frame.pack(fill='both', expand=True)
        
        
        # Frame for holding 4 action buttons at corners
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", fill="both", expand=True)

        # Configure grid to evenly distribute buttons (2x2)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.rowconfigure(0, weight=1)

        # Button at bottom-left (Single Payment)
        self.single_payment_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["single payment"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.single_payment_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Button at bottom-right (Group Payment)
        self.group_payment_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["group payment"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.group_payment_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)


    def _add_table(self, table_number, table_data=[], total=0):
        table_frame = TableFrame(self.table_frame, table_number, table_data, total, self.value_changed_command, self.remove_command, self.focus_changed)
        table_frame.pack(fill='x', pady=10)
        self.table_frames.append(table_frame)

    def _clear_tables(self):
        for table_frame in self.table_frames:
            table_frame.destroy()
        self.table_frames = []

    def set_value_changed_command(self, command):
        self.value_changed_command = command

    def set_remove_command(self, command):
        self.remove_command = command

    def get_values(self):
        return [table.get_values() for table in self.table_frames]
    
    def focus_changed(self, table_id):
        self.table_frames[self.current_table].config(borderwidth=0)
        self.current_table = table_id
        self.table_frames[self.current_table].config(borderwidth=2, relief='solid')
    
    def update_value(self, tables):
        for i, data in enumerate(tables):
            total = sum([item['amount'] * item['price'] for item in data])
            self.table_frames[i].set_values(data, total)


    def update_table(self, tables, current_table=0):
        """
        Update the table data
        
        Args:
            tables (list): List of dictionaries containing table data
            e.g. [[{'item': 'item1', 'price': 10, 'comment': 'comment1'}, {'item': 'item2', 'price': 20, 'comment': 'comment2'}]]
        """
        self._clear_tables()
        for i, data in enumerate(tables):
            total = sum([item['price'] for item in data])
            self._add_table(i+1, data, total)
        self.focus_changed(current_table)
        
# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bartender Panel")
    panel = BartenderPanel(root, "English", 1)
    panel.pack(fill='both', expand=True, padx=10, pady=10)
    panel.update_table([[{'item': 'item1', 'price': 10, 'reason': 'Normal', 'comment': 'comment1'}, {'item': 'item2', 'price': 20, 'reason': 'Normal', 'comment': 'comment2'}], [], []])
    root.mainloop()
