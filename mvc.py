# =============================================================================
# MVC.py 
# =============================================================================
# @AUTHOR: Lars Oestreicher
# @VERSION: 1.0
# @DATE: February 2, 2025
#
# PURPOSE:
#    Small program to demonstrate:
#       - the use of dictionaries
#       - the Model-View Control structure.
#
# This file contains the complete program for the demonstration,
# except the Dictionary.
# =============================================================================
# COPYLEFT: This program may be distributed and used 
# freely. It can also be modified to be included in 
# other programs without any restrictions. 
# ===============================================
# IMPORTS
# ===============================================
# Library imports 
#
import tkinter as tk
from tkinter import StringVar
#
# ===============================================
# Local imports
#
import Dictionary

# ===============================================
# Global variables
#
local_dictionary = Dictionary.Dict()


# =======================================================
# CLASS MODEL
# =======================================================
#
# Model: The model handles the application data and business logic.
# This can be any data structure that is feasible för the project, 
# including json structures (the data files provided for the project).
#
class Model:

    def __init__(self):

        # This statement is where you store the data. This can be just any
        # structure. Just change the accessors to the appropriate function,
        # for example it could be the accessors to a Python dictionary structure.
        #
        self.data = "Hello, MVC!"

    # RESERVED METHODS FOR THE CONTROLLER
    #
    # We don't access the data directly through the model data structures, but the
    # controller will use accessors (setters and getters). The advantage is that the
    # accessors can, for example, contain error detection and prevention.
    #
    # First function lets the controller retrieve the data from the database
    #
    def get_data(self):
        return self.data

    # Second function lets the controller change the data in the database
    # It replaces the value.
    #
    def set_data(self, new_data):
        self.data = new_data


# =============================================================================
# CLASS VIEW
# =============================================================================
#
# View: Defines and manages the User Interface activities. It's functions can be
# called by the Controller. However, the Controller will not directly put any
# values in the interface, but use the View's accessor functions.
#
class View:

    # The __init__ functions will be used to set up all the details of the
    # user interface.
    #
    def __init__(self):
        # =======================================================
        # The root contains the actual window frame (the view). The window
        # is instantiated when the program is run at the end of the main file.
        # =======================================================
        # The example VIEW:
        #
        # Create a fixed label and a changeable label to display some ¨
        # data from the model. We use the simplest type of layout manager here,
        # elements are just placed above each other. Each added element
        # has to be placed in the interface by the "pack()"-method.
        #
        # The two buttons at the bottom of the dialogue are placed in a
        # separate frame that has a horizontal direction instead.
        #
        # The use of a dictionary for strings complicates the construction of
        # all items that have an attached string. The structure is adapted to
        # allow the program to change language dynamically.
        #
        self.lab1 = StringVar()                     # The variable containing the value of the
                                                    # label, button or other variable in a widget.
        self.val1 = 'content'                       # The key for the strings

        # Create the first label, and place it on the root surface. As can be seen we
        # can also set the font and the text size here.
        #
        self.label1 = tk.Label(root, textvariable=self.lab1, font=("Arial", 14))

        # We don't store the strings in the code, but use a lookup function from the dictionary
        # in the Dictionary file.
        #
        self.lab1.set(local_dictionary.get_string(self.val1))   # Lookup the string for the key
        self.label1.pack(pady=10)                               # and add to the variable.

        # Finally we add a textvariable-key pair to the list of objects that contain
        # a string (for the language change through the dictionary).
        #
        local_dictionary.add_container([self.val1, self.lab1])

        # A StringVar is a special type of variable used in user interfaces
        # instead of ordinary variables. When the StringVar variable is changed
        # the value changes also in the view. This variable does not need any entry
        # in the dictionary for this label.
        #
        # Note also again how the font settings can be easily changed on different parts of the
        #
        self.label_var = StringVar()
        self.label = tk.Label(root, textvariable=self.label_var, font=("Arial", 14))
        self.label_var.set("")
        self.label.pack()

        # Create an entry widget for data input. This is a text field.
        # It is left empty in the beginning for this example. It does not need to
        # have a dictionary entry.
        #
        self.entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.entry.pack(pady=10)

        # Create a button to update data, and show the change in the view. This
        # button sends a signal to the controller to perform the action.
        #
        self.upd_val = StringVar()
        self.updval1 = 'update'
        self.update_button = tk.Button(root, textvariable=self.upd_val, font=("Arial", 14))
        self.upd_val.set(local_dictionary.get_string(self.updval1))
        self.update_button.pack(pady=10)

        local_dictionary.add_container([self.updval1, self.upd_val])

        # =======================================================
        # Start horizontal layout Quit and Reset.
        # =======================================================
        # Create a new frame in the root window to hold a Quit
        # and Reset buttons side by side
        #
        self.button_frame = tk.Frame(root)

        # Reset button (default button by the keyword active. Most widgets
        #
        self.resval = StringVar()
        self.resval1 = 'reset'

        self.reset_button = tk.Button(self.button_frame, textvariable=self.resval, font=("Arial", 14), default="active")
        self.resval.set(local_dictionary.get_string(self.resval1))
        self.reset_button.pack(side="left", padx=10, pady=10)

        local_dictionary.add_container([self.resval1, self.resval])

        # Quit button
        #
        self.quitval = StringVar()
        self.quitval1 = 'quit'

        self.quit_button = tk.Button(self.button_frame, textvariable=self.quitval, font=("Arial", 14))
        self.quitval.set(local_dictionary.get_string(self.quitval1))
        self.quit_button.pack(side="left", padx=10, pady=10)

        local_dictionary.add_container([self.quitval1, self.quitval])
        self.button_frame.pack(pady=10)

    # =======================================================
    # RESERVED METHODS FOR THE CONTROLLER.
    # =======================================================
    # The methods in this part constitute the access functions to the view
    # for the controller
    #
    # This is the function handle used by the controller to change the content
    # of the label displaying the data.
    #
    def update_view(self, text):
        self.label_var.set(text)

    # This is the function handle used by the control to retrieve the new data from
    # input field of the view,
    #
    def get_user_entry(self):
        return self.entry.get()

    # If we have written too much text, we can clear the data field with
    # the click on one button.
    #
    def clear_user_entry(self):
        self.entry.delete(0, tk.END)    # Delete from position 0 to end of text
                                        # field.


