# =============================================================================
# loginController.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Controller the whole application
# =======================================================

# Import the necessary libraries
from tkinter import messagebox

# Local imports
from models.language import LANGUAGE
from models.services import UsersService
from views.loginView import LoginView
from controllers.base import BaseController


class LoginController(BaseController):
    """ The login controller class

        Specific methods available for the login controller.

        Attributes:
            BaseController: the inherited class BaseController
    """

    def __init__(self, tk_root, main_controller, current_language, current_resolution):
        """ Initial method

            Args:
                tk_root: used to get the root tk window
                main_controller: used to get the main controller
                current_language: used to get the current language of the system
                current_resolution: used to get the current resolution of the window
        """

        super().__init__(tk_root, current_language, current_resolution) # inherit from BaseController

        # The geometry values might vary for different display sizes, but for a 15.6 inches
        # display should be on a perfect fullscreen, resolution not being direct proportional
        # to the screen display
        self.tk_root.title("The Flying Dutchman Pub")

        # Values to calculate the initial window display size in pixels
        w = tk_root.winfo_screenwidth()
        h = tk_root.winfo_screenheight()-int(0.036*tk_root.winfo_screenheight())
        x = -int(0.005*tk_root.winfo_screenwidth())
        y = 0
        self.tk_root.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))

        self.users = UsersService('models/sample_users.json') # load the users' details from a JSON file
        self.frame = None
        self.main_controller = main_controller

    def create_login_widgets(self, current_language, current_resolution):
        """ Creating the login widgets and the view itself

            Args:
                current_language: used to get the current language of the system
                current_resolution: used to get the current resolution of the window
        """
        self.frame = LoginView(self.tk_root, current_language, current_resolution)
        self.frame.pack(expand=True, fill='both')

        self.set_up_bind() # handling the binding of widgets that have key assignment

    def hide_login_widgets(self):
        """ Hide the logout button from the view """
        self.frame.settings_widget.logout_button.grid_forget()

    def destroy_widgets(self):
        """ Destroy all the widgets from the view """
        self.frame.destroy()
        self.frame = None

    def set_up_bind(self):
        """ Binding of widgets that have key assignment """
        self.frame.login_button.bind("<Button-1>", self.login_button_click)
        self.frame.username_entry.bind("<Return>", self.login_button_click)
        self.frame.password_entry.bind("<Return>", self.login_button_click)
        self.frame.guest_button.bind("<Button-1>", self.guest_button_click)
        self.frame.settings_widget.login_combo.bind("<<ComboboxSelected>>", self.main_controller.update_language)
        self.frame.settings_widget.res_combo.bind("<<ComboboxSelected>>", self.main_controller.change_res)

    def login_button_click(self, event=None):
        """ Login button functionality

            Args:
                event: not used, but to be here in order to bind the functionality to a widget
        """
        print("Login button clicked")

        # Get the username and password from the entries in the view part
        username = self.frame.username_entry.get()
        password = self.frame.password_entry.get()
        success, message = self.login(username, password)

        # if it is not a successful login
        if not success:
            self.show_message(message, "ERROR")
            return
        # otherwise
        else:
            self.show_message(message, "SUCCESS")

            # Depending on the credentials of the user from the JSON file, get the correct controller
            if self.main_controller.current_user.credentials == 0:
                self.main_controller.switch_controller(self.main_controller.owner_controller)
            elif self.main_controller.current_user.credentials == 1:
                self.main_controller.switch_controller(self.main_controller.bartender_controller)
            elif self.main_controller.current_user.credentials == 2:
                self.main_controller.switch_controller(self.main_controller.vip_controller)

    def guest_button_click(self, event=None):
        """ Normal customer button functionality

            Args:
                event: not used, but to be here in order to bind the functionality to a widget
        """
        print("Continue as a guest button")

        # Go directly to the CustomerController
        self.main_controller.switch_controller(self.main_controller.customer_controller)

    def login(self, username, password):
        """ Login functionality

            Args:
                username: get the username
                password: get the password
        """

        # Get the user from the JSON file based on the username
        user = self.users.get_user(username)

        # Get the current language of the system based on the change of the language combobox from mainController
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)

        # No user
        if user is None:
            return False, LANGUAGE[language_window]["not_found"]
        # No correct password
        if user.password != password:
            return False, LANGUAGE[language_window]["wrong_pass"]

        # Get the user successfully
        self.main_controller.current_user = user
        return True, LANGUAGE[language_window]["success"]

    def show_message(self, message, mess_type):
        """ Display a message regarding the login part

            Args:
                message: the message to be displayed
                mess_type: type of the message
        """

        # The same functionality as the previous mention of this function return
        language_window = self.main_controller.update_language(lambda event: self.main_controller.update_language)

        # if error, display the correct messagebox from tkinter
        if mess_type == "ERROR":
            messagebox.showerror(LANGUAGE[language_window]["error"], message)
        elif mess_type == "SUCCESS":
            messagebox.showinfo(LANGUAGE[language_window]["success"], message)
