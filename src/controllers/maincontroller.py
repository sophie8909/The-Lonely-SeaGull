import tkinter as tk

from PIL import Image, ImageTk

from controllers.base import BaseController
from controllers.custormerController import CustomerController
from controllers.loginController import LoginController
from controllers.vipController import VIPController
from controllers.bartenderController import BartenderController
from controllers.ownerController import OwnerController


class MainController(BaseController):
    def __init__(self, tk_root, current_language, current_resolution):
        super().__init__(tk_root, current_language, current_resolution)

        self.login_controller = LoginController(tk_root, self, current_language, current_resolution)
        self.customer_controller = CustomerController(tk_root, self, current_language, current_resolution)
        self.vip_controller = VIPController(tk_root, self, current_language, current_resolution)
        self.bartender_controller = BartenderController(tk_root, self, current_language, current_resolution)
        self.owner_controller = OwnerController(tk_root, self, current_language, current_resolution)

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
            self.current_controller.hide_widgets()
            # should maintain the same button status, even if we switch between the views
            if self.current_resolution == 1:
                self.current_controller.frame.shopping_cart_widget.confirm_btn["state"] = tk.DISABLED
            else:
                self.current_controller.frame.shopping_cart_widget.confirm_btn["state"] = tk.NORMAL
        elif self.current_controller == self.vip_controller:
            self.current_controller.create_vip_widgets(self.current_language, self.current_resolution)
            self.current_controller.hide_widgets()
            # should maintain the same button status, even if we switch between the views
            if self.current_resolution == 1:
                self.current_controller.frame.shopping_cart_widget.confirm_btn["state"] = tk.NORMAL
                self.current_controller.frame.add_to_balance_button["state"] = tk.DISABLED
            else:
                self.current_controller.frame.shopping_cart_widget.confirm_btn["state"] = tk.DISABLED
                self.current_controller.frame.add_to_balance_button["state"] = tk.NORMAL
        elif self.current_controller == self.bartender_controller:
            self.current_controller.create_bartender_widgets(self.current_language, self.current_resolution, self.current_controller)
            self.current_controller.hide_widgets()
        elif self.current_controller == self.owner_controller:
            self.current_controller.create_owner_widgets(self.current_language, self.current_resolution)
            self.current_controller.hide_widgets()

    # Method used to handle different display size setting
    def change_res(self, event):
        res_type = self.current_controller.frame.settings_widget.res_combo.get()
        screen_width = self.tk_root.winfo_screenwidth()
        screen_height = self.tk_root.winfo_screenheight()

        if res_type == "27\"":
            w = int(screen_width)
            h = int(screen_height - int(0.036 * screen_height))
            x = -int(0.005 * screen_width)
            y = 0
            self.current_resolution = 0
        else:
            w = int(screen_width * 0.7)
            h = int(screen_height * 0.7)
            x = int((screen_width / 2) - (w / 2))
            y = int((screen_height / 2) - (h / 2))
            self.current_resolution = 1

        self.tk_root.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))
        print("screen_width:", w)
        print("screen_height:", h)
        print("x:", x)
        print("y:", y)

        if self.current_controller == self.login_controller:
            # Show background image using label
            self.image = Image.open("./assets/boat.jpg")
            # Resize the image using resize() method
            self.resize_image = self.image.resize((w, h))
            self.img = ImageTk.PhotoImage(self.resize_image)
            self.current_controller.frame.login_background_label.configure(image=self.img)
        # disable the buttons if they are not at the correct tablet, depending on the view
        elif self.current_controller == self.customer_controller:
            if self.current_resolution == 1:
                self.current_controller.frame.shopping_cart_widget.confirm_btn["state"] = tk.DISABLED
            else:
                self.current_controller.frame.shopping_cart_widget.confirm_btn["state"] = tk.NORMAL
        elif self.current_controller == self.vip_controller:
            if self.current_resolution == 1:
                self.current_controller.frame.shopping_cart_widget.confirm_btn["state"] = tk.NORMAL
                self.current_controller.frame.add_to_balance_button["state"] = tk.DISABLED
            else:
                self.current_controller.frame.shopping_cart_widget.confirm_btn["state"] = tk.DISABLED
                self.current_controller.frame.add_to_balance_button["state"] = tk.NORMAL

    # Method used to handle different languages and update the text fields of different widgets
    # belonging to different views (login, guest, vip, bartender, owner)
    def update_language(self, event):
        self.current_language = self.current_controller.frame.settings_widget.login_combo.get()

        if self.current_controller == self.login_controller:
            self.current_controller.frame.update_login_language(self.current_language)
        elif self.current_controller == self.customer_controller:
            self.current_controller.frame.update_customer_language(self.current_language)
        elif self.current_controller == self.vip_controller:
            self.current_controller.frame.update_vip_language(self.current_language)
        elif self.current_controller == self.bartender_controller:
            self.current_controller.frame.update_bartender_language(self.current_language)
        elif self.current_controller == self.owner_controller:
            self.current_controller.frame.update_owner_language(self.current_language)

        return self.current_language

    def logout_button_click(self, event):
        print("Successfully logged out")
        self.switch_controller(self.login_controller)


if __name__ == "__main__":
    root = tk.Tk()
    controller = MainController(root)
    root.mainloop()
