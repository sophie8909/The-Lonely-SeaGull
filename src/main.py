import tkinter as tk
from tkinter import messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys
import Customer
import Owner
import Bartender
import VIP
import json

# Global Variables
user_role = None
current_language = "English"
order_history = []
redo_stack = []

# Simulated user data
USERS = {
    "admin": {"password": "password", "role": "bartender"},
    "owner": {"password": "password", "role": "owner"},
    "vip": {"password": "password", "role": "vip"},
    "customer": {"password": "password", "role": "customer"}
}

# Language options
LANGUAGES = {
    "English": {"login": "Log in", "logout": "Log out", "menu": "Menu", "cart": "Shopping Cart",
                "checkout": "Checkout", '<--': "Undo", '-->': "Redo", 'username': 'Username', 'password': 'Password'},
    "Swedish": {"login": "Logga in", "logout": "Logga ut", "menu": "Meny", "cart": "Kundvagn", "checkout": "Betala",
                '<--': "Ångra", '-->': "Gör igen", 'username': 'Användarnamn', 'password': 'Lösenord'},
    "Chinese": {"login": "登录", "logout": "登出", "menu": "菜单", "cart": "购物车", "checkout": "结账", '<--': "撤消",
            '-->': "重做", 'username': '用户名', 'password': '密码'}
}


def login():
    global user_role
    user_role = "customer"
    root.withdraw()

    # if username_entry.get() in USERS:
    #     if password_entry.get() == USERS[username_entry.get()]["password"]:
    #         user_role = USERS[username_entry.get()]["role"]
    #         messagebox.showinfo("Login", f"Welcome {username_entry.get()}!")
    #     else:
    #         messagebox.showerror("Login", "Invalid password!")
    # else:
    #     messagebox.showerror("Login", "Invalid username!")

    # open the main window
    if user_role == "customer":
        customer.open_customer_interface()
    # elif user_role == "owner":
    #     Owner.open_owner_interface()
    # elif user_role == "bartender":
    #     Bartender.open_bartender_interface()
    # elif user_role == "vip":
    #     VIP.open_vip_interface()

def close_application():
    root.destroy()
    sys.exit()

class LoginInterface:
    def __init__(self, root):
        self.root = root
        
    def selection_changed(self, event):
        current_language = self.combo.get()
        self.button.config(text=LANGUAGES[current_language]["login"])
        self.label1.config(text=LANGUAGES[current_language]["username"])
        self.label2.config(text=LANGUAGES[current_language]["password"])


    def create_widgets(self):
        self.root.title("Login Interface")
        self.root.geometry("300x200")
        self.root.protocol("WM_DELETE_WINDOW", close_application)

        # Combo box for selecting different system language
        self.combo = ttk.Combobox(self.root, state="readonly", values=["English", "Swedish", "Chinese"], height=2, width=10)
        self.combo.pack(padx=5)
        self.combo.current(0)
        self.combo.bind("<<ComboboxSelected>>", self.selection_changed)

        # Username label and entry
        self.label1 = tk.Label(self.root, text=LANGUAGES[current_language]["username"])
        self.label1.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        # Password label and entry
        self.label2 = tk.Label(self.root, text=LANGUAGES[current_language]["password"])
        self.label2.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        self.button = tk.Button(self.root, text=LANGUAGES[current_language]["login"], command=login)
        self.button.pack(pady=20)
        self.button.config(text=LANGUAGES[current_language]["login"])



if __name__ == "__main__":
    # Create main application window
    root = TkinterDnD.Tk()
    
    # Create instance for Customer, Owner, Bartender, and VIP
    global customer
    customer = Customer.Customer()
    # owner = Owner.Owner()
    # bartender = Bartender.Bartender()
    # vip = VIP.VIP()

    # Create login interface
    login_interface = LoginInterface(root)
    login_interface.create_widgets()

    # Run the application
    root.mainloop()
