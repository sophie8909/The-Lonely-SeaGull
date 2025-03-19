import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from models.language import LANGUAGE
from views.baseView import BaseView
from views.components.settings import Settings


class LoginView(BaseView):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent, current_language, current_resolution)

        style = ttk.Style()
        style.configure("BTN.TButton", background=self.light_green_label, foreground=self.green_button, font=self.default_font, relief="flat")

        # Show background image using label
        # Read the Image - do it in the change_res method
        self.image = Image.open("../assets/boat.jpg")
        screen_width = int(parent.winfo_screenwidth())
        screen_height = int(parent.winfo_screenheight() - (0.036 * parent.winfo_screenheight()))

        # Resize the image using resize() method
        self.resize_image = self.image.resize((screen_width, screen_height))

        self.img = ImageTk.PhotoImage(self.resize_image)
        self.login_background_label = tk.Label(self, image=self.img)
        self.login_background_label.place(x=-2, y=-2)

        # Create a frame for the login form
        self.frame = tk.Frame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome message label
        self.login_welcome_label = tk.Label(self.frame, text=LANGUAGE[self.current_language]["login_welcome"], font=self.default_font)
        self.login_welcome_label.grid(row=0, column=0, columnspan=2,padx=10, pady=10, sticky=tk.E+tk.W)

        # Username label and entry
        self.username_label = tk.Label(self.frame, text=LANGUAGE[self.current_language]["username"], fg=self.dark_green, font=self.default_font)
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ttk.Entry(self.frame, width=25, font=self.default_font)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        # Password label and entry
        self.password_label = tk.Label(self.frame, text=LANGUAGE[self.current_language]["password"], fg=self.dark_green, font=self.default_font)
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ttk.Entry(self.frame, width=25, show="*", font=self.default_font)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        self.btn_frame = tk.Frame(self.frame, bg=self.primary_color)
        self.btn_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # 用 tk.Button 替代 ttk.Button 來方便設計樣式
        self.login_button = ttk.Button(self.btn_frame, text=LANGUAGE[self.current_language]["login"], style="BTN.TButton")
        self.login_button.pack(side="left")

        self.guest_button = ttk.Button(self.btn_frame, text=LANGUAGE[self.current_language]["guest_btn"], style="BTN.TButton")
        self.guest_button.pack(side="right")

        # Added the view for language and display size settings
        self.settings_widget = Settings(self, self.dark_green, self.primary_color, self.default_font, self.current_language, self.current_resolution)
        self.settings_widget.pack(side="top", anchor="e")

    def update_login_language(self, current_lgn):
        """Update UI text based on selected language"""
        self.settings_widget.language_label.config(text=LANGUAGE[current_lgn]["language"])
        self.settings_widget.res_label.config(text=LANGUAGE[current_lgn]["resolution"])
        self.settings_widget.logout_button.config(text=LANGUAGE[current_lgn]["logout"])
        self.username_label.config(text=LANGUAGE[current_lgn]["username"])
        self.password_label.config(text=LANGUAGE[current_lgn]["password"])
        self.login_button.config(text=LANGUAGE[current_lgn]["login"])
        self.guest_button.config(text=LANGUAGE[current_lgn]["guest_btn"])
        self.login_welcome_label.config(text=LANGUAGE[current_lgn]["login_welcome"])