import tkinter as tk
from tkinter import messagebox, ttk, font
import types

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


class ShoppingCart(tk.Frame):
    def __init__(self, master, background_color, primary_color, default_font):
        tk.Frame.__init__(self, master)
        self.background_color = background_color
        self.primary_color = primary_color
        self.default_font = default_font
        self.current_person = 0

        # Define colors
        self.primary_color = "#035BAC"
        self.light_primary = "#D5E5F5"  # Approximation of rgba(3, 91, 172, 0.27)
        self.background_color = "#FFFFFF"
        self.light_gray = "#D9D9D9"
        self.dark_text = "#5A5A5A"  # Approximation of rgba(0, 0, 0, 0.65)
        self.light_icon = "#BEBDBD"  # Approximation of rgba(151, 148, 148, 0.5)
        
        # Try to set up fonts (if not available, fallback to system fonts)
        try:
            self.default_font = font.Font(family="Roboto", size=14)
            self.header_font = font.Font(family="Roboto", size=24, weight="normal")
        except:
            self.default_font = font.Font(family="Arial", size=14)
            self.header_font = font.Font(family="Arial", size=24, weight="normal")
        # Create a frame for the bottom elements
        self.bottom_frame = tk.Frame(self, bg=self.background_color)
        self.bottom_frame.pack(fill="x", pady=0, side="bottom")

        # Person selection area (at the top)
        self.cart_frame = tk.Frame(self, bg=self.background_color)
        self.cart_frame.pack(fill="both", pady=0, side="top", expand=True)

        self.person_frame_top = tk.Frame(self.cart_frame, bg=self.background_color)
        self.person_frame_top.pack(fill="x", side="top")
        self.items_frame = tk.Frame(self.cart_frame, bg=self.background_color)
        self.items_frame.pack(fill="both", side="top", expand=True)
        self.person_frame_bottom = tk.Frame(self.cart_frame, bg=self.background_color)
        self.person_frame_bottom.pack(fill="x", side="bottom")

        self.person_top = []
        self.person_bottom = []
        self.items = []
        self.totals = []
        

        self.total_label = tk.Label(self.bottom_frame, text="Total: 0 SEK", bg=self.background_color, font=self.header_font)
        self.total_label.pack(fill="x", pady=0, side="bottom")
        
        # Undo/Redo section (at the bottom)
        self.action_frame = tk.Frame(self.bottom_frame, bg=self.background_color)
        self.action_frame.pack(fill="x", pady=10)
        
        self.undo_btn = tk.Button(self.action_frame, text="undo", 
                               bg=self.light_gray, font=("Inter", 12))
        self.undo_btn.pack(side="left", padx=5)
        
        self.redo_btn = tk.Button(self.action_frame, text="redo", 
                               bg=self.light_gray, font=("Inter", 12))
        self.redo_btn.pack(side="right", padx=5)
        
        # Add friends button (second from bottom)
        self.add_friends_btn = tk.Button(self.bottom_frame, text="add friends",
                                       bg=self.primary_color, fg="white", font=self.header_font,
                                       bd=0, padx=16, pady=10)
        self.add_friends_btn.pack(fill="x", pady=10)
        # Confirm button (third from bottom)
        self.confirm_btn = tk.Button(self.bottom_frame, text="confirm",
                                   bg=self.primary_color, fg="white", font=self.header_font,
                                   bd=0, padx=16, pady=10)
        self.confirm_btn.pack(fill="x", pady=10)
        


        # test item
        # self.add_person()
        # self.add_item("Test item1", 50, 2)
        # self.add_item("Test item2", 10.99, 1)


    def add_person(self, remove_command=None):
        person_container = tk.Frame(self.person_frame_top, bg=self.light_gray, pady=5, padx=10)
        person_container.pack(fill="x", pady=10)
        
        person_label = tk.Label(person_container, text=f"Person {len(self.person_top)+1}", bg=self.light_gray, font=("Inter", 12))
        person_label.pack(side="left")
        remove_btn = tk.Button(person_container, text="✕", bg=self.light_gray, bd=1, command=lambda person_label=person_label: remove_command(person_label))
        remove_btn.pack(side="right")
        total_label = tk.Label(person_container, text="0 SEK", bg=self.light_gray, font=("Inter", 12), padx=10)
        total_label.pack(side="right")
        self.person_top.append(person_container)

        person_container = tk.Frame(self.person_frame_bottom, bg=self.light_gray, pady=5, padx=10)
        # person_container.pack(fill="x", pady=10)
        
        person_label = tk.Label(person_container, text=f"Person {len(self.person_bottom)+1}", bg=self.light_gray, font=("Inter", 12))
        person_label.pack(side="left")
        total_label = tk.Label(person_container, text="0 SEK", bg=self.light_gray, font=("Inter", 12))
        total_label.pack(side="right")
        remove_btn = tk.Button(person_container, text="✕", bg=self.light_gray, bd=0)
        remove_btn.pack(side="right")
        self.person_bottom.append(person_container)
        self.items.append([])
        self.totals.append(0)

    def add_item(self, item_name, price, amount=1):
        item_frame = tk.Frame(self.items_frame, bg=self.background_color, pady=0, padx=0)
        item_frame.pack(fill="x", side="top")
        item_name_label = tk.Label(item_frame, text=item_name, bg=self.background_color, font=("Inter", 12))
        item_name_label.pack(side="left")
        item_price_label = tk.Label(item_frame, text=f"{amount}x {price} = {amount*price} SEK", bg=self.background_color, font=("Inter", 12))
        item_price_label.pack(side="right")
        self.items[self.current_person].append(item_frame)
        self.totals[self.current_person] += float(price) * int(amount)
        self.person_top[self.current_person].children["!label2"].config(text=f"{self.totals[self.current_person]} SEK")
        self.person_bottom[self.current_person].children["!label2"].config(text=f"{self.totals[self.current_person]} SEK")
        self.total_label.config(text=f"Total: {sum(self.totals)} SEK")

    def set_person(self, current_person):
        for i in range(len(self.person_top)):
            if i <= current_person:
                self.person_top[i].pack(fill="x", pady=10)
                self.person_bottom[i].pack_forget()
            else:
                self.person_top[i].pack_forget()
                self.person_bottom[i].pack(fill="x", pady=10)
        if self.current_person < len(self.items):
            for item in self.items[self.current_person]:
                print(item.children['!label'].cget("text"))
                item.pack_forget()
        self.current_person = current_person
        for item in self.items[self.current_person]:
            item.pack(fill="x", side="top")

    def remove_person(self, i):
        self.person_top[i].destroy()
        self.person_top.pop(i)
        for i, person in enumerate(self.person_top):
            person.children["!label"].config(text=f"Person {i+1}")
        self.person_bottom[i].destroy()
        self.person_bottom.pop(i)
        for i, person in enumerate(self.person_bottom):
            person.children["!label"].config(text=f"Person {i+1}")
        for item in self.items[i]:
            item.destroy()
        self.items.pop(i)
        self.totals.pop(i)
        
    
    def set_on_drop(self, on_drop):
        self.on_drop = on_drop
        self.cart_frame.on_drop = on_drop
        self.person_frame_top.on_drop = on_drop
        self.items_frame.on_drop = on_drop
        self.person_frame_bottom.on_drop = on_drop

    def clear_cart(self):
        for person in self.person_top:
            person.destroy()
        for person in self.person_bottom:
            person.destroy()
        for item in self.items:
            for widget in item:
                widget.destroy()
        self.person_top = []
        self.person_bottom = []
        self.items = []
        self.totals = []
        self.current_person = 0
        self.total_label.config(text="Total: 0 SEK")

    # pop up window for confirm order
    def double_check_confirm(self):
        # pop up window in center for double check the order
        self.confirm_window = tk.Toplevel(self)
        self.confirm_window.title("Confirm Order")
        self.confirm_window.geometry("300x200")
        self.confirm_window.resizable(False, False)
        # set the position of the pop up window
        x = self.confirm_window.winfo_screenwidth() // 2 - 150
        y = self.confirm_window.winfo_screenheight() // 2 - 100
        self.confirm_window.geometry(f"+{x}+{y}")

        # force the user to confirm the order
        self.confirm_window.grab_set() # block the main window
        self.confirm_window.focus_set() # focus on the pop up window
        self.confirm_window.protocol("WM_DELETE_WINDOW", self.prevent_closing)

        confirm_label = tk.Label(self.confirm_window, text="Are you sure to confirm the order?", font=("Inter", 12))
        confirm_label.pack(pady=20)

        self.confirm_yes_btn = tk.Button(self.confirm_window, text="Yes", bg=self.primary_color, fg="white", font=("Inter", 12))
        self.confirm_yes_btn.pack(side="left", padx=20)

        self.confirm_no_btn = tk.Button(self.confirm_window, text="No", bg=self.primary_color, fg="white", font=("Inter", 12))
        self.confirm_no_btn.pack(side="right", padx=20)    
    
    def confirm_window_close(self):
        self.confirm_window.destroy()


    def prevent_closing(self):
        """ Prevent closing the confirmation window without an explicit choice """
        pass  # Do nothing, forcing user interaction

