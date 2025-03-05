import tkinter as tk
from controllers.maincontroller import MainController

def main():
    root = tk.Tk()
    MainController(root, current_language="English")
    root.mainloop()

if __name__ == '__main__':
    main()