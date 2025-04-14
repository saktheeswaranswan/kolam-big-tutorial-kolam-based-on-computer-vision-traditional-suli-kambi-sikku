import csv
import turtle
import time
import json

movements = []
yr = -200  # Starting y-coordinate

def log_movement(x, y):
    timestamp = time.time()
    movements.append({'timestamp': timestamp, 'x': x, 'y': y})

def line(x1p, y1p, x2p, y2p):
    turtle.penup()
    turtle.goto(x1p, y1p)
    log_movement(turtle.xcor(), turtle.ycor())
    turtle.pendown()
    turtle.goto(x2p, y2p)
    log_movement(turtle.xcor(), turtle.ycor())

def arc(radius, angle):
    turtle.circle(radius, angle)

def apply_l_system(axiom, rules, iterations):
    for _ in range(iterations):
        axiom = ''.join([rules.get(symbol, symbol) for symbol in axiom])
    return axiom

def draw_from_l_system(axiom, step_size):
    for symbol in axiom:
        if symbol == 'F':
            turtle.forward(step_size)
        elif symbol == 'A':
            arc(10, 90)
        elif symbol == 'B':
            arc(5, 270)
        # Add more symbols here if needed

def import_csv(file_name):
    pattern_data = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            pattern_data.append(row)
    return pattern_data

def save_logs():
    with open("kolam_movements.json", "w") as jf:
        json.dump(movements, jf, indent=4)
    with open("kolam_movements.csv", "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=["timestamp", "x", "y"])
        writer.writeheader()
        writer.writerows(movements)

def putkolam():
    turtle.bgcolor('white')
    turtle.color('black')
    turtle.speed(1)
    
    # L-system setup
    axiom = "FBFBFBFB"  # Example axiom
    rules = {'A': 'AFBFA', 'B': 'AFBFBFBFA'}  # L-system rules
    iterations = 2  # Example iterations
    step_size = 10
    
    # Apply L-system rules and generate the pattern
    pattern = apply_l_system(axiom, rules, iterations)
    draw_from_l_system(pattern, step_size)

def main():
    turtle.hideturtle()
    turtle.home()
    putkolam()
    save_logs()
    turtle.tracer(1)
    return "Done!"

if __name__ == '__main__':
    msg = main()
    print(msg)
    turtle.mainloop()

