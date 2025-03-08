import tkinter as tk
from tkinter import messagebox, ttk, font
from models.language import LANGUAGE
from views.components.product import ProductCard, ShoppingCart
from views.customerView import CustomerView

class VIPView(CustomerView):
    def __init__(self, parent, current_language):
        super().__init__(parent, current_language)
        