# =============================================================================
# Author: Lars Oestreicher
# Date: 3/3 2025
# =============================================================================
# This file contains a Python program which uses PyGame to manage the handling
# of a simple interface to a system for use in the Flying Dutchman application.
# The different constructs in the file are intended to point to various ideas
# on how to implement functionality that is used to handle the interaction with
# users. It does NOT contain the backend needed for handling the data points.
#
# All code in this file can be used without constraints, but it is still suggested
# that you implement this from scratch with this code as an inspiration. This will
# help you to understand the principles, rather than just reusing the code. Some of
# the code here is also duplicated for clarity and it is recommended that you find
# ways of restructuring the code. in order to use it.
#
# General imports
#
import pygame
import random

# Local imports
#
import BackEnd as be

# The PIL library is needed if you want to have an image placed in the
# graphic for an item. Currently it is not used. 
#
import PIL

# Initialize pygame
#
pygame.init()

# Constant window size definitions. Note that if we want to resize this dynamically
# it has to be rendered in a function that checks for window resizing.
#
WIDTH, HEIGHT = 1000, 800
SIDE_BAR = 200
MENU_WIDTH = (WIDTH - SIDE_BAR) * 0.6
DRINK_MENU_HEIGHT = HEIGHT / 2
FOOD_MENU_HEIGHT = HEIGHT / 2
ORDER_WIDTH = WIDTH - SIDE_BAR - MENU_WIDTH

# Here we define the positions of various buttons. This can be useful
# if we want to add many buttons, and also check for clicks inside.
# This is also very useful to store other entities, such as the color
# definitions below.
#
button_positions = {
    "Quit": {"pos": (WIDTH - SIDE_BAR + 20, 20, SIDE_BAR - 40, 30),
             "func": be.QuitFunction()},

    "Other": {"pos": (WIDTH - SIDE_BAR + 20, 60, SIDE_BAR - 40, 30),
              "func": be.OtherFunction()},
    "Pay": {"pos": (WIDTH - SIDE_BAR + 20, 100, SIDE_BAR - 40, 30),
            "func": be.PayFunction()}
}

# Predefined colors for the display
#
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (200, 220, 255)
GREEN = (120, 200, 120)
LIGHTRED = (255, 220, 220)
TURQUISE = (100, 220, 220)
SCROLL_BAR_COLOR = (180, 150, 150)

# Create the main window. This is slightly different from how you would do it in tkinter.
#
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Layout and handling ideas for the Flying Dutchman. Pygame!")

# Load example images (Replace with real images here). The images are defined as
# surfaces in pygame. In this way we can create the images and store them in the
# appropriate format later. If we use real images we have to use the pillow library
# to add the images.
#
drink_image = pygame.Surface((60, 60))
drink_image.fill(BLUE)

# Generate example databases, one for drinks and one for foods, we still use the same
# dummy image here. These databases will have to be replaced by calls to the real
# database with instantiated data.
#
drink_data = [
    {"name": f"Drink {i + 1}", "price": random.randint(30, 100), "image": drink_image}
    for i in range(45)
]
food_data = [
    {"name": f"Course {i + 1}", "price": random.randint(30, 100), "image": drink_image}
    for i in range(10)
]

# We also need to have an order list to move items to. This will be handled in a separate
# list, which is empty to start with.
#
order_list = []

# Variables used to define the different menus.
#
# If we instead use drink_size = (100, 60), it makes it possible
# to have different formats on the items.
#
drink_size = 100  # Size of each menu item (the items are square shaped).
food_size = 100
drink_columns = 4  # Number of columns for the drinks in the grid
food_columns = 3
rows_visible = 4  # Number of visible rows

# Our own scroll bar item
#
menu_scroll = 0.0  # Current scroll position (float for smooth scrolling)
target_scroll = 0.0  # Target scroll position
scroll_speed = 0.2  # Speed of smooth scrolling

