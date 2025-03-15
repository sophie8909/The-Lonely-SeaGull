import tkinter as tk
from tkinter import font, ttk

from models.language import LANGUAGE




class Dragable:
    _drag_threshold = 20

    def __init__(self, widget):
        self.widget = widget
        self.widgets = []
        self.ghost = None
        self._drag_data = {"x": 0, "y": 0}


    def set_anchor_widget(self, widget):
        self.anchor_widget = widget


    def add_draggable(self, widgets):
        for widget in widgets:
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.do_drag)
            widget.bind("<ButtonRelease-1>", self.stop_drag)
            self.widgets.append(widget)


    def start_drag(self, event):
        self._drag_data["x"] = event.x_root
        self._drag_data["y"] = event.y_root
        if hasattr(self, "create_ghost_card"):
            self.ghost = self.create_ghost_card()
            self.ghost.place(x=self.anchor_widget.winfo_rootx(), y=self.anchor_widget.winfo_rooty())


    def do_drag(self, event):
        if self.ghost:
            dx = event.x_root - self._drag_data["x"]
            dy = event.y_root - self._drag_data["y"]
            if abs(dx) < self._drag_threshold and abs(dy) < self._drag_threshold:
                return
            # new_x = self.anchor_widget.winfo_x() - self.anchor_widget.master.winfo_x() + dx
            # new_y = self.anchor_widget.winfo_y() - self.anchor_widget.master.winfo_y() + dy
            # new_x = self.anchor_widget.winfo_x()+ dx
            # new_y = self.anchor_widget.winfo_y()+ dy
            new_x = self.anchor_widget.winfo_rootx() + dx
            new_y = self.anchor_widget.winfo_rooty() + dy
            self.ghost.place(x=new_x, y=new_y)


    def stop_drag(self, event):
        if self.ghost:
            self.ghost.destroy()
            self.ghost = None
            below_widget = self.widget.winfo_containing(event.x_root, event.y_root)
             
            while not hasattr(below_widget, "on_drop"):
                if below_widget.master is None:
                    return
                below_widget = below_widget.master
                
            below_widget.on_drop(self.widget)

# Class used for the language and display size settings, to change between them

class ProductCard(Dragable, tk.Frame):
    drag_threshold = 20

    def __init__(self, master, row, col, background_color, primary_color, default_font, product, detail_frame, click_callback=None):
        tk.Frame.__init__(self, master)
        Dragable.__init__(self, self)
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

        self.product_card = tk.Frame(self.product_frame, bg=self.background_color, width=223, height=262, bd=1, relief="solid")
        self.product_card.grid(row=row, column=col, padx=10, pady=10)
        self.product_card.pack_propagate(False)

        self.product_image = tk.PhotoImage(file="../assets/beer.png")
        self.product_image = self.product_image.subsample(3)
        self.product_image_label = tk.Label(self.product_card, image=self.product_image, bg=self.background_color)
        self.product_image_label.image = self.product_image
        self.product_image_label.pack(pady=0)

        self.product_name = tk.Label(self.product_card, text=self.product['Name'], bg=self.background_color, font=self.default_font)
        self.product_name.pack(pady=(30, 5))


        price_info_frame = tk.Frame(self.product_card, bg=self.background_color)
        price_info_frame.pack(pady=5)

        # info button
        self.info_btn = tk.Button(price_info_frame, text="ℹ️", bg=self.primary_color, fg="white", width=2, height=2)
        self.info_btn.pack(side="left", padx=(10, 0))
        self.info_btn.bind("<Button-1>", self.info_click)
        # price
        self.product_price = tk.Label(price_info_frame, text=self.product['Price'], bg=self.background_color, font=self.default_font)
        self.product_price.pack(side="left")

        if product["VIP"]:
            self.product_vip_label = tk.Label(price_info_frame, text="VIP", bg=self.primary_color, fg="white", font=self.default_font)
            self.product_vip_label.pack(side="left", anchor="w", padx=(10, 0))

        self.add_draggable([self.product_card, self.product_image_label, self.product_name, self.product_price])

        # add to cart
        self.add_to_cart_btn = tk.Button(price_info_frame, text="+", bg=self.primary_color, fg="white", padx=10, pady=5)
        self.add_to_cart_btn.pack(side="right")
        self.add_to_cart_btn.bind("<Button-1>", self.add_to_cart_click)  # 綁定事件

        self.set_anchor_widget(self.product_card)
    
    def add_to_cart_click(self, event):
        if self.click_callback:
            self.click_callback(self)

    def info_click(self, event):
        print(self.product)
        self.show_item_detail(self.product)


    def create_ghost_card(self):
        root = self.master

        while not isinstance(root, tk.Tk):
            root = root.master

        ghost = tk.Frame(root, bg=self.background_color, width=223, height=262, bd=1, relief="solid")
        ghost.pack_propagate(False)
        ghost_image = tk.PhotoImage(file="../assets/beer.png")
        ghost_image = ghost_image.subsample(3)

        ghost_image_label = tk.Label(ghost, image=ghost_image, bg=self.background_color)
        ghost_image_label.image = ghost_image
        ghost_image_label.pack(pady=0)
        ghost_name = tk.Label(ghost, text=self.product["Name"], bg=self.background_color, font=self.default_font)
        ghost_name.pack(pady=(30,5))
        ghost_price = tk.Label(ghost, text=self.product["Price"], bg=self.background_color, font=self.default_font)
        ghost_price.pack(pady=5)
        ghost_button = tk.Button(ghost, text="Add to Cart", bg=self.primary_color, fg="white", padx=10, pady=5)
        ghost_button.pack(pady=20)

        return ghost

    def show_item_detail(self, item_info):
        # clear the detail frame
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        item_label = tk.Label(self.detail_frame, text=item_info["Name"], font=self.default_font, bg=self.background_color)
        item_label.pack()
        
        item_price = tk.Label(self.detail_frame, text=item_info["Price"], font=self.default_font, bg=self.background_color)
        item_price.pack()
        
        for info in item_info:
            if info not in ["Name", "Price", "VIP"]:
                if info == "Allergens":
                    allergens_label = tk.Label(self.detail_frame, text=f"{info}: {', '.join(item_info[info])}", font=self.default_font, bg=self.background_color)
                    allergens_label.pack()
                else:
                    info_label = tk.Label(self.detail_frame, text=f"{info}: {item_info[info]}", font=self.default_font, bg=self.background_color)
                    info_label.pack()


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
            product_card = ProductCard(product_frame, row, col, "white", "blue", "Arial 10")
    root.mainloop()