class ProductCard(Dragable, tk.Frame):
    drag_threshold = 20
    def __init__(self, master, row, col, background_color, primary_color, default_font, product, click_callback=None):
        tk.Frame.__init__(self, master)
        Dragable.__init__(self, self)
        self.product_frame = master
        self.background_color = background_color
        self.primary_color = primary_color
        self.default_font = default_font
        self.row = row
        self.col = col
        self._is_dragging = False

        self.product_card = tk.Frame(self.product_frame, bg=self.background_color, width=223, height=262, bd=1, relief="solid")
        self.product_card.grid(row=row, column=col, padx=10, pady=10)
        self.product_card.pack_propagate(False)

        self.product_image = tk.PhotoImage(file="../assets/beer.png")
        self.product_image = self.product_image.subsample(3)
        self.product_image_label = tk.Label(self.product_card, image=self.product_image, bg=self.background_color)
        self.product_image_label.image = self.product_image
        self.product_image_label.pack(pady=0)

        self.product_name = tk.Label(self.product_card, text=product['Name'], bg=self.background_color, font=self.default_font)
        self.product_name.pack(pady=(30, 5))
        
        self.product_price = tk.Label(self.product_card, text=product['Price'], bg=self.background_color, font=self.default_font)
        self.product_price.pack(pady=5)

        for widget in [self.product_card, self.product_image_label, self.product_name, self.product_price]:
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.do_drag)
            widget.bind("<ButtonRelease-1>", self.stop_drag)

        self.set_anchor_widget(self.product_card)
    def click(self):
        print(f"Product {self.row*3+self.col+1} clicked")
        
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
        ghost_name = tk.Label(ghost, text=f"Product {self.row*3+self.col+1}", bg=self.background_color, font=self.default_font)
        ghost_name.pack(pady=(30,5))
        ghost_price = tk.Label(ghost, text="50 SEK", bg=self.background_color, font=self.default_font)
        ghost_price.pack(pady=5)
        ghost_button = tk.Button(ghost, text="Add to Cart", bg=self.primary_color, fg="white", padx=10, pady=5)
        ghost_button.pack(pady=20)
        return ghost

if __name__ == "__main__":
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