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

def poly(x1, y1, d, i):
    x11 = -x1
    y11 = y1
    x2 = x1 + 10 * i
    y2 = yr - 10
    x21 = -x2
    y21 = y2
    x3 = -10 * i
    y3 = y1 + 20 * d
    x31 = -x3
    y31 = y3
    line(x1, y1, x11, y11)
    line(x11, y11, x21, y21)
    line(x21, y21, x3, y3)
    line(x3, y3, x31, y31)
    line(x31, y31, x2, y2)
    line(x2, y2, x1, y1)

def triangle(x1, y1):
    color('yellow')
    x11 = -x1
    y11 = y1
    xe = 0
    ye = yr - 10
    line(x1, y1, x11, y11)
    line(x11, y11, xe, ye)
    line(xe, ye, x1, y1)

def putkolam():
    bgcolor('white')
    color('black')
    speed(1)  # Adjust for visible animation
    n = numinput('Extendable Kolam', 'Dots (1,2,3...):')
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
        poly(x, y, d, i)
        i = i + 1
        d = d - 2
        x = x + 10
        y = y + 20

    if n % 2 != 0:
        triangle(x, y)

def save_logs():
    with open("kolam_movements.json", "w") as jf:
        json.dump(movements, jf, indent=4)
    with open("kolam_movements.csv", "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=["timestamp", "x", "y"])
        writer.writeheader()
        writer.writerows(movements)

def main():
    ht()
    home()
    putkolam()
    save_logs()
    tracer(1)
    return "Done!"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()

