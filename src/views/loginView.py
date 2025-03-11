import tkinter as tk
from tkinter import messagebox, ttk

from models.language import LANGUAGE


class LoginView(tk.Frame):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent)
        self.res_label = None
        self.language_label = None
        self.logout_button = None
        self.res_combo = None
        self.login_combo = None
        self.current_language = current_language
        self.current_resolution = current_resolution

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

    def settings_login_view(self):
        settings_frame = tk.Frame(self, bg="#035BAC")
        settings_frame.pack(side="top", anchor="e")

        # Combo box for selecting different system language
        self.language_label = tk.Label(settings_frame, text=LANGUAGE[self.current_language]["language"], bg="#d3d3d3")
        self.language_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.login_combo = ttk.Combobox(settings_frame, state="readonly", values=["English", "Română", "中文"], height=2, width=8)
        self.login_combo.grid(row=0, column=1, padx=10, pady=10)
        self.login_combo.current(int(LANGUAGE[self.current_language]["index"]))

        # Combo box for different display resolution sizes
        self.res_label = tk.Label(settings_frame, text=LANGUAGE[self.current_language]["resolution"], bg="#d3d3d3")
        self.res_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        self.res_combo = ttk.Combobox(settings_frame, state="readonly", values=["27\"", "9\""], height=2, width=3)
        self.res_combo.grid(row=0, column=3, padx=10, pady=10)
        self.res_combo.current(self.current_resolution)

        self.logout_button = ttk.Button(settings_frame, text=LANGUAGE[self.current_language]["logout"])
        self.logout_button.grid(row=0, column=4, padx=10, pady=10)
