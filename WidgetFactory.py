# The Widget factory class is used to simplify the creation of labels and buttons
#
import tkinter as tk
from tkinter import StringVar

# This file is only used by mvc2.
#
from mvc2 import local_dictionary
import functionObjects as fo

class WidgetFactory:

    fontFamily = 'Arial'
    fontSize =  14

    def __init__(self, ctrl):
        self.cont = ctrl

    # self.upd_val = StringVar()
    # self.updval1 = 'update'
    # self.update_button = tk.Button(self.root, textvariable=self.upd_val, font=("Arial", 14))
    # self.upd_val.set(local_dictionary.dictionary[self.updval1])
    # self.update_button.pack(pady=10)
    # local_dictionary.add_container([self.updval1, self.upd_val])

    def create(self, parentFrame, type, key):

        # Create a changeable variable for the label (if needed).
        #
        val = StringVar()
        val1 = key
        val.set(local_dictionary.get_string(val1))

        match type :
            case 'label' :
                item = tk.Label(parentFrame, textvariable=val, font=(self.fontFamily, self.fontSize))
            case 'button' :
                item = tk.Button(parentFrame,
                                 textvariable=val,
                                 font=(self.fontFamily, self.fontSize),
                                 command=lambda: self.cont.funs.doFunction(key))
            case _ :
                item = tk.Text(parentFrame,
                                    width=100,
                                    height=20)

        # Set the text of the button or the label
        #
        val.set(local_dictionary.get_string(val1))

        # Add the key + widget to the container with all widgets. This is needed for the
        # translation later.
        #
        local_dictionary.add_container([val1,val])

        return item, val  # We return the StringVar, in case we need to change the
                          # content of the object.

# END WIDGETFACTORY