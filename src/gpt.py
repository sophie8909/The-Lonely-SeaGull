import tkinter as tk
from tkinter import messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys

# Simulated user data
USERS = {
    "admin": {"password": "password", "role": "bartender"},
    "owner": {"password": "password", "role": "owner"},
    "vip": {"password": "password", "role": "vip", "balance": 500},
    "customer": {"password": "password", "role": "customer"}
}

# Simulated beer data with detailed information
SIMULATED_BEERS = [
    {"name": "Pale Ale", "brewery": "BrewCo", "country": "Sweden", "type": "Ale", "strength": "5.0%", "serving_size": "Bottle", "price": 49.99},
    {"name": "Stout", "brewery": "DarkBrew", "country": "Ireland", "type": "Stout", "strength": "6.5%", "serving_size": "Tap", "price": 59.99},
    {"name": "Lager", "brewery": "GoldenBrew", "country": "Germany", "type": "Lager", "strength": "4.7%", "serving_size": "Bottle", "price": 39.99},
    {"name": "IPA", "brewery": "HopHouse", "country": "USA", "type": "IPA", "strength": "7.2%", "serving_size": "Tap", "price": 54.99}
]

# Global Variables
user_role = None
current_language = "English"
order_history = []
redo_stack = []

# Language options
LANGUAGES = {
    "English": {"login": "Login", "logout": "Logout", "menu": "Menu", "cart": "Shopping Cart", "checkout": "Checkout"},
    "Swedish": {"login": "Logga in", "logout": "Logga ut", "menu": "Meny", "cart": "Kundvagn", "checkout": "Betala"},
    "Chinese": {"login": "登录", "logout": "登出", "menu": "菜单", "cart": "购物车", "checkout": "结账"}
}

def fetch_beers():
    return SIMULATED_BEERS

def add_to_cart(beer):
    shopping_cart.insert(tk.END, f"{beer['name']} ({beer['brewery']}) - {beer['price']} SEK")
    order_history.append(beer)
    redo_stack.clear()

def undo_last_action():
    if order_history:
        last_item = order_history.pop()
        shopping_cart.delete(tk.END)
        redo_stack.append(last_item)

def redo_last_action():
    if redo_stack:
        item = redo_stack.pop()
        add_to_cart(item)

def login():
    global user_role
    username = username_entry.get()
    password = password_entry.get()
    
    if username in USERS and USERS[username]["password"] == password:
        user_role = USERS[username]["role"]
        root.withdraw()
        open_main_interface()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_main_interface():
    global shopping_cart
    main_window = tk.Toplevel()
    main_window.title("Main Interface")
    main_window.geometry("900x600")
    main_window.protocol("WM_DELETE_WINDOW", close_application)
    
    menu_frame = tk.Frame(main_window, width=300, relief=tk.SUNKEN, borderwidth=2)
    menu_frame.pack(side=tk.LEFT, fill=tk.Y)
    
    tk.Label(menu_frame, text=LANGUAGES[current_language]["menu"], font=("Arial", 16)).pack(pady=5)
    
    for beer in fetch_beers():
        beer_label = tk.Label(menu_frame, text=f"{beer['name']} - {beer['price']} SEK", relief=tk.RAISED, padx=5, pady=5)
        beer_label.pack(pady=5)
        beer_label.bind("<ButtonPress-1>", lambda e, b=beer: add_to_cart(b))
    
    right_frame = tk.Frame(main_window, relief=tk.SUNKEN, borderwidth=2)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    tk.Label(right_frame, text=LANGUAGES[current_language]["cart"], font=("Arial", 14)).pack()
    shopping_cart = tk.Listbox(right_frame, width=50, height=20)
    shopping_cart.pack()
    
    tk.Button(right_frame, text=LANGUAGES[current_language]["checkout"], command=lambda: messagebox.showinfo("Order", "Order placed successfully!"))\
        .pack(pady=10)
    
    tk.Button(right_frame, text="Undo", command=undo_last_action).pack()
    tk.Button(right_frame, text="Redo", command=redo_last_action).pack()

def close_application():
    root.destroy()
    sys.exit()

# Create main application window
root = TkinterDnD.Tk()
root.title("Login Interface")
root.geometry("300x200")
root.protocol("WM_DELETE_WINDOW", close_application)

# Username label and entry
tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

# Password label and entry
tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

# Login button
tk.Button(root, text="Login", command=login).pack(pady=20)

# Run the application
root.mainloop()
