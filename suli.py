import turtle
from turtle import *
import math

# Global offset for panning
offset_x = 0
offset_y = 0

# Global variables to keep track of the drawing mode and parameters.
# mode: "square" or "custom"
current_mode = None  
side_length = 400    # side length for square-dot mode (boundary dots)
num_dots = 10        # number of dots per side for square-dot mode
custom_coords = []   # list of (x,y) tuples for custom dots

# --------------------- Drawing Functions ---------------------

def draw_square_dots():
    """Draw dots along the boundary of a square centered at (0,0) using the global offset."""
    spacing = side_length / (num_dots - 1)
    pencolor("red")
    dot_size = 5

    # Top side: from left to right.
    for i in range(num_dots):
        x = -side_length/2 + i * spacing + offset_x
        y = side_length/2 + offset_y
        penup(); goto(x, y); dot(dot_size)
    # Bottom side: from left to right.
    for i in range(num_dots):
        x = -side_length/2 + i * spacing + offset_x
        y = -side_length/2 + offset_y
        penup(); goto(x, y); dot(dot_size)
    # Left side: excluding already drawn corners.
    for i in range(1, num_dots - 1):
        x = -side_length/2 + offset_x
        y = side_length/2 - i * spacing + offset_y
        penup(); goto(x, y); dot(dot_size)
    # Right side: excluding corners.
    for i in range(1, num_dots - 1):
        x = side_length/2 + offset_x
        y = side_length/2 - i * spacing + offset_y
        penup(); goto(x, y); dot(dot_size)

def draw_custom_dots():
    """Draw custom dots using a list of coordinates (relative to center) and the global offset."""
    pencolor("blue")
    dot_size = 7
    for (x, y) in custom_coords:
        penup()
        goto(x + offset_x, y + offset_y)
        dot(dot_size)

def redraw():
    """Clear the screen and redraw the current dot pattern with the current offsets."""
    clear()
    if current_mode == "square":
        draw_square_dots()
    elif current_mode == "custom":
        draw_custom_dots()
    update()

# --------------------- Panning Functions ---------------------

def move_up():
    global offset_y
    offset_y += 20
    redraw()

def move_down():
    global offset_y
    offset_y -= 20
    redraw()

def move_left():
    global offset_x
    offset_x -= 20
    redraw()

def move_right():
    global offset_x
    offset_x += 20
    redraw()

# --------------------- Main Program ---------------------

def main():
    global current_mode, side_length, num_dots, custom_coords, offset_x, offset_y
    turtle.setup(800, 800)
    turtle.bgcolor("black")
    hideturtle()
    speed(0)
    tracer(0)  # Turn off animation for fast drawing
    title("Boundary & Custom Dot Pattern with Panning")

    # Ask user which mode to draw.
    mode_choice = textinput("Select Mode", "Enter 'square' for boundary square dots or 'custom' for custom dots:")
    if mode_choice is None:
        return
    mode_choice = mode_choice.strip().lower()
    
    if mode_choice == "square":
        current_mode = "square"
        # Ask for side length and number of dots per side.
        side_str = textinput("Square Dots", "Enter side length (e.g., 400):")
        num_str = textinput("Square Dots", "Enter number of dots per side (e.g., 10):")
        try:
            side_length = float(side_str)
            num_dots = int(num_str)
        except:
            side_length = 400
            num_dots = 10
        # Initialize offset to zero.
        offset_x = 0
        offset_y = 0
        redraw()
    elif mode_choice == "custom":
        current_mode = "custom"
        # Ask user for custom dot coordinates.
        # Expected format: x1,y1;x2,y2;... (e.g. "100,50;-50,-100;0,0")
        coords_str = textinput("Custom Dots", "Enter custom dot coordinates as x,y pairs separated by semicolons:")
        custom_coords = []
        try:
            pairs = coords_str.split(";")
            for pair in pairs:
                if pair.strip():
                    x_str, y_str = pair.split(",")
                    custom_coords.append((float(x_str), float(y_str)))
        except Exception as e:
            print("Error parsing coordinates, using default custom dots.")
            custom_coords = [(0,0), (100,0), (100,100), (0,100)]
        offset_x = 0
        offset_y = 0
        redraw()
    else:
        print("Invalid mode selected.")
        return

    # Bind arrow keys for panning.
    listen()
    onkey(move_up, "Up")
    onkey(move_down, "Down")
    onkey(move_left, "Left")
    onkey(move_right, "Right")
    update()
    mainloop()

if __name__ == "__main__":
    main()

