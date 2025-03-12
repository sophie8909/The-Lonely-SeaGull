import tkinter as tk
from tkinter import ttk, font

from models.language import LANGUAGE
from views.components.product import Settings


class LoginView(tk.Frame):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent)
        self.current_language = current_language
        self.current_resolution = current_resolution

        # Define colors
        self.primary_color = "#035BAC"
        self.light_primary = "#D5E5F5"  # Approximation of rgba(3, 91, 172, 0.27)
        self.background_color = "#FFFFFF"
        self.light_gray = "#D9D9D9"
        self.dark_text = "#5A5A5A"  # Approximation of rgba(0, 0, 0, 0.65)
        self.light_icon = "#BEBDBD"  # Approximation of rgba(151, 148, 148, 0.5)

        # Try to set up fonts (if not available, fallback to system fonts)
        try:
            self.default_font = font.Font(family="Roboto", size=14)
            self.header_font = font.Font(family="Roboto", size=24, weight="normal")
        except:
            self.default_font = font.Font(family="Arial", size=14)
            self.header_font = font.Font(family="Arial", size=24, weight="normal")

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

        # Added the view for language and display size settings
        self.settings_widget = Settings(self, self.background_color, self.primary_color, self.default_font, self.current_language, self.current_resolution)
        self.settings_widget.pack(side="top", anchor="e")

