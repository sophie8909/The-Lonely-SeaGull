# =======================================================
# IMPORTS
# =======================================================
import tkinter as tk

# We need to use the tkinter dnd library in order to be able to
# perform a drag and drop from the desktop.
#
from tkinterdnd2 import DND_FILES, TkinterDnD


# ============================================================================
# This is a file that defines a small program that illustrates the use of Drag
# and drop between objects in an application and from a desktop file to the
# application.
#
class DragDropApp(TkinterDnD.Tk):

    def __init__(self):
        super().__init__()

        self.title("Drag and Drop Example")
        self.geometry("500x400")

        # Draggable Label (No Text) Note that the size measures are given on the size of
        # the font: Width=10 means 10 characters wide, height=2 means 2 lines tall.
        #
        self.draggable_label = tk.Label(self, text="Drag me", bg="lightblue", relief="raised", width=10, height=2)
        self.draggable_label.place(x=50, y=50)

        # Prepare the eventhandlers for the drag and drop.
        #
        self.draggable_label.bind("<ButtonPress-1>", self.start_drag)
        self.draggable_label.bind("<B1-Motion>", self.on_drag)
        self.draggable_label.bind("<ButtonRelease-1>", self.on_drop)

        # Defining the Drop Target
        #
        self.drop_target = tk.Label(self, text="Drop Here", bg="lightgray", relief="sunken", width=20, height=5)
        self.drop_target.place(x=150, y=200)

        # First we define the external Drag & Drop (From the Desktop to the surface of Tkinter)
        #
        self.drop_target.drop_target_register(DND_FILES)
        self.drop_target.dnd_bind("<<Drop>>", self.on_file_drop)

    # The function called upon the start of dragging
    #
    def start_drag(self, event):
        self.draggable_label.lift()
        self._drag_data = {"x": event.x, "y": event.y}
        self.drop_target.config(bg="yellow")  # Highlight the target for dropping.

    # The event when moving the object
    #
    def on_drag(self, event):
        x = self.draggable_label.winfo_x() + (event.x - self._drag_data["x"])
        y = self.draggable_label.winfo_y() + (event.y - self._drag_data["y"])
        self.draggable_label.place(x=x, y=y)

    # The function that defines what is going to happen in a drop event
    #
    def on_drop(self, event):

        self.drop_target.config(bg="lightgray")  # Reset the highlight of the drop zone

        # Check if the label is over the target
        #
        lx, ly = self.draggable_label.winfo_x(), self.draggable_label.winfo_y()
        tx, ty, tw, th = self.drop_target.winfo_x(), self.drop_target.winfo_y(), self.drop_target.winfo_width(), self.drop_target.winfo_height()

        if tx <= lx <= tx + tw and ty <= ly <= ty + th:
            self.fade_to_white(0)  # Start fade-out effect

    # When we want to animate what's happening whe we drop it, we gradually fade the label
    # to white before we let the label disappear. The fading is done in an internal function.
    def fade_to_white(self, step):
        if step < 10:
            new_color = f"#{255 - step * 20:02x}{255 - step * 20:02x}FF"  # Moves towards white
            self.draggable_label.config(bg=new_color)
            self.after(50, self.fade_to_white, step + 1)
        else:
            self.draggable_label.place_forget()  # Hide label completely
            self.drop_target.config(text="Thanks for the tip-drop!")

    # Define the operation of the external file drop function: from desktop to the surface of
    # the application. In this case we just print the text of the file that was dropped.
    # We could drop an image file on the surface, and in that case we'd make sure that
    #  1. it is a real image in the file.
    #  2. we can open it ourselves and use it in the proper way.
    #
    def on_file_drop(self, event):
        file_path = event.data
        self.drop_target.config(text=f"File Dropped:\n{file_path}")

# =============================================================================
# Run the program.
# =============================================================================
if __name__ == "__main__":
    app = DragDropApp()
    app.mainloop()
# =============================================================================
# End of file DragnDrop.py
# =============================================================================