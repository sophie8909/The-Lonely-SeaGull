import tkinter as tk
from tkinter import font, ttk

from models.language import LANGUAGE
from views.baseView import BaseView


# Class used for the language and display size settings, to change between them
class Settings(BaseView):
    def __init__(self, master, background_color, primary_color, default_font, current_language, current_resolution):
        tk.Frame.__init__(self, master)
        self.background_color = background_color
        self.primary_color = primary_color
        self.default_font = default_font
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

        # Combo box for selecting different system language
        self.language_label = tk.Label(self, text=LANGUAGE[self.current_language]["language"], bg="#d3d3d3")
        self.language_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.login_combo = ttk.Combobox(self, state="readonly", values=["English", "Română", "中文"], height=2, width=8)
        self.login_combo.grid(row=0, column=1, padx=10, pady=10)
        self.login_combo.current(int(LANGUAGE[self.current_language]["index"]))

        # Combo box for different display resolution sizes
        self.res_label = tk.Label(self, text=LANGUAGE[self.current_language]["resolution"], bg="#d3d3d3")
        self.res_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        self.res_combo = ttk.Combobox(self, state="readonly", values=["27\"", "9\""], height=2, width=3)
        self.res_combo.grid(row=0, column=3, padx=10, pady=10)
        self.res_combo.current(self.current_resolution)

        self.logout_button = ttk.Button(self, text=LANGUAGE[self.current_language]["logout"])
        self.logout_button.grid(row=0, column=4, padx=10, pady=10)

