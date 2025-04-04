# =============================================================================
# bartender_panel.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao, Darius Loga
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: The component for the BartenderView
# =======================================================

# Import the necessary libraries
import tkinter as tk
from tkinter import ttk

# Local imports
from models.language import LANGUAGE
from views.baseView import BaseView


class Notification(tk.Frame):
    """ The Notification class

        Class to create a toast notification
        credit to this git repo for inspiration https://github.com/ritik48/popup-notification-tkinter/blob/main/notification.py

        Attributes:
            tk.Frame: the inherited class tk.Frame
    """

    def __init__(self, master, width, height, bg, text, font, y_pos):
        """ Initial method

            Args:
                master: used to get the tk window/frame
                width: width of the window
                height: height of the window
                bg: background color of the window
                text: text of the window
                font: font of the window
                y_pos: y position of the window
        """

        super().__init__(master, bg=bg, width=width, height=height) # inherit from tk.Frame
        self.pack_propagate(tk.FALSE) # no propagation for the size of the notification

        self.y_pos = y_pos

        self.master = master
        self.width = width

        right_offset = 8

        # Calculations for placement in the right top part of the window
        self.cur_x = self.master.winfo_width()
        self.x = self.cur_x - (self.width + right_offset)

        # Label for the text message of the notification
        self.message = tk.Label(self, text=LANGUAGE[text]["panic text"], font=font, bg=bg, fg="black")
        self.message.pack(side="left", padx=5)

        # Close button, represented as "X", of the notification
        self.close_btn = tk.Button(self, text="X", bg=bg, relief="flat", command=self.hide_animation, cursor="hand2")
        self.close_btn.pack(side="right", padx=5)

        # Actual placement
        self.place(x=self.cur_x, y=y_pos)

    def show_animation(self):
        """ Show the notification,
            moving the frame with the text and button up to a certain position
        """
        if self.cur_x > self.x:
            self.cur_x -= 1
            self.place(x=self.cur_x, y=self.y_pos)

            # Show after 1 ms when the click has been made, making it almost instantly
            # Auto hide after 5 seconds
            self.after(1, self.show_animation)
            self.after(5000, self.hide_animation)

    def hide_animation(self):
        """ Hide the notification,
            moving the frame with the text and button up to the edge
            of the width of the window frame
        """
        if self.cur_x < self.master.winfo_width():
            self.cur_x += 1
            self.place(x=self.cur_x, y=self.y_pos)

            # Hide after 1 ms when the click has been made, making it almost instantly
            self.after(1, self.hide_animation)


