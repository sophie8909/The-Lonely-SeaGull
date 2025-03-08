if __name__ == "__main__":
    import sys
    sys.path.append(sys.path[0] + "/../")

from controllers.base import BaseController
from views.customerView import CustomerView


class CustomerController(BaseController):
    def __init__(self, tk_root, main_controller, current_language):
        super().__init__(tk_root, current_language)
        self.frame = None
        self.person_count = 0
        self.current_person = 0

        self.shopping_cart = []
        self.order_history = []
        self.undo_stack = []
        self.redo_stack = []
        self.ordered_list = []

    def customer_view_setup(self):
        self.frame.shopping_cart_widget.set_on_drop(self.add_cart_item)
        self.frame.shopping_cart_widget.add_friends_btn.config(command=self.add_person)
        self.frame.shopping_cart_widget.confirm_btn.config(command=self.confirm_order)
        # self.frame.shopping_cart_widget.undo_btn.config(command=self.undo)
        # self.frame.shopping_cart_widget.redo_btn.config(command=self.redo)
        self.add_person()
    
    def create_widgets(self):
        self.frame = CustomerView(self.tk_root, self.current_language)
        self.frame.pack(expand=True, fill='both')
        self.customer_view_setup()

    def destroy_widgets(self):
        self.frame.destroy()
        self.frame = None

    def add_person(self):
        self.person_count += 1
        self.shopping_cart.append([])
        self.undo_stack.append('add_person')
        self.frame.add_person(remove_command=self.remove_person)
        self.current_person = self.person_count - 1
        self.frame.set_person(self.current_person)

    def remove_person(self, i):
        if isinstance(i, tk.Label):
            i = int(i.cget("text").split(" ")[1]) - 1
        print(i, self.person_count)
        self.person_count -= 1
            
        self.shopping_cart.pop(i)
        self.undo_stack.append('remove_person')
        self.frame.remove_person(i)
        if self.person_count == 0:
            self.add_person()
        elif self.current_person == self.person_count:
            self.current_person -= 1
            print(self.current_person, self.person_count, self.frame.shopping_cart_widget.items)
        self.frame.set_person(self.current_person)
    def add_cart_item(self, product_widget):
        """Add an item to the shopping cart"""
        print("Adding item to cart")
        item_name = product_widget.product_name.cget("text")
        itme_price = product_widget.product_price.cget("text").split(" ")[0]
        self.shopping_cart[self.current_person].append({"name": item_name, "price": itme_price})
        self.frame.shopping_cart_widget.add_item(item_name, itme_price)

    """Confirm the order and add it to the order history"""
    def confirm_order(self):
        # double check the order
        self.frame.shopping_cart_widget.double_check_confirm()
        self.frame.shopping_cart_widget.confirm_yes_btn.config(command=self.confirm_order_yes)
        self.frame.shopping_cart_widget.confirm_no_btn.config(command=self.confirm_order_no)

    def confirm_order_yes(self):
        print("Confirming order")
        order = []
        # Add all items in the shopping cart to the order
        for person in self.shopping_cart:
            order.append(person)
        self.order_history.append(order)

        print("Order history:")
        for order in self.order_history:
            print(order)

        # reset shopping cart
        self.frame.shopping_cart_widget.clear_cart()
        self.shopping_cart = []
        self.person_count = 0
        self.add_person()

        # empty the undo stack
        self.undo_stack = []
        self.redo_stack = []


        self.frame.shopping_cart_widget.confirm_window_close()

        

    def confirm_order_no(self):
        print("Cancelling order")
        self.frame.shopping_cart_widget.confirm_window_close()

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    controller = CustomerController(root, None, "English")
    controller.create_widgets()
    root.mainloop()