import tkinter as tk
from tkinter import font, ttk

from models.language import LANGUAGE
from views.components.product_card import ProductCard

class ProductCardManager(ProductCard):

    def __init__(self, master, row, col, background_color, primary_color, default_font, product, detail_frame, current_language, click_callback=None):
        super().__init__(master, row, col, background_color, primary_color, default_font, product, detail_frame, current_language, click_callback)
        self.product_card.config(height=312)
        self.left_num_frame = tk.Frame(self.product_card)
        self.left_num_frame.pack(side="left", fill="both", expand=True)
        self.num_label = tk.Label(self.left_num_frame, 
                                  text=self.product["Stock"], 
                                  font=default_font, 
                                  bg=background_color, 
                                  fg=primary_color)
        self.num_label.pack(side="left", fill="both", expand=True)
        self.left_num_label = tk.Label(self.left_num_frame, 
                                       text=LANGUAGE[self.current_language]["items left"], 
                                       font=default_font, 
                                       bg=background_color, 
                                       fg=primary_color)
        self.left_num_label.pack(side="left", fill="both", expand=True)

        self.add_to_cart_btn.bind("<Button-1>", self.select_item_click)
        
        # if product["Hidden"] add a label to show it is hidden
        if product["Hidden"]: 
            self.hidden_label = tk.Label(self.product_card, 
                                         text=LANGUAGE[self.current_language]["hide item"], 
                                         font=default_font, 
                                         bg=background_color, 
                                         fg=primary_color)
            self.hidden_label.pack(side="bottom", fill="both", expand=True)


    def select_item_click(self, event):
        if self.click_callback:
            self.click_callback(self)

if __name__ == "__main__":
    from views.components.shopping_cart import ShoppingCart
    
    root = tk.Tk()
    root.geometry("400x400")
    root.wm_attributes("-topmost", True)
    shopping_cart = ShoppingCart(root, "gray", "blue", "Arial 10")
    shopping_cart.pack(side="right", fill="both", expand=True, pady=10)
    product_frame = tk.Frame(root, bg="white")
    product_frame.pack(side="left", fill="both", expand=True, pady=10)
    for row in range(2):
        for col in range(3):
            product_card = ProductCardManager(product_frame, row, col, "white", "blue", "Arial 10")
    root.mainloop()