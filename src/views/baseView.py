# =============================================================================
# product_card_manager.py
# =============================================================================
# @AUTHOR: Yuxie Liu, Darius Loga
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Have a base view class to be inherited by other classes also
# =======================================================
import tkinter as tk
from tkinter import font

# Local imports
from models.style import style


class BaseView(tk.Frame):
    """ The base view class

        Used to have a reusable class that can be inherited and store different styles

        Attributes:
            tk.Frame: the Frame class provided by the tkinter library
    """

    def __init__(self, parent, current_language, current_resolution, *args, **kwargs):
        """ Initial method

            Used to get all some style settings to be reusable throughout
            different views (login, customer, vip, bartender, owner) that can inherit this class

            Args:
                parent: used to get the tk window/frame
                current_language: used to get the current language of the system
                current_resolution: used to get the current resolution of the window
                *args: multiple arguments
                **kwargs: multiple arguments
        """

        super().__init__(parent, *args, **kwargs) # inherit from tk.Frame

        self.current_language = current_language
        self.current_resolution = current_resolution

        # setting color for different widgets to be used
        self.primary_color = style["primary_color"]
        self.light_primary = style["light_primary"]
        self.background_color = style["background_color"]
        self.light_gray = style["light_gray"]
        self.dark_text = style["dark_text"]
        self.light_icon = style["light_icon"]
        self.green_button = style["green_button"]
        self.light_green_button = style["light_green_button"]
        self.light_green_frame = style["light_green_frame"]
        self.light_green_label = style["light_green_label"]
        self.green_white = style["green_white"]
        self.dark_green = style["dark_green"]
        self.green = style["green"]
        self.light_green = style["light_green"]
        self.gray_green = style["gray_green"]
        self.light_gray_green = style["light_gray_green"]

        # setting for different fonts to be used
        self.default_font = self.create_font(parent, style["default_font"])
        self.header_font = self.create_font(parent, style["header_font"])

    def create_font(self, root, font_info):
        """ Helper function to create a font with fallback

            Args:
                root: used to get the tk window/frame
                font_info: font style to be used
        """
        try:
            return font.Font(root=root, family=font_info["family"], size=font_info["size"], weight=font_info.get("weight", "normal"))
        except:
            return font.Font(root=root, family=font_info["fallback_family"], size=font_info["size"], weight=font_info.get("weight", "normal"))
