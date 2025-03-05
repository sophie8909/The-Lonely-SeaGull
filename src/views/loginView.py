import tkinter as tk
from tkinter import messagebox, ttk
from models.language import LANGUAGE


class LoginView(tk.Frame):
    def __init__(self, parent, current_language):
        super().__init__(parent)

    # def create_widgets(self):
        # Combo box for selecting different system language
        
        self.combo = ttk.Combobox(self, state="readonly", values=["English", "Swedish", "Chinese"], height=2, width=10)
        self.combo.pack(padx=5)
        self.combo.current(0)
        # self.combo.bind("<<ComboboxSelected>>", self.selection_changed)

        # Create a frame for the login form
        self.frame = tk.Frame(self, bg="#d3d3d3")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Username label and entry
        self.username_label = tk.Label(self.frame, text="User name", bg="#d3d3d3").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ttk.Entry(self.frame, width=25)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password label and entry
        self.password_label = tk.Label(self.frame, text="Password", bg="#d3d3d3").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ttk.Entry(self.frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        
        # Buttons
        self.btn_frame = tk.Frame(self.frame, bg="#d3d3d3")
        self.btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.login_button = ttk.Button(self.btn_frame, text="Login")
        self.login_button.pack(side="left", padx=5)

        self.guest_button = ttk.Button(self.btn_frame, text="Continue as a Guest")
        self.guest_button.pack(side="left", padx=5)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    # def hide_widgets(self):
    #     self.combo.pack_forget()
    #     self.frame.place_forget()
    #     self.btn_frame.grid_forget()
    #     self.login_button.pack_forget()
    #     self.guest_button.pack_forget()

