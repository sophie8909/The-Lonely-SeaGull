import tkinter as tk
from models.language import LANGUAGE
from views.baseView import BaseView


class ShoppingCart(BaseView):
    def __init__(self, master, current_language, current_resolution):
        super().__init__(master, current_language, current_resolution)
        # self.background_color = background_color
        # self.primary_color = primary_color
        # self.default_font = default_font
        self.current_language = current_language
        self.current_resolution = current_resolution

        # define person x button command
        self.remove_person_command = None

        # define person label click command
        self.current_person_command = None
        
        # Create a frame for the bottom elements
        self.bottom_frame = tk.Frame(self, bg=self.background_color)
        self.bottom_frame.pack(fill="x", pady=2, side="bottom")

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

        # Undo/Redo section (at the bottom)
        self.action_frame = tk.Frame(self.bottom_frame, bg=self.background_color)
        self.action_frame.pack(fill="x", pady=10)
        
        self.undo_btn = tk.Button(self.action_frame, text=LANGUAGE[self.current_language]["undo"],
                               bg=self.light_gray, font=("Inter", 12))
        self.undo_btn.pack(side="left", padx=5)
        
        self.redo_btn = tk.Button(self.action_frame, text=LANGUAGE[self.current_language]["redo"],
                               bg=self.light_gray, font=("Inter", 12))
        self.redo_btn.pack(side="right", padx=5)
        
        # Add friends button (second from bottom)
        self.add_friends_btn = tk.Button(self.bottom_frame, text=LANGUAGE[self.current_language]["add friends"],
                                       bg=self.primary_color, fg="white", font=self.header_font,
                                       bd=0, padx=16, pady=10)
        self.add_friends_btn.pack(fill="x", pady=10)
        # Confirm button (third from bottom)
        self.payment_frame = tk.Frame(self.bottom_frame, bg=self.background_color)
        self.payment_frame.pack(fill="x", pady=10)

        self.confirm_btn = tk.Button(self.payment_frame, text=LANGUAGE[self.current_language]["confirm"],
                                   bg=self.primary_color, fg="white", font=self.header_font,
                                   bd=0, padx=16, pady=10)
        self.confirm_btn.pack(fill="x", pady=10, side="top")

        # total
        self.total_frame = tk.Frame(self.payment_frame, bg=self.background_color)
        self.total_frame.pack(fill="x", pady=10, side="bottom")

        self.total_text_label = tk.Label(self.total_frame, text=LANGUAGE[self.current_language]["total"],
                                         bg=self.background_color, font=self.header_font)
        self.total_text_label.pack(fill="x", pady=0, side="left", anchor="center")

        self.total_price_label = tk.Label(self.total_frame, text="", bg=self.background_color, font=self.header_font)
        self.total_price_label.pack(fill="x", pady=0, side="right", anchor="center")

    def _add_person(self, person_frame, person_id, current_lgn, total=0):
        person_container = tk.Frame(person_frame, bg=self.light_gray, pady=5, padx=10)
        person_container.pack(fill="x", pady=10)

        # it has to be the current_lgn parameter in order to dynamically change the "Person" word
        # throughout the language changes
        self.person_label = tk.Label(person_container, text=LANGUAGE[current_lgn]["person"], bg=self.light_gray, font=("Inter", 12))
        self.person_label.pack(side="left")
        person_count_label = tk.Label(person_container, text=f"{person_id+1}", bg=self.light_gray, font=("Inter", 12))
        person_count_label.pack(side="left")
        remove_btn = tk.Button(person_container, text="X", bg=self.light_gray, bd=1, command=lambda: self.remove_person_command(person_id))
        remove_btn.pack(side="right")
        
        total_text = f"{total:.2f} SEK"
        total_label = tk.Label(person_container, text=total_text, bg=self.light_gray, font=("Inter", 12), padx=10)
        total_label.pack(side="right")
        person_container.bind("<Button-1>", lambda event: self.current_person_command(person_id))
        self.person_label.bind("<Button-1>", lambda event: self.current_person_command(person_id))
        total_label.bind("<Button-1>", lambda event: self.current_person_command(person_id))
        self.person_top.append(person_container)

    def _add_item(self, item_name, price, amount=1):
        item_frame = tk.Frame(self.items_frame, bg=self.background_color, pady=0, padx=0)
        item_frame.pack(fill="x", side="top")
        item_name_label = tk.Label(item_frame, text=item_name, bg=self.background_color, font=("Inter", 12))
        item_name_label.pack(side="left")
        item_price_label = tk.Label(item_frame, text=f"{amount}x {price} = {amount*price} SEK", bg=self.background_color, font=("Inter", 12))
        item_price_label.pack(side="right")
        self.items.append(item_frame)

    def clear_cart(self):
        for person in self.person_top:
            person.destroy()
        for person in self.person_bottom:
            person.destroy()
        for item in self.items:
            item.destroy()
        self.person_top = []
        self.person_bottom = []
        self.items = []

    def update_cart(self, current_person, person_count, shopping_cart, current_lgn):
        self.clear_cart()
        final_total = 0
        for i in range(person_count):
            total = sum([item["price"]*item["amount"] for item in shopping_cart[i]])
            final_total += total
            if i <= current_person:
                self._add_person(self.person_frame_top, i, current_lgn, total)
            else:
                self._add_person(self.person_frame_bottom, i, current_lgn, total)
        for item in shopping_cart[current_person]:
            self._add_item(item["name"], item["price"], item["amount"])
        self.total_price_label.config(text=f" {final_total} SEK")

    def set_current_person_command(self, set_person_command):
        self.current_person_command = set_person_command

    def set_remove_person_command(self, remove_person_command):
        self.remove_person_command = remove_person_command

    def set_on_drop(self, on_drop):
        self.on_drop = on_drop
        self.cart_frame.on_drop = on_drop
        self.person_frame_top.on_drop = on_drop
        self.items_frame.on_drop = on_drop
        self.person_frame_bottom.on_drop = on_drop

    # pop up window for confirm order
    def double_check_confirm(self, language):
        # pop up window in center for double-check the order
        self.confirm_window = tk.Toplevel(self)
        self.confirm_window.title("Confirm Order")
        self.confirm_window.geometry("300x200")
        self.confirm_window.resizable(False, False)
        # set the position of the pop-up window
        x = self.confirm_window.winfo_screenwidth() // 2 - 150
        y = self.confirm_window.winfo_screenheight() // 2 - 100
        self.confirm_window.geometry(f"+{x}+{y}")

        # force the user to confirm the order
        self.confirm_window.grab_set() # block the main window
        self.confirm_window.focus_set() # focus on the pop-up window
        self.confirm_window.protocol("WM_DELETE_WINDOW", self.prevent_closing)

        self.confirm_label = tk.Label(self.confirm_window, text=LANGUAGE[language]["confirm_order"], font=("Inter", 12))
        self.confirm_label.pack(pady=20)

        self.confirm_yes_btn = tk.Button(self.confirm_window, text=LANGUAGE[language]["yes"], bg=self.primary_color, fg="white", font=("Inter", 12))
        self.confirm_yes_btn.pack(side="left", padx=20)

        self.confirm_no_btn = tk.Button(self.confirm_window, text=LANGUAGE[language]["no"], bg=self.primary_color, fg="white", font=("Inter", 12))
        self.confirm_no_btn.pack(side="right", padx=20)

    def confirm_window_close(self):
        self.confirm_window.destroy()

    def prevent_closing(self):
        """ Prevent closing the confirmation window without an explicit choice """
        pass  # Do nothing, forcing user interaction
