# =============================================================================
# product_card_manager.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Component for the product card of items to be visible only for bartender
# and owner
# =======================================================

# Import the necessary libraries
import tkinter as tk

# Local libraries
from models.language import LANGUAGE
from views.components.product_card import ProductCard

class ProductCardManager(ProductCard):
    """ The Product Card class

        Modified version of ProductCard for the bartender and owner to show the available stock,
        have a "Hidden Item" tag

        Attributes:
            ProductCard: the inherited class ProductCard
    """

    def __init__(self, master, row, col, background_color, primary_color, default_font, product, detail_frame, current_language, click_callback=None):
        """ Initial method

            Args:
                master: used to get the tk window/frame
                row: used to get the row
                col: used to get the column
                background_color: used to get the background color
                primary_color: used to get the primary color
                default_font: used to get the default font
                product: used to get the product
                detail_frame: used to get the detail frame
                current_language: used to get the current language of the system
                click_callback: callback to a click function on the product card
        """

        super().__init__(master, row, col, background_color, primary_color, default_font, product, detail_frame, current_language, click_callback) # inherit from ProductCard
        self.product_card.config(height=312)

        self.left_num_frame = tk.Frame(self.product_card)
        self.left_num_frame.pack(side="left", fill="both", expand=True)

        # Number of the stock label to be displayed
        self.num_label = tk.Label(self.left_num_frame,
                                  text=self.product["Stock"], 
                                  font=default_font, 
                                  bg=background_color, 
                                  fg=primary_color)
        self.num_label.pack(side="left", fill="both", expand=True)
        # Label to display the "items left" text
        self.left_num_label = tk.Label(self.left_num_frame,
                                       text=LANGUAGE[self.current_language]["items left"], 
                                       font=default_font, 
                                       bg=background_color, 
                                       fg=primary_color)
        self.left_num_label.pack(side="left", fill="both", expand=True)

        # Change the colour of the text to red when low on stock (below or equal 5)
        if int(product["Stock"]) <= 5:
            self.num_label.config(fg="red")
            self.left_num_label.config(fg="red")

        # Bind to click a button to add items to cart (using the modified view of the product card)
        self.add_to_cart_btn.bind("<Button-1>", self.select_item_click)
        
        # if an item has the hidden tag true, add a label to show it is hidden
        if product["Hidden"]: 
            self.hidden_label = tk.Label(self.product_card, 
                                         text=LANGUAGE[self.current_language]["hide item"], 
                                         font=default_font, 
                                         bg=background_color, 
                                         fg=primary_color)
            self.hidden_label.pack(side="bottom", fill="both", expand=True)

    def select_item_click(self, event=None):
        """ Select item

            Callback to a click event to add this item also to the shopping cart/list

            Args:
                event: not used, but to be here to bind the functionality to a widget
        """

        if self.click_callback:
            self.click_callback(self)

# Main function that can be used to run this .py file individually to test some functionalities
if __name__ == "__main__":
    from views.components.shopping_cart import ShoppingCart
    
    root = tk.Tk()
    root.geometry("400x400")
    root.wm_attributes("-topmost", True)
    shopping_cart = ShoppingCart(root, "gray", "blue")
    shopping_cart.pack(side="right", fill="both", expand=True, pady=10)
    product_frame = tk.Frame(root, bg="white")
    product_frame.pack(side="left", fill="both", expand=True, pady=10)
    for row in range(2):
        for col in range(3):
            product_card = ProductCardManager(product_frame, row, col, "white", "blue", "Arial 10")
    root.mainloop()