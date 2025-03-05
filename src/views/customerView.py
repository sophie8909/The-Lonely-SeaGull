import tkinter as tk
from tkinter import messagebox, ttk
from models.language import LANGUAGE


class CustomerView(tk.Frame):
    def __init__(self, parent, current_language):
        super().__init__(parent)
        self.current_language = current_language

        self.shopping_cart = tk.Listbox()
        

        # Combo box for selecting different system language
        self.combo = ttk.Combobox(self, state="readonly", values=["English", "Svenska", "中文"], height=2, width=10)
        self.combo.pack(padx=5)
        self.combo.current(0)
        # self.combo.bind("<<ComboboxSelected>>", self.selection_changed)

        # Search bar
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = ttk.Entry(self.search_frame, width=40)
        self.search_entry.pack(side="left", padx=5)

        self.search_button = ttk.Button(self.search_frame, text=LANGUAGE[self.current_language]["search"])
        self.search_button.pack(side="left")

        # Select label (filter buttons)
        self.filter_frame = tk.Frame(self)
        self.filter_frame.pack(fill="x", padx=10)

        # TODO: Add filter buttons
        self.filters = ["magenta", "iced beer", "discount", "alcohol free"]
        self.filter_buttons = []
        for filter_name in self.filters:
            btn = ttk.Button(self.filter_frame, text=filter_name)
            btn.pack(side="left", padx=5)
            self.filter_buttons.append(btn)
        
        # Main view area (menu display)
        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(self.menu_frame)
        self.scrollbar = ttk.Scrollbar(self.menu_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.menu_container = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.menu_container, anchor="nw")

        # update the scroll region to the size of the frame
        self.menu_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Right side buttons
        self.side_frame = tk.Frame(self)
        self.side_frame.pack(side="right", padx=20, fill="y")
        

        self.add_friends_btn = ttk.Button(self.side_frame, text=LANGUAGE[self.current_language]["add friends"])
        self.add_friends_btn.pack(pady=5)

        self.confirm_btn = ttk.Button(self.side_frame, text=LANGUAGE[self.current_language]["confirm"])
        self.confirm_btn.pack(pady=5)
        
        # self.undo_label = tk.Button(self.side_frame, text=LANGUAGE[self.current_language]["undo"]).pack()
        # self.redo_label = tk.Button(self.side_frame, text=LANGUAGE[self.current_language]["redo"]).pack()
    


    def displat_menu_item(self, item, row, col):
        item_frame = tk.Frame(self.menu_container, relief=tk.RAISED, borderwidth=1)
        item_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        item_label = tk.Label(item_frame, text=item["name"])
        item_label.pack()

        item_price = tk.Label(item_frame, text=item["price"])
        item_price.pack()

        item_button = tk.Button(item_frame, text="Add to Cart")
        item_button.pack()

    # def hide_widgets(self):
    #     self.combo.pack_forget()
    #     self.beer_menu_label.pack_forget()
    #     self.beer_menu_frame.pack_forget()
    #     self.menu_label.pack_forget()
    #     for beer in self.beers_list:
    #         beer.pack_forget()
    #     self.cart_label.pack_forget()
    #     self.shopping_cart.pack_forget()
    #     self.checkout_language_label.pack_forget()
    #     self.undo_label.pack_forget()
    #     self.redo_label.pack_forget()
        

    def update_beer_menu(self, beers):
        # for widget in self.beer_menu_frame.winfo_children():
        #     self.beers_list.clear()
        #     widget.destroy()
        for beer in self.beers_list:
            beer.destroy()
        self.beers_list.clear()
        for beer in beers:
            beer_label = tk.Label(self.beer_menu_frame, text=f"{beer['name']} - {beer['price']} SEK", relief=tk.RAISED, padx=5, pady=5)
            beer_label.pack(pady=5)
            self.beers_list.append(beer_label)
            # self.beer_label.bind("<ButtonPress-1>", lambda e, b=beer: self.add_to_cart(b))

    def update_language(self):
        self.beer_menu_label.config(text=LANGUAGE[self.current_language]["beer menu"])
        self.menu_label.config(text=LANGUAGE[self.current_language]["menu"])
        self.cart_label.config(text=LANGUAGE[self.current_language]["cart"])
        self.checkout_language_label.config(text=LANGUAGE[self.current_language]["checkout"])
        self.undo_label.config(text=LANGUAGE[self.current_language]["undo"])
        self.redo_label.config(text=LANGUAGE[self.current_language]["redo"])
        

        
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Customer Ordering Interface")
#     root.geometry("1920x1280")
    
#     ui = CustomerView(root, LAGN, "English")
#     ui.pack()
#     root.mainloop()