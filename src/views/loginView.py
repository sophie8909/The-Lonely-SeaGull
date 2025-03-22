# =============================================================================
# loginView.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao, Darius Loga, Yuxie Liu
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: The login view with all the widgets for the whole system
# =======================================================

# Import the necessary libraries
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Local imports
from models.language import LANGUAGE
from views.baseView import BaseView
from views.components.settings import Settings


class LoginView(BaseView):
    """ The login view class

        Here are all the widgets that are going to be available for the login view

        Attributes:
            BaseView: the inherited class BaseView
    """

    def __init__(self, parent, current_language, current_resolution):
        """ Initial method

            Args:
                parent: used to get the tk window/frame
                current_language: used to get the current language of the system
                current_resolution: used to get the current resolution of the window
        """

        super().__init__(parent, current_language, current_resolution) # inherit from BaseView

        # trying to use the style functionality from tkinter, working only for ttk components
        style = ttk.Style()
        style.configure("BTN.TButton", background=self.light_green_label, foreground=self.green_button, font=self.default_font, relief="flat")

        # Load an image to be used as background
        # Did it also in the change_res method from MainController
        # resolution not being direct proportional to the screen display
        self.image = Image.open("./assets/boat.jpg")
        screen_width = int(parent.winfo_screenwidth())
        screen_height = int(parent.winfo_screenheight() - (0.036 * parent.winfo_screenheight()))

        # Resize the image using resize() method
        self.resize_image = self.image.resize((screen_width, screen_height))
        self.img = ImageTk.PhotoImage(self.resize_image)

        # Setting the background image to the window frame
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

        # Frame for some buttons
        self.btn_frame = tk.Frame(self.frame, bg=self.primary_color)
        self.btn_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # Login and Guest buttons
        self.login_button = ttk.Button(self.btn_frame, text=LANGUAGE[self.current_language]["login"], style="BTN.TButton")
        self.login_button.pack(side="left")

        self.guest_button = ttk.Button(self.btn_frame, text=LANGUAGE[self.current_language]["guest_btn"], style="BTN.TButton")
        self.guest_button.pack(side="right")

        # Added the view for language and display size settings
        self.settings_widget = Settings(self, self.current_language, self.current_resolution)
        self.settings_widget.pack(side="top", anchor="e")

    def update_login_language(self, current_lgn):
        """ Update UI text based on selected language

            Args:
                current_lgn: current language of the system
        """

        self.settings_widget.language_label.config(text=LANGUAGE[current_lgn]["language"])
        self.settings_widget.res_label.config(text=LANGUAGE[current_lgn]["resolution"])
        self.settings_widget.logout_button.config(text=LANGUAGE[current_lgn]["logout"])
        self.username_label.config(text=LANGUAGE[current_lgn]["username"])
        self.password_label.config(text=LANGUAGE[current_lgn]["password"])
        self.login_button.config(text=LANGUAGE[current_lgn]["login"])
        self.guest_button.config(text=LANGUAGE[current_lgn]["guest_btn"])
        self.login_welcome_label.config(text=LANGUAGE[current_lgn]["login_welcome"])