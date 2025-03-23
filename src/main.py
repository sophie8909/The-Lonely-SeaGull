# =============================================================================
# main.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Controller to run the application
# =======================================================

# Import the necessary libraries
import tkinter as tk

# Local imports
from controllers.mainController import MainController

def main():
    """ Function to start the whole application logic in a loop """

    root = tk.Tk()
    MainController(root, current_language="English", current_resolution=0)
    root.mainloop()

# Main function to run the application
if __name__ == '__main__':
    main()