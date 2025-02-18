# ===============================================
# functionObjects.py
# ===============================================
# @AUTHOR: Lars Oestreicher
# @VERSION: 1.0
# @DATE: February 16, 2025
#
# PURPOSE:
# Illustrates the use of a factory class, used to create certain widgets for
# use in combination with an undo manager (see separate file).
#
import UndoManager

# The Functions class is used to hold the different function objects.
# A function object is an object containing the methods and the data used
# to perform DO, UNDO and REDO for a specific user function. The method is
# using a version of the COMMAND OOP-pattern.
#
class Functions :

    # The Initiation is used to set the communications between the functions and the
    # controller.
    #
    def __init__(self, ctrl):
        self.control = ctrl

        # Here we define the functionality that is going to be in the system. The Undo Manager is
        # used in here too by the inheritance symbol.
        #
        self.um = UndoManager.UndoManager(self.control)

    # It is necessary to create three main functions in order to be able to give a
    # general idea about how to undo things as a general function.
    #
    def doFunction(self, valString):
        match valString :
            # The reset button has been pressed.
            case "reset" :
                self.um.doIt(self.ResetFunc(self.control))
            # The quit buttons has been pressed.
            case "quit" :
                quit(1)  # Quit is not really undoable.
            # The update button has been pressed.
            case "update" :
                self.um.doIt(self.UpdateFunction(self.control))
            # The undo or redo buttons have been pressed. But they are of course not
            # possible to undo or redo, since that would make them endlessly recursive.
            #
            case '<--' : self.um.undoIt()
            case '-->' : self.um.redoIt()

            # Any other triggering event will not generate any action at all.
            # There is no UNDO-REDO either
            #
            case _ :
                pass

    # =========================================================================
    # APPLICATION METHODS
    # All functions that are involved in the changes on the model, have to be
    # defined here. These functions need to have the necessary functions for
    # undoing with the UndoManager.
    # =========================================================================
    # This function resets the content of the Entry-field. To Undo means to put
    # the previous content back in the Entry-field.
    #
    # The class hierachy here is a bit complicated.
    # self.controller.view reaches the view.
    #
    class ResetFunc :
        def __init__(self, ctrl):

            self.controller = ctrl
            self.data = ""

        # "Execute" will be getting the content of the entry field.
        # Delete content in the entry, so that the action is clearly defined.
        #
        def execute(self):
            self.data = self.controller.view.entry.get()
            self.controller.view.clear_user_entry()

        # Unexecute will then put the text back into the entry. The UNDO means
        # to put the latest data placed in the Entry field back
        #
        def unexecute(self):
            self.controller.view.clear_user_entry()
            self.controller.view.entry.insert(self.data)

        # Reexecute will in this case almost do the same things as the execute
        # function.
        #
        def reexecute(self):
            self.data = self.controller.view.entry.get()
            self.controller.view.clear_user_entry()


    # UPDATE
    # This function takes the data from the user entry and changes the database
    # with this value.
    # To undo it will take the old value of the database and replace that in the
    # database. The current value of the database will be put back in the user entry
    # field.
    #
    class UpdateFunction :
        def __init__(self, ctrl):
            self.controller = ctrl
            self.data = ""  # Stores the old data in the label (database).
            self.entry = "" # Stores the old data in the Entry field

        def execute(self):
            # Start by storing the existing data in both places.
            #
            self.entry = self.controller.get_entry()  # Store the current user input.
            self.data = self.controller.get_data()    # Store the previous value of the database
                                                      # so that it can be restored.
            # Update the model with the new data for the existing key.
            #
            self.controller.set_data(self.entry)

            # Empty the user input field.
            #
            self.controller.reset_entry()
            self.controller.update_view()

        def unexecute(self):

            # Put the current database value back into entry field.
            #
            self.controller.set_entry(self.entry)

            # Put the old database value back in the database.
            #
            self.controller.set_data(self.data)
            self.controller.update_view()

        def reexecute(self):

            # Put the user entry back into the database.
            #
            self.controller.set_data(self.entry)
            self.controller.reset_entry()
            self.controller.set_entry(self.data)
            self.controller.update_view()

    # We should always try to use the standard way of quitting the application.
    # Calling the quit/1 function will do its best to provide a clean shutdown
    # of the system.
    #
    class QuitFunction :

        def __init__(self, ctrl):
            quit(1)
# =============================================================================
# END of Functions.py
# =============================================================================