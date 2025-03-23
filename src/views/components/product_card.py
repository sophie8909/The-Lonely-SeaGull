# =============================================================================
# product_card.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: The component for all the views that uses a menu frame
# =======================================================

# Import the necessary libraries
import tkinter as tk
from PIL import Image, ImageTk

# Local imports
from models.language import LANGUAGE


class Draggable:
    """ Class to make the product card a draggable for the drag and drop functionality """
    _drag_threshold = 20 # threshold for dragging event

    def __init__(self, widget):
        """ Initial method

            Args:
                widget: which widget to drag
        """

        self.widget = widget
        self.widgets = []
        self.ghost = None # display also a ghost card to see some info of that draggable object
        self._drag_data = {"x": 0, "y": 0}

    def set_anchor_widget(self, widget):
        """ Set anchor widget """
        self.anchor_widget = widget

    def add_draggable(self, widgets):
        """ Make the widgets draggable
        Args:
            widgets: which widget to drag
        """

        # Bind events to the widgets
        for widget in widgets:
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.do_drag)
            widget.bind("<ButtonRelease-1>", self.stop_drag)
            self.widgets.append(widget)

    def start_drag(self, event):
        """ Start dragging the widget
        Args:
            event: tk.Event
        """

        self._drag_data["x"] = event.x_root
        self._drag_data["y"] = event.y_root

        # Create a ghost card
        if hasattr(self, "create_ghost_card"):
            self.ghost = self.create_ghost_card()
            self.ghost.place(x=self.anchor_widget.winfo_rootx(), y=self.anchor_widget.winfo_rooty())

    def do_drag(self, event):
        """ Drag the widget
        Args:
            event: tk.Event
        """

        # If the ghost card is created, move it
        if self.ghost:
            dx = event.x_root - self._drag_data["x"]
            dy = event.y_root - self._drag_data["y"]
            if abs(dx) < self._drag_threshold and abs(dy) < self._drag_threshold:
                return
            new_x = self.anchor_widget.winfo_rootx() + dx
            new_y = self.anchor_widget.winfo_rooty() + dy
            self.ghost.place(x=new_x, y=new_y)

    def stop_drag(self, event):
        """ Stop dragging the widget
        Args:
            event: tk.Event
        """

        # If the ghost card is created, destroy it
        if self.ghost:
            self.ghost.destroy()
            self.ghost = None
            below_widget = self.widget.winfo_containing(event.x_root, event.y_root)
             
            while not hasattr(below_widget, "on_drop"):
                if below_widget.master is None:
                    return
                below_widget = below_widget.master
                
            below_widget.on_drop(self.widget)


