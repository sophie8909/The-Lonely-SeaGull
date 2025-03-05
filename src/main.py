import tkinter as tk
from controllers.controller import Controller

def main():
    root = tk.Tk()
    Controller(root, current_language="English")
    root.mainloop()

if __name__ == '__main__':
    main()