# =============================================================================
# CLASS CONTROLLER
# =============================================================================
# Controller: Connects the Model and View. Ideally, it should not know anything
# about the data it transmits between View and Model.
#
class Controller:
    def __init__(self):

        # Create the model and the view in the controller. This allows the
        # controller to have access to both parts directly.
        #
        self.model = Model()

        # The view is created with the root as argument. This variable contains
        # the window frame, which is created at the running of the program.
        #
        self.view = View()

        # Initialize the view with data from the model. Note that (beside the
        # variable names the controller does not know anything about the content,
        # neither in the model, nor in the view. It is merely fetching the
        # data from the model and displaying it in the view.
        #
        self.view.update_view(self.model.get_data())

        # Bind the update button to the update action. Note that this is
        # one crucial part of the interface design, namely to bind an action
        # to an interface component, so that the user can initiate the action. 
        #
        # The callback function may not use any arguments.
        #
        self.view.update_button.config(command=self.update_data)

        # Bind the Reset button to a function that clears the entry field
        #
        self.view.reset_button.config(command=self.reset_entry)
        self.reset_entry()  # Clear the input field when the Reset button is clicked

        # Bind the Quit button to the command used to exit the application
        # in a normal way. 
        # 
        self.view.quit_button.config(command=root.quit)

    # Here all the actions needed to update the system so that the model is changed, and 
    # the view portrays the updated status of the model.
    #
    def update_data(self):

        # First we modify the model with the new data from the user.
        #
        # Get new data from the input field in the view.
        #
        new_data = self.view.get_user_entry()

        # Then we update the model with new data
        #
        self.model.set_data(new_data)

        # Finally we update the view from the new version of the model.
        #
        self.view.update_view(self.model.get_data())

    def get_data(self):
        return self.model.get_data()

    def set_data(self, data):
        self.model.set_data(data)

    def reset_entry(self):

        # Clear the entry field in the view
        #
        self.view.clear_user_entry()
# =============================================================================
# END CLASS CONTROLLER
# =============================================================================


# =============================================================================
# Main application loop
#
# This has to be at the end of the main (start) file.
#
if __name__ == "__main__":

    # Generate the frame window.
    #
    root = tk.Tk()

    # Set the Title of the window
    #
    root.title("MVC Example with Tkinter")

    # Set the size of the window,
    #
    root.geometry("400x300")

    # Initialize the controller, which will manage the model and view with
    # the main window as argument.
    #
    app = Controller()

    # Start the main event loop
    # After this, only the already defined items are available, so this has to be
    # the absolutely last part of the file.
    #
    root.mainloop()

# =============================================================================
# END PROGRAM MVC DEMO
# =============================================================================
