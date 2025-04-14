from turtle import *
import time
import csv
import json

yr = -200
movements = []

def log_movement(x, y):
    timestamp = time.time()
    movements.append({'timestamp': timestamp, 'x': x, 'y': y})

def line(x1p, y1p, x2p, y2p):
    pu()
    goto(x1p, y1p)
    log_movement(xcor(), ycor())
    pd()
    goto(x2p, y2p)
    log_movement(xcor(), ycor())

def draw_square_grid(n, size=20):
    """Draw a square grid of dots based on input n."""
    x_start = -size * (n // 2)
    y_start = yr + size * (n // 2)
    
    for row in range(n):
        for col in range(n):
            x = x_start + col * size
            y = y_start - row * size
            pu()
            goto(x, y)
            log_movement(xcor(), ycor())
            dot(3, 'black')

def save_logs():
    with open("kolam_movements.json", "w") as jf:
        json.dump(movements, jf, indent=4)
    with open("kolam_movements.csv", "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=["timestamp", "x", "y"])
        writer.writeheader()
        writer.writerows(movements)

def putkolam():
    bgcolor('white')
    color('black')
    speed(1)  # Adjust for visible animation
    n = numinput('Extendable Kolam', 'Dots (1,2,3...):')
    n = int(n)
    draw_square_grid(n)
    save_logs()

def main():
    ht()
    home()
    putkolam()
    tracer(1)
    return "Done!"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()

