import tkinter as tk

from models.language import LANGUAGE
from views.components.product_card import ProductCard

class ProductCardManager(ProductCard):
    """
    This class is a subclass of ProductCard, it is used to display the product card in the customer view.
    It has a select_item_click method that is used to handle the click event of the add to cart button.
    args:
        master: tk.Frame
        row: int
        col: int
        background_color: str
        primary_color: str
        default_font: str
        product: dict
        detail_frame: tk.Frame
        current_language: str
        click_callback: function
    """
    def __init__(self, master, row, col, background_color, primary_color, default_font, product, detail_frame, current_language, click_callback=None):
        super().__init__(master, row, col, background_color, primary_color, default_font, product, detail_frame, current_language, click_callback)
        self.product_card.config(height=312)
        
        # add a label to show the number of items left
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

        # if the stock is less than or equal to 5, change the color of the label to red
        if int(product["Stock"]) <= 5:
            self.num_label.config(fg="red")
            self.left_num_label.config(fg="red")

        # add a button to add the item to the cart
        self.add_to_cart_btn.bind("<Button-1>", self.select_item_click)
        
        # if product["Hidden"] add a label to show it is hidden
        if product["Hidden"]: 
            self.hidden_label = tk.Label(self.product_card, 
                                         text=LANGUAGE[self.current_language]["hide item"], 
                                         font=default_font, 
                                         bg=background_color, 
                                         fg=primary_color)
            self.hidden_label.pack(side="bottom", fill="both", expand=True)

    # method used to handle the click event of the add to cart button
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