import tkinter as tk
from tkinter import messagebox, ttk
from src.models.language import LANGUAGES

class LoginView:
    def __init__(self, parent, language, current_language):
        # self.root.title("Login Interface")
        # self.root.geometry("300x200")
        # self.root.protocol("WM_DELETE_WINDOW", close_application)

        # Combo box for selecting different system language
        self.combo = ttk.Combobox(self.root, state="readonly", values=["English", "Swedish", "Chinese"], height=2, width=10)
        self.combo.pack(padx=5)
        self.combo.current(0)
        self.combo.bind("<<ComboboxSelected>>", self.selection_changed)

        # Username label and entry
        self.label1 = tk.Label(self.root, text=LANGUAGES[current_language]["username"])
        self.label1.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        # Password label and entry
        self.label2 = tk.Label(self.root, text=LANGUAGES[current_language]["password"])
        self.label2.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        self.button = tk.Button(self.root, text=LANGUAGES[current_language]["login"], command=self.login)
        self.button.pack(pady=20)
        self.button.config(text=LANGUAGES[current_language]["login"])