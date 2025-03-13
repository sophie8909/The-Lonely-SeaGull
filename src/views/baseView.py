import tkinter as tk
from tkinter import ttk, font
from views.style import style


class BaseView(tk.Frame):
    def __init__(self, parent, current_language, current_resolution):
        super().__init__(parent, bg=style["background_color"])

        self.current_language = current_language
        self.current_resolution = current_resolution

        # setting color
        self.primary_color = style["primary_color"]
        self.light_primary = style["light_primary"]
        self.background_color = style["background_color"]
        self.light_gray = style["light_gray"]
        self.dark_text = style["dark_text"]
        self.light_icon = style["light_icon"]

        # setting font
        self.default_font = self._create_font(parent, style["default_font"])
        self.header_font = self._create_font(parent, style["header_font"])

    def _create_font(self, root, font_info):
        """Helper function to create a font with fallback"""
        try:
            return font.Font(root=root, family=font_info["family"], size=font_info["size"], weight=font_info.get("weight", "normal"))
        except:
            return font.Font(root=root, family=font_info["fallback_family"], size=font_info["size"], weight=font_info.get("weight", "normal"))