class TableFrame(tk.Frame):
    """ The Table frame component view class

        Here are all the widgets that are going to be available for the table frame component view

        Attributes:
            tk.Frame: the inherited class tk.Frame
    """

    def __init__(self, parent, table_number, language, table_data=[], total=0, value_changed_command=None, remove_command=None, focus_command=None, **kwargs):
        """ Initial method

            Args:
                parent: used to get the tk window/frame
                table_number: table number
                language: used to get the current language of the system
                table_data: list of table data
                total: total number of tables
                value_changed_command: command to execute when the table is changed
                remove_command: command to remove the table
                focus_command: command to focus the table
        """

        super().__init__(parent, bg='lightgray', **kwargs) # inherit from tk.Frame

        # Table number label
        tk.Label(self, text=f"{LANGUAGE[language]['table']} {table_number}", font=("Arial", 10, "bold"), bg='lightgray').pack(anchor='w', pady=5)
        
        # Items, Prices, Comments Headers
        headers_frame = tk.Frame(self, bg='lightgray')
        headers_frame.pack(fill='x')
        headers_frame.grid_columnconfigure(0, weight=1)
        headers_frame.grid_columnconfigure(2, weight=1)
        headers_frame.grid_columnconfigure(3, weight=1)
        headers_frame.grid_columnconfigure(4, weight=1)
        
        # Headers using grid layout
        tk.Label(headers_frame, text=LANGUAGE[language]["Items"], bg='lightgray', font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, sticky="ew")
        tk.Label(headers_frame, text=LANGUAGE[language]["Amount"], bg='lightgray', font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, sticky="ew")
        tk.Label(headers_frame, text=LANGUAGE[language]["Prices"], bg='lightgray', font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, sticky="ew")
        tk.Label(headers_frame, text=LANGUAGE[language]["Reason"], bg='lightgray', font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5, sticky="ew")
        tk.Label(headers_frame, text=LANGUAGE[language]["Comments"], bg='lightgray', font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, sticky="ew")

        # Create other widgets for the table management
        self.items = []
        for row, data in enumerate(table_data):
            item = tk.Label(headers_frame, text=data['item'], bg='lightgray')
            item.grid(row=row+1, column=0, padx=5, sticky="ew")

            # Amount combobox
            amount = ttk.Combobox(headers_frame, values=[str(i) for i in range(1, 100)], state='readonly', width=2)
            amount.set("1")
            amount.grid(row=row+1, column=1, padx=5)

            # Price entry
            price = tk.Entry(headers_frame, bg='lightgray', width=5)
            price.insert(0, f"{data['price']:.2f}")
            price.grid(row=row+1, column=2, padx=5, sticky="ew")

            # Default reason for the price reduction combobox
            reason = ttk.Combobox(headers_frame, values=[LANGUAGE[language]["normal"], LANGUAGE[language]["on house"], LANGUAGE[language]["compensation"]], width=11)
            reason.grid(row=row+1, column=3, padx=5, sticky="ew")

            # Future comments entry
            comment = tk.Entry(headers_frame, bg='lightgray', width=10)
            comment.insert(0, data['comment'])
            comment.grid(row=row+1, column=4, padx=5, sticky="ew")

            self.items.append((item, amount, price, reason, comment)) # add this to an item details

            # Button to delete an item from the focused table
            tk.Button(headers_frame, text="X", command=lambda table_id=table_number-1, item_id=row: remove_command(table_id, item_id)).grid(row=row+1, column=5, padx=5)

            if value_changed_command:
                price.bind("<FocusOut>", value_changed_command)
                price.bind("<Return>", value_changed_command)
                amount.bind("<<ComboboxSelected>>", value_changed_command)
                reason.bind("<<ComboboxSelected>>", value_changed_command)
                comment.bind("<FocusOut>", value_changed_command)
                comment.bind("<Return>", value_changed_command)

        # Bind the click to switch between the focus on the tables
        self.bind("<Button-1>", lambda event, table_id=table_number-1: focus_command(table_id))
        
        # Total Payment label
        self.total = tk.Label(self, text=f"{LANGUAGE[language]['total']}: {total:.2f} SEK", bg='lightgray')
        self.total.pack(anchor='w', pady=5)

    def get_values(self):
        """ Get the values from the item details """
        return [{'item': item[0].cget('text'), 'amount': int(item[1].get()), 'price': float(item[2].get()), 'reason': item[3].get(), 'comment': item[4].get()} for item in self.items]
    
    def set_values(self, table_data, language, total):
        """ Set the values from the item details """
        for i, item in enumerate(self.items):
            item[0].config(text=table_data[i]['item'])
            item[1].set(table_data[i]['amount'])
            item[2].delete(0, tk.END)
            item[2].insert(0, f"{table_data[i]['price']:.2f}")
            item[3].set(table_data[i]['reason'])
            item[4].delete(0, tk.END)
            item[4].insert(0, table_data[i]['comment'])

        self.total.config(text=f"{LANGUAGE[language]['total']}: {total:.2f} SEK")


