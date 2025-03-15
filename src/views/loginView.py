import tkinter as tk
from tkinter import ttk, font

from models.language import LANGUAGE
from views.baseView import BaseView
from views.components.settings import Settings


class LoginView(BaseView):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent, current_language, current_resolution)

        style = ttk.Style()
        style.configure("BTN.TButton", background="white", foreground=self.primary_color, font=self.default_font, relief="flat")

        # Create a frame for the login form
        self.frame = tk.Frame(self, bg=self.light_gray)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Username label and entry
        self.username_label = tk.Label(self.frame, text=LANGUAGE[self.current_language]["username"], bg=self.primary_color, font=self.default_font, fg="white")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ttk.Entry(self.frame, width=25, font=self.default_font)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password label and entry
        self.password_label = tk.Label(self.frame, text=LANGUAGE[self.current_language]["password"], bg=self.primary_color, font=self.default_font, fg="white")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ttk.Entry(self.frame, width=25, show="*", font=self.default_font)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        self.btn_frame = tk.Frame(self.frame, bg=self.primary_color)
        self.btn_frame.grid(row=2, column=0, columnspan=3, pady=10)

        # 用 tk.Button 替代 ttk.Button 來方便設計樣式
        self.login_button = ttk.Button(self.btn_frame, text=LANGUAGE[self.current_language]["login"], style="BTN.TButton")
        self.login_button.pack(side="left")

        self.guest_button = ttk.Button(self.btn_frame, text=LANGUAGE[self.current_language]["guest_btn"], style="BTN.TButton")
        self.guest_button.pack(side="right")


        # Added the view for language and display size settings
        self.settings_widget = Settings(self, self.background_color, self.primary_color, self.default_font, self.current_language, self.current_resolution)
        self.settings_widget.pack(side="top", anchor="e")