# Defining some other interconnected variables.
#
drink_menu_items_per_row = drink_columns
food_menu_items_per_row = food_columns
menu_items_visible = rows_visible * drink_menu_items_per_row
total_rows = (len(drink_data) + drink_columns - 1) // drink_columns  # Total rows in the menu
max_scroll = max(0, total_rows - rows_visible)  # Max scroll position

# Scrollbar control variables
#
scrolling = False  # Track if the scrollbar is being dragged
scroll_bar_rect = pygame.Rect(0, 0, 0, 0)  # Placeholder for scrollbar rectangle

# Drag & Drop variables
#
dragging = None
drag_pos = (0, 0)
drag_offset_x = 0
drag_offset_y = 0

# The clock is used to run pygame animations.
#
clock = pygame.time.Clock()


#  We will use linear interpolation (lerp) for smooth transitions, for example
#  when scrolling.
#
def lerp(a, b, t):
    return a + (b - a) * t


# The sidebar can as in this example be used to keep an interactive menu of buttons.
# The creation of a header will be left as an exercise.
#
# If we want to have a border on an area, we need to paint the item twice, one for the fill,
# and one for the border.
def draw_side_bar():
    pygame.draw.rect(screen, TURQUISE, (WIDTH - SIDE_BAR, 0, WIDTH - SIDE_BAR, HEIGHT - 1), width=0)  # Fill
    pygame.draw.rect(screen, BLACK, (WIDTH - SIDE_BAR, 0, WIDTH - SIDE_BAR, HEIGHT - 1), width=1)  # Border

    # The addition of buttons is automated here.
    #
    add_button(button_positions["Quit"]["pos"], "Quit")
    add_button(button_positions["Other"]["pos"], "Other")  # This button is just a dummy.
    add_button(button_positions["Pay"]["pos"], "Cash")     # This button is just a dummy


# The drawing of Buttons is automated. Changes in this definition can be used to create
# different types of buttons, for example, default buttons.
#
# For this example we haven't calculated the positions of the text. Longer texts will
# not be centered.
#
def add_button(pos, txt):
    pygame.draw.rect(screen, WHITE, pos, width=0, border_radius=10)  # Fill
    pygame.draw.rect(screen, BLACK, pos, width=1, border_radius=10)  # Border
    font = pygame.font.Font(None, 30)  # The font needs to be rendered with
    text = font.render(txt, True, BLACK)  # the text.
    screen.blit(text, (pos[0] + 60, pos[1] + 8))  # The text is positioned here.


# Draw the menu for drinks with its content. It is important to remember that
# we have to draw things in the correct order. From the bottom and up. This
# will be used to stop the drawings to be painted over each other.
#
def draw_drink_menu():

    # The base rectangle!
    #
    pygame.draw.rect(screen, LIGHTRED, (0, 0, MENU_WIDTH, DRINK_MENU_HEIGHT), border_radius=20)

    # Smoothly interpolate scroll position. We create a scrollbar for the drinks menu.
    #
    global menu_scroll
    menu_scroll = lerp(menu_scroll, target_scroll, scroll_speed)

    # Calculate the starting position for the scroll bar.
    #
    start_index = max(0, int(menu_scroll) * drink_menu_items_per_row)

    # We only show the number of beverages that will fit on the screen
    #
    visible_drinks = drink_data[start_index:]

    # Go through the database of drinks and add them to the menu
    # in a matrix with some distance between the items (the number 10 below) both
    # vertically and horisontally.
    #
    for index, drink in enumerate(visible_drinks):
        row = index // drink_columns
        col = index % drink_columns
        x = col * drink_size + 10
        y = row * drink_size + 10 - (menu_scroll % 1) * drink_size  # Smooth fractional offset

        # Hide items outside the screen
        #
        if y + drink_size < 0 or y > DRINK_MENU_HEIGHT:
            continue

        # Create a combined object to draw on the menu.
        #
        pygame.draw.rect(screen, WHITE, (x, y, drink_size - 10, drink_size - 10), border_radius=10)

        # The "blit" is a function to combine objects into a combined object. This makes it easier
        # to move the objects when they are dragged.
        #
        screen.blit(drink["image"], (x + 10, y + 10))

        # Again we render the text for the font. This could be made into a function
        #
        font = pygame.font.Font(None, 20)
        text = font.render(f"{drink['name']} {drink['price']}kr", True, BLACK)
        screen.blit(text, (x + 5, y + drink_size - 30))

    # Draw scrollbar if needed
    #
    if max_scroll > 0:
        scroll_bar_height = DRINK_MENU_HEIGHT * (rows_visible / total_rows)  # Dynamic height
        scroll_bar_y = (DRINK_MENU_HEIGHT - scroll_bar_height) * (menu_scroll / max_scroll)  # Position
        global scroll_bar_rect
        scroll_bar_rect = pygame.Rect(MENU_WIDTH - 10, scroll_bar_y + 10, 8, scroll_bar_height - 10)
        pygame.draw.rect(screen, SCROLL_BAR_COLOR, scroll_bar_rect)


