from turtle import *
from math import sqrt

def line(x1, y1, x2, y2):
    penup()
    goto(x1, y1)
    pendown()
    goto(x2, y2)

def poly(x, y, d, i, base_y):
    # Calculate the mirror and offset coordinates
    x_mir = -x
    x2 = x + 10 * i
    y2 = base_y - 10
    x2_mir = -x2
    x3 = -10 * i
    y3 = y + 20 * d
    x3_mir = -x3
    # Draw the 6-line polygon connecting these points
    line(x, y, x_mir, y) 
    line(x_mir, y, x2_mir, y2)
    line(x2_mir, y2, x3, y3)
    line(x3, y3, x3_mir, y3)
    line(x3_mir, y3, x2, y2)
    line(x2, y2, x, y)

def triangle(x, y, base_y):
    pencolor('yellow')
    # Draw triangle from point (x, y) to its mirror and a fixed endpoint
    x_mir = -x
    line(x, y, x_mir, y)
    line(x_mir, y, 0, base_y - 10)
    line(0, base_y - 10, x, y)

def putkolam():
    # Set up the background and input:
    bgcolor('black')
    # Request number of dots from the user (even if very high)
    n = numinput('Extendable KoLam', 'Dots (e.g., 4,6,8,... up to 1000):', default=6)
    n = int(n)
    
    # For large n, we can adjust our base offsets and forward step.
    base_y = -200
    step = 20          # Horizontal step between dots
    row_dx = 10        # x offset per row
    row_dy = 20        # y offset per row
    # Determine starting x so that the pattern is centered
    start_x = -10 * (n - 1)
    
    tracer(0)  # Turn off animation for speed
    # --- Draw dot pattern (upper half) ---
    l = n
    x, y = start_x, base_y
    for row in range(n):
        penup()
        goto(x, y)
        for _ in range(l):
            dot(3, 'white')
            penup()
            forward(step)
        x += row_dx
        y += row_dy
        l -= 2  # Reduce number of dots per subsequent row

    # --- Draw connecting polygon elements ---
    d = n - 1
    i = 1
    x = -10 * n
    y = base_y + 10
    # Number of polygon rows based on half the dot count
    rows = int(n / 2)
    for _ in range(rows):
        pencolor('white')
        poly(x, y, d, i, base_y)
        i += 1
        d -= 2
        x += row_dx
        y += row_dy
    # --- If odd number of dots, add a triangle closure ---
    if n % 2 != 0:
        triangle(x, y, base_y)
    update()  # Refresh the screen

def main():
    hideturtle()
    home()
    # Optionally, set up a larger canvas for high dot counts.
    setup(width=1200, height=800)
    putkolam()
    return "Done!"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()

