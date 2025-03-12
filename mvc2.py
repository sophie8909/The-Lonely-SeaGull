# =============================================================================
# MVC2.py
# =============================================================================
# @AUTHOR: Lars Oestreicher
# @VERSION: 2.0
# @DATE: February 2, 2025
#
# PURPOSE:
# Small program to demonstrate: 
#    - the use of dictionaries
#    - the Model-View Control structure.
# In version 2 we add a slightly more advanced model
# to the program. In this version we use a python
# dictionary to store the data.
#
# Furthermore, the creation of the labels and buttons is modified
# by the use of the factory pattern. We use the same dictionary,
# as in mvc.py.§
# =======================================================
# COPYLEFT: This program may be distributed and used 
# freely. It can also be modified to be included in 
# other programs without any restrictions. 
# =======================================================
# IMPORTS
# =======================================================
# Library imports 
#
import tkinter as tk

# ===============================================
# Local imports
#
import Dictionary
import WidgetFactory
import functionObjects as fO

# The StringVars are only used explicitly in the
# definition of the widgets.
#

# ===============================================
# Global variables
#
local_dictionary = Dictionary.Dict()
com = Dictionary.Common()

# ===============================================
# CLASS MODEL
# ===============================================
#
# Model: The model handles the application data and business logic.
# This can be any data structure that is feasible för the project, 
# including json structures (the data files provided for the project).
#
class Model:

    def __init__(self):

        # DATA BASE
        # This statement is where you store the data. This can be just any
        # structure. Here we use a Python dictionary to store the data. Now we
        # can use several keywords and value pairs in the database. This
        # complicates the program slightly.
        #
        self.data = {
            'content': "Hello, MVC!"
        }
    # =========================================================================
    # RESERVED METHODS FOR THE CONTROLLER
    # =========================================================================
    #
    # We don't access the data directly from the model data structures, but the
    # controller will use these use accessors (setters and getters).
    # The first function lets the controller retrieve the data from the database
    #
    # def get_data(self, key):
    #     return self.data[key]

    # @override
    # This version uses a fixed key, content.
    #
    def get_data(self):
        return self.data["content"]

    # Second function lets the controller change the data in
    # the database. It replaces the value for a key, alternatively
    # defines a new key:values pair.
    #
    # def set_data(self, key, new_data):
    #     self.data[key] = new_data

    # @override
    # This version again uses a fixed key for the access of the data.
    #
    def set_data(self, new_data):
        self.data["content"] = new_data


# =========================================================================
# CLASS VIEW
# =========================================================================
#
# View: Defines and manages the User Interface activities.
#
class View:

    contvar = ""

    # The __init__ functions will be used to set up all the details of the
    # user interface. Root contains the window that everything is displayed on
    #
    def __init__(self, ctrl, root):
        
        # The root contains the actual window frame (the view). The window
        # is instantiated when the program is run at the end of the main file.
        #
        self.root = root

        # The Widget factory is used to create the labels and buttons, but
        # can be extended to many other elements. 
        #
        c = WidgetFactory.WidgetFactory(ctrl)
    
        # =======================================
        # THE EXAMPLE VIEW:
        # =======================================
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
        # 1. First we create a sub surface (a frame) to put the UNDO and REDO buttons
        # and a label for the data content space at a top.

        self.top_frame = tk.Frame(self.root, bg='#f7f7bd')
        self.top_frame.pack(expand=1, fill='x')

        # 2. Then we create the widgets for this frame using the WidgetFactory.
        #
        undo_button, _ = c.create(self.top_frame, 'button', '<--')
        undo_button.pack(side="left", padx=20)

        label, _ = c.create(self.top_frame, 'label', 'content')
        label.pack(side='left', expand='true', fill='x')

        redo_button, _ = c.create(self.top_frame, 'button', '-->')
        redo_button.pack(side="left", padx=20)

        # =====================================================================
        # This is the code for a label defined without the WidgetFactory
        # =====================================================================
        # self.lab1 = StringVar()
        # self.val1 = 'content'                       # The key for the strings
        #
        # self.label1 = tk.Label(self.root, textvariable=self.lab1, font=("Arial", 14))
        #
        # self.lab1.set(local_dictionary.dictionary[self.val1])   # Lookup the string for the key
        # self.label1.pack(pady=10)                   # and add to the variable.
        # local_dictionary.add_container([self.val1, self.lab1])
        # =====================================================================
        # A StringVar is a special type of variable used in user interfaces
        # instead of ordinary variables. When the StringVar variable is changed
        # the value changes also in the view. This variable does not need any entry
        # in the dictionary for this label.
        # =====================================================================
        #
        label, self.contvar = c.create(root, 'label', 'contentDisp')
        label.pack(padx=20)

        # 3. Create an entry widget for data input. This is a text field.
        # It is left empty in the beginning for this example. It does not need to
        # have a dictionary entry, and will not be created in the simple version
        # of the WidgetFactory.
        #
        self.entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.entry.pack(pady=10)

        # 4. Create a button to update data, and show the change in the view. This
        # button sends a signal to the controller to perform the action.
        #
        button, _ = c.create(root, 'button', 'update')
        button.pack(pady=10)

        # =======================================================
        # Start horizontal layout Quit and Reset.
        # =======================================================
        # 5. Create a new frame in the root window to hold a Quit
        # and Reset buttons side by side
        #
        self.button_frame = tk.Frame(self.root, bg='#fecece')

        # Create a reset button (default button)
        #
        button, _ = c.create(self.button_frame, 'button', 'reset')
        button.pack(side="left", pady=10, padx=10)

        # Quit button
        #
        button, _ = c.create(self.button_frame, 'button', 'quit')
        button.pack(pady=10, padx=10)

        # Nothing will show until we initialise the widget by the pack version
        self.button_frame.pack(pady=20)

    # =====================================================================
    # RESERVED METHODS FOR THE CONTROLLER.
    # =====================================================================
    # The methods in this part constitute the access functions to the view
    # for the controller
    #
    # =====================================================================
    # First is the function handle used by the controller to change the content
    # of the label displaying the data. They are not dependent on the content that
    # is entered from the model.
    #
    # To update the view, we have to change the content in the view field
    # from the model.
    #
    def update_view(self, value):
        self.contvar.set(value)

    # To get the value that is already in the widgets of the view, we will access
    # current value.
    #
    def get_current_value(self):
        return self.contvar.get()

    # This is the function handle used by the controller to retrieve the new data from
    # input field of the view, the entry field.
    #
    def get_user_entry(self):
        return self.entry.get()

    # This function is used primarily by the UNDO-functionality, since we have to be able
    # to put back the information in the entry field from before it was added to the database,
    # when it was deleted.
    #
    # First we delete the content of the field, i.e., the whole content from position 0 to the
    # last position in the entry. Then we can insert the replacing text.
    #
    def set_user_entry(self, value):
        self.clear_user_entry()
        self.entry.insert(0, value)

    # If we have written too much text, we can clear the data field with
    # the click on one button.
    #
    def clear_user_entry(self):
        self.entry.delete(0, tk.END)  # Delete from position 0 to end of text
                                      # field.