# The food menu is exactly the same as the drink menu. They should therefore be generalised.
# This is left as an exercice. Note that positioning might become a problem!
#
def draw_food_menu():
    pygame.draw.rect(screen, GREEN, (0, DRINK_MENU_HEIGHT, MENU_WIDTH, HEIGHT), border_radius=20)

    # Here we don't use the scroll bar, so start_index = 0
    start_index = 0
    visible_foods = food_data[start_index:]

    # Go through the database of drinks and add them to the menu
    #
    for index, food in enumerate(visible_foods):
        row = index // food_columns
        col = index % food_columns
        x = col * food_size + 10
        y = FOOD_MENU_HEIGHT + row * food_size + 10  # Smooth fractional offset
        if y + food_size < 0 or y > HEIGHT:  # Hide items outside the screen
            continue

        # Create a combined object to draw on the menu.
        #
        pygame.draw.rect(screen, WHITE,
                         (x, y, food_size - 10, food_size - 10),
                         border_radius=10)

        # The "blit" is a function to combine objects into a combined object. This makes it easier
        # to move the objects when they are dragged.
        #
        screen.blit(food["image"], (x + 10, y + 10))

        font = pygame.font.Font(None, 20)
        text = font.render(f"{food['name']} {food['price']}kr", True, BLACK)
        screen.blit(text, (x + 5, y + food_size - 30))


# The order list is easier to draw. But this can probably be optimised too.
#
def draw_order_list():
    pygame.draw.rect(screen, GREEN, (MENU_WIDTH, 0, ORDER_WIDTH, HEIGHT))
    font = pygame.font.Font(None, 30)

    # Dynamic adding of items, so they dont end up overlapping with each other.
    #
    y_offset = 10
    for item in order_list:
        text = font.render(f"{item['name']} - {item['price']}kr", True, BLACK)
        screen.blit(text, (MENU_WIDTH + 10, y_offset))
        y_offset += 30


# Detect which drink is at a certain point. Position is a tuple of x and y.
#
def get_drink_at_pos(pos):
    """Returns the drink at the clicked position in the menu."""
    x, y = pos
    if x >= MENU_WIDTH:
        return None

    start_index = int(menu_scroll) * drink_menu_items_per_row
    visible_drinks = drink_data[start_index:]

    # Calculate which item we have selected in the list. Here we get the names and the
    # prices.
    #
    for index, drink in enumerate(visible_drinks):
        row = index // drink_columns
        col = index % drink_columns
        x_start = col * drink_size + 10
        y_start = row * drink_size + 10 - (menu_scroll % 1) * drink_size  # Apply smooth scrolling
        rect = pygame.Rect(x_start, y_start, drink_size - 10, drink_size - 10)

        # Here we detect the click position.
        #
        if rect.collidepoint(pos):
            return drink, x_start, y_start

    # If there is no collision we just return nothing
    #
    return None