class BartenderPanel(BaseView):
    """ The Bartender panel component view class

        Here are all the widgets that are going to be available for the bartender panel component view

        Attributes:
            BaseView: the inherited class BaseView
    """

    def __init__(self, parent, current_language, current_resolution, *args, **kwargs):
        """ Initial method

            Args:
                parent: used to get the tk window/frame
                current_language: used to get the current language of the system
                current_resolution: used to get the current resolution of the window
        """

        super().__init__(parent, current_language, current_resolution, *args, **kwargs) # inherit from BaseView

        self.current_language = current_language

        self.current_table = 0
        self.remove_command = None
        self.value_changed_command = None
        
        # User Info and Panic Button in Horizontal Layout
        user_panic_frame = tk.Frame(self, bg=self.background_color)
        user_panic_frame.pack(fill='x', pady=5)
        
        # Name frame
        self.name_frame = tk.Frame(user_panic_frame, bg=self.background_color)
        self.name_frame.pack(side="left",fill="both", expand=True, padx=0)

        # Welcome message label
        self.welcome_label = tk.Label(self.name_frame, text=LANGUAGE[self.current_language]["welcome"], font=self.default_font, bg=self.background_color)
        self.welcome_label.pack(side="left", anchor="e")

        # Username naming label
        self.name_label = tk.Label(self.name_frame, font=self.default_font, bg=self.background_color)
        self.name_label.pack(side="left", anchor="e")

        # SOS button
        self.panic_button = tk.Button(user_panic_frame, text=LANGUAGE[self.current_language]["panic"], bg="red", fg="white", font=("Arial", 12, "bold"))
        self.panic_button.pack(side='right', expand=True, fill='both')

        # Frame for tables' view
        self.table_frames = []
        self.table_frame = tk.Frame(self, bg='white')
        self.table_frame.pack(fill='both', expand=True)

        # Frame for holding 4 action buttons at corners
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", fill="both", expand=True)

        # Configure grid to evenly distribute buttons (2x2)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.rowconfigure(0, weight=1)

        # Button at the bottom-left (Single Payment)
        self.single_payment_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["single payment"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.single_payment_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Button at the bottom-right (Group Payment)
        self.group_payment_button = tk.Button(
            self.button_frame,
            text=LANGUAGE[self.current_language]["group payment"],
            bg=self.primary_color,
            fg="white",
            font=self.default_font
        )
        self.group_payment_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def _add_table(self, table_number, language, table_data=[], total=0):
        """ Update the table data

            Args:
                table_number: number of the table
                language: current language
                table_data: list of table data
                total: total table data
        """

        # Constructor for the frames of the table management
        table_frame = TableFrame(self.table_frame, table_number, language, table_data, total, self.value_changed_command, self.remove_command, self.focus_changed)
        table_frame.pack(fill='x', pady=10)
        self.table_frames.append(table_frame)

    def _clear_tables(self):
        """ Clear the tables' data """
        for table_frame in self.table_frames:
            table_frame.destroy()
        self.table_frames = []

    def set_value_changed_command(self, command):
        """ Used for changing the focus of the tables command"""
        self.value_changed_command = command

    def set_remove_command(self, command):
        """ Used for item removal command """
        self.remove_command = command

    def get_values(self):
        """ Get values """
        return [table.get_values() for table in self.table_frames]
    
    def focus_changed(self, table_id):
        """ Change the focus of the tables based on the table_id
            and have a visual representation to see which table is focused
        """

        self.table_frames[self.current_table].config(borderwidth=0)
        self.current_table = table_id
        self.table_frames[self.current_table].config(borderwidth=2, relief='solid')
    
    def update_value(self, tables, language):
        """ Update the items' value data from tables

        Args:
            tables (list): List of dictionaries containing table data
            e.g. [[{'item': 'item1', 'price': 10, 'comment': 'comment1'}, {'item': 'item2', 'price': 20, 'comment': 'comment2'}]]
            language: current language
        """

        for i, data in enumerate(tables):
            total = sum([item['amount'] * item['price'] for item in data])
            self.table_frames[i].set_values(data, language, total)

    def update_table(self, tables, language, current_table=0):
        """ Update the table data

        Args:
            tables (list): List of dictionaries containing table data
            e.g. [[{'item': 'item1', 'price': 10, 'comment': 'comment1'}, {'item': 'item2', 'price': 20, 'comment': 'comment2'}]]
            language: current language
            current_table: current table number
        """
        self._clear_tables()
        for i, data in enumerate(tables):
            total = sum([item['price'] for item in data])
            self._add_table(i+1, language, data, total)
        self.focus_changed(current_table)
        
# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bartender Panel")
    panel = BartenderPanel(root, "English", 1)
    panel.pack(fill='both', expand=True, padx=10, pady=10)
    panel.update_table([[{'item': 'item1', 'price': 10, 'reason': 'Normal', 'comment': 'comment1'}, {'item': 'item2', 'price': 20, 'reason': 'Normal', 'comment': 'comment2'}], [], []])
    root.mainloop()
