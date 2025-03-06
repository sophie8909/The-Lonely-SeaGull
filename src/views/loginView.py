import tkinter as tk
from tkinter import messagebox, ttk

from models.language import LANGUAGE


class LoginView(tk.Frame):
    def __init__(self, parent, current_language):
        super().__init__(parent)
        self.current_language = current_language

        # # resize the window frame
        # screen_width = parent.winfo_screenwidth()
        # screen_height = parent.winfo_screenheight()
        #
        # w = screen_width * 0.5
        # h = screen_height * 0.5
        # x = (screen_width / 2) - (w / 2)
        # y = (screen_height / 2) - (h / 2)
        #
        # parent.geometry(str(int(w)) + "x" + str(int(h)) + "+" + str(int(x)) + "+" + str(int(y)))
        #
        # print("screen_width:", w)
        # print("screen_height:", h)
        # print("x:", x)
        # print("y:", y)

        # Combo box for selecting different system language
        self.language_label = tk.Label(self, text=LANGUAGE[self.current_language]["language"], bg="#d3d3d3")
        self.language_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.combo = ttk.Combobox(self, state="readonly", values=["English", "Svenska", "中文"], height=2, width=10)
        self.combo.grid(row=0, column=1, padx=10, pady=10)
        self.combo.bind("<<ComboboxSelected>>", self.update_language)

        # Create a frame for the login form
        self.frame = tk.Frame(self, bg="#d3d3d3")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Username label and entry
        self.username_label = tk.Label(self.frame, text=LANGUAGE[self.current_language]["username"], bg="#d3d3d3")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ttk.Entry(self.frame, width=25)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password label and entry
        self.password_label = tk.Label(self.frame, text=LANGUAGE[self.current_language]["password"], bg="#d3d3d3")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ttk.Entry(self.frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        
        # Buttons
        self.btn_frame = tk.Frame(self.frame, bg="#d3d3d3")
        self.btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.login_button = ttk.Button(self.btn_frame, text=LANGUAGE[self.current_language]["login"])
        self.login_button.pack(side="left", padx=5)

        self.guest_button = ttk.Button(self.btn_frame, text=LANGUAGE[self.current_language]["guest_btn"])
        self.guest_button.pack(side="left", padx=5)

        # 27 inch display button
        self.button1 = tk.Button(self.btn_frame, text="27 inch display")
        self.button1.pack(pady=20)

        # 9 inch display button
        self.button2 = tk.Button(self.btn_frame, text="9 inch display")
        self.button2.pack(pady=20)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def update_language(self, event):
        self.current_language = self.combo.get()
        self.username_label.config(text=LANGUAGE[self.current_language]["username"])
        self.password_label.config(text=LANGUAGE[self.current_language]["password"])
        self.login_button.config(text=LANGUAGE[self.current_language]["login"])
        self.guest_button.config(text=LANGUAGE[self.current_language]["guest_btn"])
        self.language_label.config(text=LANGUAGE[self.current_language]["language"])

    # def hide_widgets(self):
    #     self.combo.pack_forget()
    #     self.frame.place_forget()
    #     self.btn_frame.grid_forget()
    #     self.login_button.pack_forget()
    #     self.guest_button.pack_forget()