class ProductCard(Draggable, tk.Frame):
    """ The product card frame component view class

        Here are all the widgets and functionalities that are going to be available
        for the product card component view

        Attributes:
            Draggable: the inherited class Draggable
            tk.Frame: the inherited class tk.Frame
    """

    def __init__(self, master, row, col, background_color, primary_color, default_font, product, detail_frame, current_language, click_callback=None):
        """ Initial method

            Args:
                master: used to get the tk window/frame
                row: row number
                col: column number
                background_color: background color
                primary_color: primary color
                default_font: default font
                product: product card
                detail_frame: detail frame
                current_language: used to get the current language of the system
                click_callback: used to get the click callback functionality
        """

        tk.Frame.__init__(self, master) # inherit from tk.Frame
        Draggable.__init__(self, self) # inherit from Draggable

        self.product_frame = master
        self.background_color = background_color
        self.primary_color = primary_color
        self.default_font = default_font
        self.row = row
        self.col = col
        self._is_dragging = False
        self.product = product
        self.detail_frame = detail_frame
        self.click_callback = click_callback
        self.current_language = current_language

        # Create the product card
        self.product_card = tk.Frame(self.product_frame, bg=self.background_color, width=223, height=262, bd=1, relief="solid")
        self.product_card.grid(row=row, column=col, padx=7, pady=7)
        self.product_card.pack_propagate(True)

        # Create the product card content
        # Image added to the label
        if self.product["Tag"] == "wine":
            image = Image.open("./assets/wine.png")
        elif self.product["Tag"] == "cocktail":
            image = Image.open("./assets/cocktail.png")
        elif self.product["Tag"] == "food":
            image = Image.open("./assets/food.png")
        else:
            image = Image.open("./assets/beer.png")
        
        fixed_size = (100, 100)
        image = image.resize(fixed_size) # resize the image to fit the product card
        self.product_image = ImageTk.PhotoImage(image)
        self.product_image_label = tk.Label(self.product_card, image=self.product_image, bg=self.background_color)
        self.product_image_label.image = self.product_image
        self.product_image_label.pack(pady=0)

        # Product name label
        self.product_name = tk.Label(self.product_card, text=self.product['Name'], bg=self.background_color, font=self.default_font)
        self.product_name.pack(pady=(30, 5))

        # Create the price info frame
        price_info_frame = tk.Frame(self.product_card, bg=self.background_color)
        price_info_frame.pack(pady=5)

        # Info button
        self.info_btn = tk.Button(price_info_frame, text="ℹ️", bg=self.primary_color, fg="white", width=2, height=2)
        self.info_btn.pack(side="left", padx=(10, 0))
        self.info_btn.bind("<Button-1>", self.info_click)

        # Price label
        self.product_price = tk.Label(price_info_frame, text=self.product['Price'], bg=self.background_color, font=self.default_font)
        self.product_price.pack(side="left")

        # VIP label
        if product["VIP"]:
            self.product_vip_label = tk.Label(price_info_frame, text="VIP", bg=self.primary_color, fg="white", font=self.default_font)
            self.product_vip_label.pack(side="left", anchor="w", padx=(10, 0))

        # Add draggable event
        self.add_draggable([self.product_card, self.product_image_label, self.product_name, self.product_price])

        # Add to cart button
        self.add_to_cart_btn = tk.Button(price_info_frame, text="+", bg=self.primary_color, fg="white", padx=10, pady=5)
        self.add_to_cart_btn.pack(side="right")
        self.add_to_cart_btn.bind("<Button-1>", self.add_to_cart_click)  # bind the mouse click to add to cart event

        self.set_anchor_widget(self.product_card)

    def add_to_cart_click(self, event=None):
        """ Add to cart button click functionality
        Args:
            event: not used, but to be here to bind the functionality to a widget
        """
        if self.click_callback:
            self.click_callback(self)

    def info_click(self, event=None):
        """ Show the detail of the product
        Args:
            event: not used, but to be here to bind the functionality to a widget
        """
        print(self.product)
        self.show_item_detail(self.product, self.current_language)

    def create_ghost_card(self):
        """ Method used to handle the drop event and create the ghost card
        Returns:
            Returns the ghost card
        """
        root = self.master

        while not isinstance(root, tk.Tk):
            # While not an instance of the class tk.Tk
            root = root.master

        # Ghost frame
        ghost = tk.Frame(root, bg=self.background_color, width=223, height=262, bd=1, relief="solid")
        ghost.pack_propagate(False)

        # Creation of the ghost images for the ghost card also depending on the tag
        if self.product["Tag"] == "wine":
            ghost_image = Image.open("./assets/wine.png")
        elif self.product["Tag"] == "cocktail":
            ghost_image = Image.open("./assets/cocktail.png")
        elif self.product["Tag"] == "food":
            ghost_image = Image.open("./assets/food.png")
        else:
            ghost_image = Image.open("./assets/beer.png")

        fixed_size = (100, 100)
        ghost_image = ghost_image.resize(fixed_size)  # resize the image to fit the product card
        ghost_final_image = ImageTk.PhotoImage(ghost_image)

        # Ghost label containing the above-created ghost images
        ghost_image_label = tk.Label(ghost, image=ghost_final_image, bg=self.background_color)
        ghost_image_label.image = ghost_final_image
        ghost_image_label.pack(pady=0)

        # Ghost item name label
        ghost_name = tk.Label(ghost, text=self.product["Name"], bg=self.background_color, font=self.default_font)
        ghost_name.pack(pady=(30,5))

        # Ghost item price label
        ghost_price = tk.Label(ghost, text=self.product["Price"], bg=self.background_color, font=self.default_font)
        ghost_price.pack(pady=5)

        return ghost

    def show_item_detail(self, item_info, language):
        """ Show the detail of the product
        Args:
            item_info: dict, the information of the product
            language: str, the current language
        """

        # Clear the detail frame
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        # Create the detail info
        # Item name
        item_label = tk.Label(self.detail_frame, text=item_info["Name"], font=self.default_font, bg=self.background_color)
        item_label.pack()
        
        # Item price
        item_price = tk.Label(self.detail_frame, text=item_info["Price"], font=self.default_font, bg=self.background_color)
        item_price.pack()
        
        # Item info
        for info in item_info:
            if info not in ["Name", "Price", "VIP", "Stock", "Hidden"]:
                # If the info is allergens, ingredients or contents/recipe, show them in a separate way
                if info == "Allergens":
                    allergens_label = tk.Label(self.detail_frame, 
                                               text=f"{LANGUAGE[language][info]}: {', '.join(item_info[info])}",
                                               font=self.default_font, 
                                               anchor="w",
                                               bg=self.background_color)
                    allergens_label.pack()
                elif info == "Ingredients" or info == "Contents/Recipe":
                    separate_info = ""
                    for one_info in item_info[info]:
                        separate_info += '\n' + str(one_info)

                    info_label = tk.Label(self.detail_frame, 
                                          text=f"{LANGUAGE[language][info]}: {separate_info}",
                                          font=self.default_font, 
                                          anchor="w",
                                          bg=self.background_color)
                    info_label.pack()
                else:
                    info_label = tk.Label(self.detail_frame,
                                          text=f"{LANGUAGE[language][info]}: {item_info[info]}",
                                          font=self.default_font,
                                          anchor="w",
                                          bg=self.background_color)
                    info_label.pack()

# Example usage
if __name__ == "__main__":
    from views.components.shopping_cart import ShoppingCart
    
    root = tk.Tk()
    root.geometry("400x400")
    root.wm_attributes("-topmost", True)
    shopping_cart = ShoppingCart(root, "gray", "blue", "Arial 10", current_language="English", current_resolution=1)
    shopping_cart.pack(side="right", fill="both", expand=True, pady=10)
    product_frame = tk.Frame(root, bg="white")
    product_frame.pack(side="left", fill="both", expand=True, pady=10)
    for row in range(2):
        for col in range(3):
            product_card = ProductCard(product_frame, row, col, "white", "blue", "Arial 10")
    root.mainloop()