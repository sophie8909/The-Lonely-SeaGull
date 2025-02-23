import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys

# Simulated user data
USERS = {
    "admin": {"password": "password", "role": "bartender"},
    "owner": {"password": "password", "role": "owner"},
    "vip": {"password": "password", "role": "vip"},
    "customer": {"password": "password", "role": "customer"}
}

# Simulated beer data
SIMULATED_BEERS = [
    (1, "Pale Ale", 49.99),
    (2, "Stout", 59.99),
    (3, "Lager", 39.99),
    (4, "IPA", 54.99)
]

def fetch_beers():
    return SIMULATED_BEERS

def add_to_cart(beer):
    shopping_cart.insert(tk.END, f"{beer[1]} - {beer[2]} SEK")

def login():
    global user_role
    user_role = "customer"
    root.withdraw()
    open_main_interface()

def on_drag_start(event):
    widget = event.widget
    widget.start_dragging = True
    widget.original_position = (widget.winfo_x(), widget.winfo_y())
    widget.config(relief=tk.SUNKEN)
    widget.lift()
    widget.master.lift()

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() + event.x
    y = widget.winfo_y() + event.y
    widget.place(x=x, y=y)
    widget.lift()
    widget.master.lift()

def on_drag_end(event, beer):
    widget = event.widget
    lx, ly = widget.winfo_x(), widget.winfo_y()
    tx, ty, tw, th = shopping_cart.winfo_x(), shopping_cart.winfo_y(), shopping_cart.winfo_width(), shopping_cart.winfo_height()
    
    if tx <= lx <= tx + tw and ty <= ly <= ty + th:
        add_to_cart(beer)
    
    widget.place(x=widget.original_position[0], y=widget.original_position[1])
    widget.config(relief=tk.RAISED)

def close_application():
    root.destroy()
    sys.exit()

def open_main_interface():
    global shopping_cart
    main_window = tk.Toplevel()
    main_window.title("Main Interface")
    main_window.geometry("900x600")
    main_window.protocol("WM_DELETE_WINDOW", close_application)
    
    main_frame = tk.Frame(main_window)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    left_frame = tk.Frame(main_frame, width=300, relief=tk.SUNKEN, borderwidth=2)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    
    tk.Label(left_frame, text="Beer Menu", font=("Arial", 16)).pack(pady=5)
    
    for index, beer in enumerate(fetch_beers()):
        beer_label = tk.Label(left_frame, text=f"{beer[1]} - {beer[2]} SEK", relief=tk.RAISED, padx=5, pady=5)
        beer_label.place(x=10, y=50 + index * 40)
        beer_label.bind("<ButtonPress-1>", on_drag_start)
        beer_label.bind("<B1-Motion>", on_drag_motion)
        beer_label.bind("<ButtonRelease-1>", lambda e, b=beer: on_drag_end(e, b))
    
    right_frame = tk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=2)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    tk.Label(right_frame, text="Shopping Cart", font=("Arial", 14)).pack()
    shopping_cart = tk.Listbox(right_frame, width=50, height=20)
    shopping_cart.pack()
    
    checkout_button = tk.Button(right_frame, text="Checkout", command=lambda: messagebox.showinfo("Order", "Order placed successfully!"))
    checkout_button.pack(pady=10)

# Create main application window
root = TkinterDnD.Tk()
root.title("Login Interface")
root.geometry("300x200")
root.protocol("WM_DELETE_WINDOW", close_application)

# Username label and entry
username_label = tk.Label(root, text="Username:")
username_label.pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

# Password label and entry
password_label = tk.Label(root, text="Password:")
password_label.pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=20)

# Run the application
root.mainloop()
