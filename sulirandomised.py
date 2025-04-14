import turtle
import math
import random
import time
import csv
import json

# Configs
dot_count = 25
dot_radius = 10
iterations = 2
step_size = 10
colors = ['red', 'green', 'blue', 'orange', 'purple', 'magenta', 'cyan']

movements = []
dot_positions = []

# Log turtle movements
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

# Draw Kolam from L-system centered at a dot
def draw_kolam_at(x, y, pattern, step_size):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.setheading(0)  # Reset direction

    for symbol in pattern:
        turtle.color(random.choice(colors))
        turtle.pensize(3)  # Thicker line
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

# Place random colorful dots
def place_dots(count, radius):
    turtle.penup()
    for _ in range(count):
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        dot_positions.append((x, y))
        turtle.goto(x, y)
        turtle.dot(radius, random.choice(colors))
        log_movement(x, y)

# Save movement logs
def save_logs():
    with open("each_dot_kolam_movements.json", "w") as jf:
        json.dump(movements, jf, indent=4)
    with open("each_dot_kolam_movements.csv", "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=["timestamp", "x", "y"])
        writer.writeheader()
        writer.writerows(movements)

# Main Function
def main():
    turtle.bgcolor("white")
    turtle.speed(0)
    turtle.hideturtle()

    place_dots(dot_count, dot_radius)

    # L-System setup
    axiom = "FBFBFBFB"
    rules = {'A': 'AFBFA', 'B': 'AFBFBFBFA'}
    pattern = apply_l_system(axiom, rules, iterations)

    # Draw Kolam centered at each dot
    turtle.speed(3)
    for x, y in dot_positions:
        draw_kolam_at(x, y, pattern, step_size)

    save_logs()
    print("✔ Kolam drawn around each dot with thick colorful lines and timestamped log.")
    turtle.done()

if __name__ == '__main__':
    main()

