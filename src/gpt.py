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
    {"name": "Pale Ale", "brewery": "BrewCo", "country": "Sweden", "type": "Ale", "strength": "5.0%",
     "serving_size": "Bottle", "price": 49.99},
    {"name": "Stout", "brewery": "DarkBrew", "country": "Ireland", "type": "Stout", "strength": "6.5%",
     "serving_size": "Tap", "price": 59.99},
    {"name": "Lager", "brewery": "GoldenBrew", "country": "Germany", "type": "Lager", "strength": "4.7%",
     "serving_size": "Bottle", "price": 39.99},
    {"name": "IPA", "brewery": "HopHouse", "country": "USA", "type": "IPA", "strength": "7.2%", "serving_size": "Tap",
     "price": 54.99}
]

# Global Variables
user_role = None
current_language = "English"
order_history = []
redo_stack = []

# Language options
LANGUAGES = {
    "English": {"login": "Log in", "logout": "Log out", "menu": "Menu", "cart": "Shopping Cart",
                "checkout": "Checkout", '<--': "Undo", '-->': "Redo", 'username': 'Username', 'password': 'Password'},
    "Swedish": {"login": "Logga in", "logout": "Logga ut", "menu": "Meny", "cart": "Kundvagn", "checkout": "Betala",
                '<--': "Ångra", '-->': "Gör igen", 'username': 'Användarnamn', 'password': 'Lösenord'},
    "Chinese": {"login": "登录", "logout": "登出", "menu": "菜单", "cart": "购物车", "checkout": "结账", '<--': "撤消",
            '-->': "重做", 'username': '用户名', 'password': '密码'}
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
        shopping_cart.insert(tk.END, f"{item['name']} ({item['brewery']}) - {item['price']} SEK")
        order_history.append(item)

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

    tk.Button(right_frame, text=LANGUAGES[current_language]["checkout"], command=lambda: messagebox.showinfo("Order", "Order placed successfully!")) \
        .pack(pady=10)

    tk.Button(right_frame, text=LANGUAGES[current_language]["<--"], command=undo_last_action).pack()
    tk.Button(right_frame, text=LANGUAGES[current_language]["-->"], command=redo_last_action).pack()

def close_application():
    root.destroy()
    sys.exit()

def selection_changed(event):
    global current_language

    selection = combo.get()
    if selection == "English":
        current_language = "English"
        button.config(text=LANGUAGES[current_language]["login"])
        label1.config(text=LANGUAGES[current_language]["username"])
        label2.config(text=LANGUAGES[current_language]["password"])
    elif selection == "Swedish":
        current_language = "Swedish"
        button.config(text=LANGUAGES[current_language]["login"])
        label1.config(text=LANGUAGES[current_language]["username"])
        label2.config(text=LANGUAGES[current_language]["password"])
    elif selection == "Chinese":
        current_language = "Chinese"
        button.config(text=LANGUAGES[current_language]["login"])
        label1.config(text=LANGUAGES[current_language]["username"])
        label2.config(text=LANGUAGES[current_language]["password"])

# Create main application window
root = TkinterDnD.Tk()
root.title("Login Interface")
root.geometry("300x200")
root.protocol("WM_DELETE_WINDOW", close_application)

# Combo box for selecting different system language
combo = ttk.Combobox(state="readonly", values=["English", "Swedish", "Chinese"], height=2, width=10)
combo.pack(padx=5)
combo.current(0)
combo.bind("<<ComboboxSelected>>", selection_changed)

# Username label and entry
label1 = tk.Label(root, text=LANGUAGES[current_language]["username"])
label1.pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

# Password label and entry
label2 = tk.Label(root, text=LANGUAGES[current_language]["password"])
label2.pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

# Login button
button = tk.Button(root, text=LANGUAGES[current_language]["login"], command=login)
button.pack(pady=20)
button.config(text=LANGUAGES[current_language]["login"])

# Run the application
root.mainloop()
