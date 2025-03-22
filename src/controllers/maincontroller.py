# =============================================================================
# maincontroller.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao, Darius Loga
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Controller the whole application
# =======================================================

# Import the necessary libraries
import tkinter as tk
from PIL import Image, ImageTk

# Local imports
from controllers.base import BaseController
from controllers.loginController import LoginController
from controllers.custormerController import CustomerController
from controllers.vipController import VIPController
from controllers.bartenderController import BartenderController
from controllers.ownerController import OwnerController


class MainController(BaseController):
    """ The main controller class that manages all the controller

        It contains also some general methods that are going to be available
        for each controller.

        Attributes:
            BaseController: the inherited class BaseController
    """

    def __init__(self, tk_root, current_language, current_resolution):
        """ Initial method

            Args:
                tk_root: used to get the root tk window
                current_language: used to get the current language of the system
                current_resolution: used to get the current resolution of the window
        """

        super().__init__(tk_root, current_language, current_resolution) # inherit from BaseController

        # Construct all the Controls for the different users plus the login part
        self.login_controller = LoginController(tk_root, self, current_language, current_resolution)
        self.customer_controller = CustomerController(tk_root, self, current_language, current_resolution)
        self.vip_controller = VIPController(tk_root, self, current_language, current_resolution)
        self.bartender_controller = BartenderController(tk_root, self, current_language, current_resolution)
        self.owner_controller = OwnerController(tk_root, self, current_language, current_resolution)

        self.current_controller = self.login_controller # start with login part
        self.current_controller.create_login_widgets(self.current_language, self.current_resolution)
        self.current_controller.hide_login_widgets()

    def switch_controller(self, new_controller):
        """ Initial method

            Args:
                new_controller: used to get the controller
        """

        print("Switching controller")
        if self.current_controller: # hide the current widgets, not to display from other controller
            print("Hiding current controller")
            print("language:", self.current_language)
            self.current_controller.destroy_widgets()

        # get the new controller and create the necessary widgets to view different users or come back
        # to the login logic
        self.current_controller = new_controller
        if self.current_controller == self.login_controller:
            self.current_controller.create_login_widgets(self.current_language, self.current_resolution)
            self.current_controller.hide_login_widgets()
        elif self.current_controller == self.customer_controller:
            self.current_controller.create_customer_widgets(self.current_language, self.current_resolution)
            self.current_controller.hide_widgets()

            # should maintain the same button status, even if we switch between the views
            # just to disable the button functionality if is not on the correct tablet
            if self.current_resolution == 1:
                self.current_controller.frame.shopping_cart_widget.confirm_btn["state"] = tk.DISABLED
            else:
                self.current_controller.frame.shopping_cart_widget.confirm_btn["state"] = tk.NORMAL
        elif self.current_controller == self.vip_controller:
            self.current_controller.create_vip_widgets(self.current_language, self.current_resolution)
            self.current_controller.hide_widgets()

            # should maintain the same button status, even if we switch between the views
            # just to disable the button functionality if is not on the correct tablet
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

    def change_res(self, event=None):
        """ Method used to handle different display size setting

            Args:
                event: not used, but to be here in order to bind the functionality to a widget
        """

        res_type = self.current_controller.frame.settings_widget.res_combo.get() # get the current value from that combobox
        screen_width = self.tk_root.winfo_screenwidth() # width of the current's device that runs the application
        screen_height = self.tk_root.winfo_screenheight() # height of the current's device that runs the application

        # for each value from the resolution combobox recalculate width, height,
        # but also the x and y positioning, resolution not being direct proportional
        # to the screen display
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

        # set the root window using the above computed values
        self.tk_root.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))
        print("screen_width:", w)
        print("screen_height:", h)
        print("x:", x)
        print("y:", y)

        if self.current_controller == self.login_controller:
            # Load an image to be used as background
            self.image = Image.open("./assets/boat.jpg")
            # Resize the image using resize() method and configure when there is a change
            # in resolution
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

    def update_language(self, event=None):
        """ Method used to handle different languages and update the text fields of different widgets
            belonging to different views (login, guest, vip, bartender, owner)

            Args:
                event: not used, but to be here in order to bind the functionality to a widget
            Returns:
                Return the current_language to be used in different controllers to change the language
                if the logic does not permit to use .config() function of different widgets from the
                View part
        """

        # get the values from the combobox that is responsible for changing the language
        self.current_language = self.current_controller.frame.settings_widget.login_combo.get()

        # update the text of different widgets that belongs to different views
        # (login, guest, vip, bartender, owner)
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

    def logout_button_click(self, event=None):
        """ Method to go back to the login view, used in all other views except the login part

            Args:
                event: not used, but to be here in order to bind the functionality to a widget
        """

        print("Successfully logged out")

        # uses the switch_controller() to go back
        # to the login view
        self.switch_controller(self.login_controller)

# Main function that can be used to run this .py file individually to test some functionalities
if __name__ == "__main__":
    root = tk.Tk()
    controller = MainController(root)
    root.mainloop()
