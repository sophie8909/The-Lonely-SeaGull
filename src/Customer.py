import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

# Simulated beer data
SIMULATED_BEERS = [
    (1, "Pale Ale", 49.99),
    (2, "Stout", 59.99),
    (3, "Lager", 39.99),
    (4, "IPA", 54.99)
]

def fetch_beers():
    return SIMULATED_BEERS

def add_to_cart(beer):
    shopping_cart.insert(tk.END, f"{beer[1]} - {beer[2]} SEK")

def order_food():
    return "Your food has been ordered!"

def order_drink():
    return "Your drink has been ordered!"

def order_vip_food():
    return "Your VIP food has been ordered!"

def view_account_balance():
    return "Your balance is: $100"

def pay_from_account():
    return "Payment has been made from your account!"

def get_customer_menu(user_role):
    menu = {
        "food": order_food,
        "drink": order_drink,
        "beers": fetch_beers
    }
    if user_role == "vip":
        menu.update({
            "vip_food": order_vip_food,
            "balance": view_account_balance,
            "pay": pay_from_account
        })
    return menu

def open_customer_interface():
    global shopping_cart
    customer_window = tk.Toplevel()
    customer_window.title("Customer Ordering Interface")
    customer_window.geometry("600x400")
    
    tk.Label(customer_window, text="Beer Menu", font=("Arial", 16)).pack(pady=5)
    
    beer_frame = tk.Frame(customer_window)
    beer_frame.pack(side=tk.LEFT, padx=10, pady=10)
    
    for beer in fetch_beers():
        beer_label = tk.Label(beer_frame, text=f"{beer[1]} - {beer[2]} SEK", relief=tk.RAISED, padx=5, pady=5)
        beer_label.pack(pady=2, fill=tk.X)
        beer_label.bind("<ButtonPress-1>", lambda e, b=beer: start_drag(e, b))
    
    cart_frame = tk.Frame(customer_window, relief=tk.SUNKEN, borderwidth=2)
    cart_frame.pack(side=tk.RIGHT, padx=10, pady=10)
    
    tk.Label(cart_frame, text="Shopping Cart", font=("Arial", 14)).pack()
    shopping_cart = tk.Listbox(cart_frame, width=40, height=10)
    shopping_cart.pack()
    
    customer_window.mainloop()

def start_drag(event, beer):
    event.widget.master.tk.call("tkdnd::drag", event.widget, "text/plain", beer)

def on_drop(event):
    item = event.data
    shopping_cart.insert(tk.END, item)
