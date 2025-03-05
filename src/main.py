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
w = 0
h = 0
x = 0
y = 0

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

    def change_res_27(self):
        # global w,h,x,y
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        w = screen_width * 0.9
        h = screen_height * 0.9
        x = (screen_width / 2) - (w / 2)
        y = (screen_height / 2) - (h / 2)

        self.root.geometry(str(int(w)) + "x" + str(int(h)) + "+" + str(int(x)) + "+" + str(int(y)))
        print("screen_width:", w)
        print("screen_height:", h)

    def change_res_9(self):
        # global w, h,x,y
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        w = screen_width  * 0.5
        h = screen_height * 0.5
        x = (screen_width/2) - (w/2)
        y = (screen_height/2) - (h/2)

        self.root.geometry(str(int(w)) + "x" + str(int(h)) + "+" + str(int(x)) + "+" + str(int(y)))

        print("screen_width:", w)
        print("screen_height:", h)
        print("x:", x)
        print("y:", y)
        
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


    def create_widgets(self):
        self.root.title("Login Interface")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        w = screen_width * 0.9
        h = screen_height * 0.9
        x = (screen_width / 2) - (w / 2)
        y = (screen_height / 2) - (h / 2)

        self.root.geometry(str(int(w)) + "x" + str(int(h)) + "+" + str(int(x)) + "+" + str(int(y)))
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
        self.button = tk.Button(self.root, text=LANGUAGES[current_language]["login"], command=self.login)
        self.button.pack(pady=20)
        self.button.config(text=LANGUAGES[current_language]["login"])

        # 27 inch display button
        self.button1 = tk.Button(self.root, text="27 inch display", command=self.change_res_27)
        self.button1.pack(pady=20)

        # 9 inch display button
        self.button2 = tk.Button(self.root, text="9 inch display", command=self.change_res_9)
        self.button2.pack(pady=20)



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
