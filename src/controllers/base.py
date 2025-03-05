import tkinter as tk
class BaseController:
    def __init__(self, tk_root, current_language):
        self.tk_root = tk_root
        self.current_language = current_language
        self.current_controller = None
        pass

    