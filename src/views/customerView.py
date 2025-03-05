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
        
        self.beer_menu_label = tk.Label(self, text=LANGUAGE[self.current_language]["beer menu"], font=("Arial", 16)).pack(pady=5)
        
        
        self.beer_menu_frame = tk.Frame(self, width=300, relief=tk.SUNKEN, borderwidth=2)
        self.beer_menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.menu_label = tk.Label(self.beer_menu_frame, text=LANGUAGE[self.current_language]["menu"], font=("Arial", 16)).pack(pady=5)
        self.beers_list = []


        right_frame = tk.Frame(self, relief=tk.SUNKEN, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.cart_label = tk.Label(right_frame, text=LANGUAGE[self.current_language]["cart"], font=("Arial", 14)).pack()
        self.shopping_cart = tk.Listbox(right_frame, width=50, height=20)
        self.shopping_cart.pack()

        self.checkout_language_label = tk.Button(right_frame, text=LANGUAGE[self.current_language]["checkout"], command=lambda: messagebox.showinfo("Order", "Order placed successfully!")) \
            .pack(pady=10)

        self.undo_label = tk.Button(right_frame, text=LANGUAGE[self.current_language]["undo"]).pack()
        self.redo_label = tk.Button(right_frame, text=LANGUAGE[self.current_language]["redo"]).pack()
    #     

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