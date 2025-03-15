import tkinter as tk
from tkinter import ttk

class TableFrame(tk.Frame):
    def __init__(self, parent, table_number, table_data=[], total=0, remove_command=None, **kwargs):
        super().__init__(parent, bg='lightgray', **kwargs)

        title_frame = tk.Frame(self, bg='lightgray')
        tk.Label(title_frame, text=f"Table {table_number}", font=("Arial", 10, "bold"), bg='lightgray').pack(side='left', fill='x')
        tk.Button(title_frame, text="X", bg='red', fg='white', command=lambda: remove_command(table_number-1) if remove_command else None).pack(side='right')
        title_frame.pack(fill='x')
        
        # Items, Prices, Comments Headers
        headers_frame = tk.Frame(self, bg='lightgray')
        headers_frame.pack(fill='x')
        
        tk.Label(headers_frame, text="Items", bg='lightgray').grid(row=0, column=0, padx=5)
        tk.Label(headers_frame, text="Prices", bg='lightgray').grid(row=0, column=1, padx=5)
        tk.Label(headers_frame, text="Comments", bg='lightgray').grid(row=0, column=2, padx=5)
        for row, data in enumerate(table_data):
            tk.Label(headers_frame, text=data['item'], bg='lightgray').grid(row=row+1, column=0, padx=5)
            tk.Label(headers_frame, text=data['price'], bg='lightgray').grid(row=row+1, column=1, padx=5)
            tk.Label(headers_frame, text=data['comment'], bg='lightgray').grid(row=row+1, column=2, padx=5)

        
        # Total Payment
        tk.Label(self, text=f"Total payment: {total:.2f} SEK", bg='lightgray').pack(anchor='w', pady=5)

class BartenderPannel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white', padx=10, pady=10)
        
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
        for i in range(2):
            table_frame = TableFrame(self.table_frame, i+1)
            table_frame.pack(fill='x', pady=10)
            self.table_frames.append(table_frame)
        
        # Payment Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(side='bottom', fill='x', pady=10)
        
        button_width = 15  # Ensure all buttons are the same size
        
        self.on_house_button = tk.Button(button_frame, text="On house", bg='blue', fg='white', width=button_width)
        self.on_house_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        self.compensation_button = tk.Button(button_frame, text="Compensation", bg='blue', fg='white', width=button_width)
        self.compensation_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        self.single_payment_button = tk.Button(button_frame, text="Single payment", bg='blue', fg='white', width=button_width)
        self.single_payment_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        
        self.group_payment_button = tk.Button(button_frame, text="Group payment", bg='blue', fg='white', width=button_width)
        self.group_payment_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Make buttons expand horizontally
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

    def _add_table(self, table_number, table_data=[]):
        table_frame = TableFrame(self.table_frame, table_number, table_data)
        table_frame.pack(fill='x', pady=10)
        self.table_frames.append(table_frame)

    def _clear_tables(self):
        for table_frame in self.table_frames:
            table_frame.destroy()
        self.table_frames = []

    def update(self, table_data):
        self._clear_tables()
        for i, table in enumerate(table_data):
            self._add_table(i+1, table)
        
# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bartender Panel")
    panel = BartenderPannel(root)
    panel.pack(fill='both', expand=True, padx=10, pady=10)
    root.mainloop()
