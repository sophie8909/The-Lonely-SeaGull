# Controller.py
import tkinter as tk
from models.language import LANGUAGE
from controllers.base import BaseController
from controllers.custormerController import CustomerController
from controllers.loginController import LoginController


class MainController(BaseController):
    def __init__(self, tk_root, current_language, current_resolution):
        super().__init__(tk_root, current_language, current_resolution)

        self.customer_controller = CustomerController(tk_root, self, current_language, current_resolution)
        self.login_controller = LoginController(tk_root, self, current_language, current_resolution)

        self.current_controller = self.login_controller
        self.current_controller.create_login_widgets(self.current_language, self.current_resolution)
        self.current_controller.hide_login_widgets()

        self.current_user = None


    def switch_controller(self, new_controller):
        print("Switching controller")
        if self.current_controller:
            print("Hiding current controller")
            print("language:", self.current_language)
            self.current_controller.destroy_widgets()

        self.current_controller = new_controller
        if self.current_controller == self.login_controller:
            self.current_controller.create_login_widgets(self.current_language, self.current_resolution)
            self.current_controller.hide_login_widgets()
        elif self.current_controller == self.customer_controller:
            self.current_controller.create_customer_widgets(self.current_language, self.current_resolution)
            self.current_controller.hide_customer_widgets()

    # Method used to handle different display size setting
    def change_res(self, event):
            res_type = self.current_controller.frame.settings_widget.res_combo.get()
            screen_width = self.tk_root.winfo_screenwidth()
            screen_height = self.tk_root.winfo_screenheight()

            if res_type == "27\"":
                w = screen_width
                h = screen_height
                self.current_resolution = 0
            else:
                w = screen_width * 0.5
                h = screen_height * 0.5
                self.current_resolution = 1
            x = (screen_width / 2) - (w / 2)
            y = (screen_height / 2) - (h / 2)

            self.tk_root.geometry(str(int(w)) + "x" + str(int(h)) + "+" + str(int(x)) + "+" + str(int(y)))
            print("screen_width:", w)
            print("screen_height:", h)
            print("x:", x)
            print("y:", y)

    # Method used to handle different languages and update the text fields of different widgets
    # belonging to different views (login, guest, vip, bartender, owner)
    def update_language(self, event):
        self.current_language = self.current_controller.frame.settings_widget.login_combo.get()

        self.current_controller.frame.settings_widget.language_label.config(text=LANGUAGE[self.current_language]["language"])
        self.current_controller.frame.settings_widget.res_label.config(text=LANGUAGE[self.current_language]["resolution"])
        self.current_controller.frame.settings_widget.logout_button.config(text=LANGUAGE[self.current_language]["logout"])

        if self.current_controller == self.login_controller:
            self.current_controller.frame.username_label.config(text=LANGUAGE[self.current_language]["username"])
            self.current_controller.frame.password_label.config(text=LANGUAGE[self.current_language]["password"])
            self.current_controller.frame.login_button.config(text=LANGUAGE[self.current_language]["login"])
            self.current_controller.frame.guest_button.config(text=LANGUAGE[self.current_language]["guest_btn"])
        elif self.current_controller == self.customer_controller:
            self.current_controller.frame.shopping_cart_widget.add_friends_btn.config(text=LANGUAGE[self.current_language]["add friends"])
            self.current_controller.frame.shopping_cart_widget.confirm_btn.config(text=LANGUAGE[self.current_language]["confirm"])
            self.current_controller.frame.shopping_cart_widget.undo_btn.config(text=LANGUAGE[self.current_language]["undo"])
            self.current_controller.frame.shopping_cart_widget.redo_btn.config(text=LANGUAGE[self.current_language]["redo"])

            self.current_controller.frame.shopping_cart_widget.total_text_label.config(text=LANGUAGE[self.current_language]["total"])
            self.current_controller.frame.shopping_cart_widget.confirm_label.config(text=LANGUAGE[self.current_language]["confirm_order"])
            self.current_controller.frame.shopping_cart_widget.confirm_yes_btn.config(text=LANGUAGE[self.current_language]["yes"])
            self.current_controller.frame.shopping_cart_widget.confirm_no_btn.config(text=LANGUAGE[self.current_language]["no"])

            self.current_controller.frame.food_button.config(text=LANGUAGE[self.current_language]["food"])
            self.current_controller.frame.beverages_button.config(text=LANGUAGE[self.current_language]["beverages"])

if __name__ == "__main__":
    root = tk.Tk()
    controller = MainController(root)
    root.mainloop()