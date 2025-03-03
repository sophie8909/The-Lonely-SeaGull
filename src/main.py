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


# Load language from JSON file
def load_language():
    global LANGUAGES
    with open("language.json", "r", encoding="utf-8") as file:
        LANGUAGES = json.load(file)
    


def close_application():
    root.destroy()
    sys.exit()

class LoginInterface:
    def __init__(self, root):
        self.root = root
        
    def login(self):
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


    def selection_changed(self, event):
        current_language = self.combo.get()
        self.button.config(text=LANGUAGES[current_language]["login"])
        self.label1.config(text=LANGUAGES[current_language]["username"])
        self.label2.config(text=LANGUAGES[current_language]["password"])


    



if __name__ == "__main__":
    load_language()
    # Create main application window
    root = TkinterDnD.Tk()
    
    # Create instance for Customer, Owner, Bartender, and VIP
    global customer
    customer = Customer.Customer(LANGUAGES, current_language)
    # owner = Owner.Owner()
    # bartender = Bartender.Bartender()
    # vip = VIP.VIP()

    # Create login interface
    login_interface = LoginInterface(root)
    login_interface.create_widgets()

    # Run the application
    root.mainloop()