# This function is duplicated, How can we make the two into a general function?
# Left as an exercise.
#
def get_food_at_pos(pos):
    """Returns the drink at the clicked position in the menu."""
    x, y = pos
    if x >= MENU_WIDTH:
        return None

    start_index = 0
    visible_foods = food_data[start_index:]

    for index, food in enumerate(visible_foods):
        row = index // food_columns
        col = index % food_columns
        x_start = col * food_size + 10
        y_start = row * food_size + 10  # Apply smooth scrolling
        rect = pygame.Rect(x_start, y_start + DRINK_MENU_HEIGHT,
                           food_size - 10, food_size - 10)

        if rect.collidepoint(pos):
            return food, x_start, y_start + DRINK_MENU_HEIGHT

    return None


# This function tests the mouseUp. If the pointer is above any of the
# buttons, the corresponding "execute" functions in the backend will
# be called.
#
def check_buttons(pos):
    for item in button_positions:
        temp = button_positions[item]["pos"]
        # The positions are stored in a Rect object.
        if pygame.Rect(temp).collidepoint(pos):
            button_positions[item]["func"].execute()


# This boolean variable is used to stop the loop.
#
running = True

# This will be the main loop
#
while running:
    screen.fill(WHITE)
    draw_drink_menu()
    draw_food_menu()
    draw_order_list()
    draw_side_bar()

    # Draw dragged item
    if dragging:
        pygame.draw.rect(screen, GREEN,
                         (drag_pos[0] - drag_offset_x,
                          drag_pos[1] - drag_offset_y,
                          drink_size - 10,
                          drink_size - 10))
        screen.blit(dragging["image"],
                    (drag_pos[0] - drag_offset_x + 10,
                     drag_pos[1] - drag_offset_y + 10))

    # The flip() function updates the display (!)
    #
    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            # Get new window size
            WIDTH, HEIGHT = event.w, event.h

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if scroll_bar_rect.collidepoint(event.pos):  # Clicked on scrollbar
                    scrolling = True
                else:
                    # Check for drink menu items
                    drink_data_at_pos = get_drink_at_pos(event.pos)
                    if drink_data_at_pos:
                        dragging, drag_x, drag_y = drink_data_at_pos
                        drag_pos = event.pos
                        drag_offset_x = event.pos[0] - drag_x
                        drag_offset_y = event.pos[1] - drag_y

                    # Check for dragging food menu items
                    food_data_at_pos = get_food_at_pos(event.pos)
                    if food_data_at_pos:
                        dragging, drag_x, drag_y = food_data_at_pos
                        drag_pos = event.pos
                        drag_offset_x = event.pos[0] - drag_x
                        drag_offset_y = event.pos[1] - drag_y

        # If we lift the mouse button we activate the function that should be performed
        # This is an important part of the system, this is where we detect what should be
        # done in the database.
        #
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dragging and event.pos[0] > MENU_WIDTH:  # Dropped in the order list
                    order_list.append(dragging)  # This should be a call to the model.

                dragging = None  # Finish the mouse action
                scrolling = False  # Stop dragging scrollbar

                check_buttons(event.pos)

        # Define what happens when we move the mouse with the button down.
        #
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                drag_pos = event.pos  # Ensure dragged item follows the mouse
            if scrolling:  # Drag scrollbar
                relative_y = event.pos[1] / DRINK_MENU_HEIGHT  # Get percentage of window height
                target_scroll = max(0, min(max_scroll, relative_y * max_scroll))  # Adjust scroll position

        # Using mouse wheel for scrolling.
        #
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up (mouse wheel)
                target_scroll = max(0, target_scroll - 1)
            elif event.button == 5:  # Scroll down (mouse wheel)
                target_scroll = min(max_scroll, target_scroll + 1)

        # Scrolling with arrow keys
        #
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Scroll up with arrow key
                target_scroll = max(0, target_scroll - 1)
            elif event.key == pygame.K_DOWN:  # Scroll down with arrow key
                target_scroll = min(max_scroll, target_scroll + 1)

pygame.quit()