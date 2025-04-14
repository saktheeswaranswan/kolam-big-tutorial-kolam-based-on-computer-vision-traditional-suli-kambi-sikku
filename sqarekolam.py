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

def square(x1, y1, size):
    """ Draw a square based on the starting position (x1, y1) and side length `size` """
    for _ in range(4):
        line(x1, y1, x1 + size, y1)
        x1 += size
        y1 += size
        log_movement(xcor(), ycor())

def put_square_kolam():
    bgcolor('white')
    color('black')
    speed(1)  # Adjust for visible animation
    n = numinput('Square Kolam', 'Dots (1,2,3...):')
    size = 20
    l = n
    xr = (-10) * (n - 1)
    x = xr
    y = yr
    for j in range(int(n)):
        pu()
        goto(x, y)
        log_movement(xcor(), ycor())
        for k in range(int(l)):
            dot(3, 'black')
            pu()
            fd(20)
            log_movement(xcor(), ycor())
        x = x + 10
        y = y + 20
        l = l - 1

    d = n - 1
    i = 1
    x = -10 * int(n)
    y = yr + 10
    l = int(n / 2)
    for j in range(l):
        color('black')
        square(x, y, size)  # Calling square drawing function
        i = i + 1
        d = d - 2
        x = x + 10
        y = y + 20

def save_logs():
    with open("square_kolam_movements.json", "w") as jf:
        json.dump(movements, jf, indent=4)
    with open("square_kolam_movements.csv", "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=["timestamp", "x", "y"])
        writer.writeheader()
        writer.writerows(movements)

def main():
    ht()
    home()
    put_square_kolam()
    save_logs()
    tracer(1)
    return "Done!"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()

