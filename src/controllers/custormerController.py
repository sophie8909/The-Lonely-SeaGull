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
        self.main_controller = main_controller

        self.shopping_cart = []
        self.order_history = []
        self.undo_stack = []
        self.redo_stack = []
        self.ordered_list = []

    def customer_view_setup(self):
        self.frame.shopping_cart_widget.set_on_drop(self.add_cart_item)
        self.frame.shopping_cart_widget.add_friends_btn.config(command=self.add_person)
        self.frame.shopping_cart_widget.confirm_btn.config(command=self.confirm_order)
        self.frame.logout_button.bind("<Button-1>", self.logout_button_click)
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

    def confirm_order(self):
        #TODO: Implement order confirmation
        pass

    def logout_button_click(self, event):
        print("Successfully logged out")
        self.main_controller.switch_controller(self.main_controller.login_controller)

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    controller = CustomerController(root, None, "English")
    controller.create_widgets()
    root.mainloop()