# ===============================================
# CLASS CONTROLLER
# ===============================================
# Controller: Connects the Model and View. Ideally, it should not know anything
# about the data it transmits between View and Model.
#
class Controller:

    # Initial value of the key field.
    #
    key = 'content'

    def __init__(self, root):

        # The controller needs to have the functions available. In the creation we also
        # send the backlink to the controller. This is used to call the controller
        # with the right functions. The controller class is currently just delegating
        # everything.
        #
        self.funs = fO.Functions(self)

        # Create the model and the view in the controller. This allows the
        # controller to have access to both parts directly. However, the
        # model and the view have no direct contact.
        #
        self.model = Model()

        # The view is created with the root wondow as argument. This variable contains
        # the window frame, which is created at the running of the program.
        #
        self.view = View(self, root)

        # Initialize the view with data from the model. Note that (beside the
        # variable and function names) the controller does not know anything
        # about the content, neither in the model, nor in the view. It is
        # merely fetching the data from the model and displaying it in the view.
        #
        self.view.update_view(self.model.get_data())

        # We need to bind the buttons to the correct actions. Note that this is
        # one crucial part of the interface design, namely to bind an action
        # to an interface component, so that the user can initiate the action. 
        #
        # The callback function may not use any arguments. This is the way this
        # should have been defined without the UNDO-manager. If you want to disable
        # the UNDO-manager, then you can uncomment the following:
        #
        # self.view.update_button.config(command=self.update_data)
        #
        # Bind the Reset button to a function that clears the entry field
        #
        # self.view.reset_button.config(command=self.reset_entry)
        # self.reset_entry()  # Clear the input field when the Reset button is clicked
        #
        # Bind the Quit button to the command used to exit the application
        # in a normal way.
        #
        # self.view.quit_button.config(command=root.quit)

    # Here all the actions needed to update the system so that the model is changed, and 
    # the view portrays the updated status of the model.
    #
    def update_data(self):

        # First, retrieve new data from the input field in the view.
        #
        new_data = self.view.get_user_entry()

        # Update the model with the new data for the existing key.
        #
        self.model.set_data(new_data)
        print(self.model.data)

        # Get the data from the model.
        #
        self.get_data()

        # Update the view with the data from the model.
        #
        self.update_view()

    # The controller part of the get the entry of the view.
    #
    def get_entry(self):
        return self.view.get_user_entry()

    # The controller part of the updating of the view. It fetches
    # the value from the database, and then sends it to the view.
    #
    def update_view(self):
        item = self.get_data()
        self.view.update_view(item)

    # The controller part of the get data from the model.
    #
    def get_data(self):
        return self.model.get_data()

    def set_data(self, value):
        self.model.set_data(value)

    def set_entry(self, value):
        self.view.set_user_entry(value)

    def reset_entry(self):
        # Clear the entry field in the view
        #
        self.view.clear_user_entry()

# ===============================================
# END CLASS CONTROLLER
# ===============================================
#
#================================================
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
    root.geometry("600x300")
    root.configure(background='#f7f7bd')

    # Initialize the controller, which will manage the model and view with
    # the main window as argument.
    #
    app = Controller(root)

    # Start the main event loop
    # After this, only the already defined items are available, so this has to be
    # the absolutely last part of the file.
    #
    root.mainloop()

# =======================================================
# END PROGRAM MVC DEMO
# =======================================================
