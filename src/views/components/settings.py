# =============================================================================
# settings.py
# =============================================================================
# @AUTHOR: Darius Loga
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Frame for the settings of the whole application (change language and
# application display view)
# =======================================================

# Import the necessary libraries
import tkinter as tk
from tkinter import ttk

# Local imports
from models.language import LANGUAGE
from views.baseView import BaseView


class Settings(BaseView):
    """ The settings class

        Used for the language and display size settings, to change between them

        Attributes:
            BaseView: the inherited class BaseView
    """

    def __init__(self, master, current_language, current_resolution):
        """ Initial method

            Used to get all the widgets to be reusable throughout the application in the
            different views (login, customer, vip, bartender, owner)

            Args:
                master: used to get the tk window/frame
                current_language: used to get the current language of the system
                current_resolution: used to get the current resolution of the window
        """

        super().__init__(master, current_language, current_resolution) # inherit from BaseView

        # Label to display the langauge options
        self.language_label = tk.Label(self, text=LANGUAGE[self.current_language]["language"], bg=self.dark_green)
        self.language_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        # Combo box for selecting different system language options
        self.login_combo = ttk.Combobox(self, state="readonly", values=["English", "Română", "中文"], height=2, width=8)
        self.login_combo.grid(row=0, column=1, padx=10, pady=10)
        # show the current options when switching through different views
        self.login_combo.current(int(LANGUAGE[self.current_language]["index"]))

        # Label to display the resolution options
        self.res_label = tk.Label(self, text=LANGUAGE[self.current_language]["resolution"], bg=self.dark_green)
        self.res_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Combo box for different display resolution sizes
        self.res_combo = ttk.Combobox(self, state="readonly", values=["27\"", "9\""], height=2, width=3)
        self.res_combo.grid(row=0, column=3, padx=10, pady=10)
        self.res_combo.current(self.current_resolution)

        # Log out button
        self.logout_button = ttk.Button(self, text=LANGUAGE[self.current_language]["logout"])
        self.logout_button.grid(row=0, column=4, padx=10, pady=10)
