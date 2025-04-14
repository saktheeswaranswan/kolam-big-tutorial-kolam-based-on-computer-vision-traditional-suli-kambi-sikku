import turtle
import math
import time
import csv
import json

# Configs
dot_radius = 10
iterations = 2
step_size = 10
colors = ['red', 'green', 'blue', 'orange', 'purple', 'magenta', 'cyan']

movements = []
dot_positions = []

# Log turtle movements with timestamp
def log_movement(x, y):
    timestamp = time.time()
    movements.append({'timestamp': timestamp, 'x': round(x, 2), 'y': round(y, 2)})

# Draw a smooth arc
def arc(radius, angle):
    turtle.circle(radius, angle)

# Apply L-System rules
def apply_l_system(axiom, rules, iterations):
    for _ in range(iterations):
        axiom = ''.join([rules.get(symbol, symbol) for symbol in axiom])
    return axiom

# Draw Kolam pattern centered at (x, y)
def draw_kolam_at(x, y, pattern, step_size):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.setheading(0)  # Face right by default

    for symbol in pattern:
        turtle.pensize(3)
        turtle.color('blue')  # Uniform color, no randomness
        if symbol == 'F':
            turtle.forward(step_size)
            log_movement(turtle.xcor(), turtle.ycor())
        elif symbol == 'A':
            arc(10, 90)
            log_movement(turtle.xcor(), turtle.ycor())
        elif symbol == 'B':
            I = 5 / math.sqrt(2)
            turtle.forward(I)
            arc(I, 270)
            turtle.forward(I)
            log_movement(turtle.xcor(), turtle.ycor())

# Read boundary dot positions from CSV
def load_dot_positions_from_csv(filename):
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            x, y = int(row['x']), int(row['y'])
            dot_positions.append((x, y))

# Draw colored dot markers at center points
def place_dots(radius):
    turtle.penup()
    for x, y in dot_positions:
        turtle.goto(x, y)
        turtle.dot(radius, 'black')  # Uniform dot style
        log_movement(x, y)

# Save turtle movement logs
def save_logs():
    with open("each_dot_kolam_movements.json", "w") as jf:
        json.dump(movements, jf, indent=4)
    with open("each_dot_kolam_movements.csv", "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=["timestamp", "x", "y"])
        writer.writeheader()
        writer.writerows(movements)

# Main function
def main():
    turtle.bgcolor("white")
    turtle.speed(0)
    turtle.hideturtle()

    load_dot_positions_from_csv("square_boundary.csv")
    place_dots(dot_radius)

    # Define L-System Kolam pattern
    axiom = "FBFBFBFB"
    rules = {'A': 'AFBFA', 'B': 'AFBFBFBFA'}
    pattern = apply_l_system(axiom, rules, iterations)

    turtle.speed(3)

    # Draw Kolam at each boundary point
    for x, y in dot_positions:
        draw_kolam_at(x, y, pattern, step_size)

    save_logs()
    print("✔ Kolam drawn at square boundary points. Logs saved.")
    turtle.done()

if __name__ == '__main__':
    main()

