import tkinter as tk
from tkinter import font
from models.style import style


class BaseView(tk.Frame):
    """ Base class for all views in the application
    This class contains the default font and color settings for the application
    """
    def __init__(self, parent, current_language, current_resolution, *args, **kwargs):
        super().__init__(parent, bg=style["background_color"], *args, **kwargs)

        self.current_language = current_language
        self.current_resolution = current_resolution

        # setting color
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

        # setting font
        self.default_font = self._create_font(parent, style["default_font"])
        self.header_font = self._create_font(parent, style["header_font"])

    def _create_font(self, root, font_info):
        """Helper function to create a font with fallback"""
        try:
            return font.Font(root=root, family=font_info["family"], size=font_info["size"], weight=font_info.get("weight", "normal"))
        except:
            return font.Font(root=root, family=font_info["fallback_family"], size=font_info["size"], weight=font_info.get("weight", "normal"))
