import csv
import matplotlib.pyplot as plt

def generate_square_boundary_points(x_min, x_max, y_min, y_max, step=1):
    points = []

    # Bottom side (left to right)
    for x in range(x_min, x_max + 1, step):
        points.append((x, y_min))

    # Right side (bottom to top)
    for y in range(y_min + step, y_max + 1, step):
        points.append((x_max, y))

    # Top side (right to left)
    for x in range(x_max - step, x_min - 1, -step):
        points.append((x, y_max))

    # Left side (top to bottom)
    for y in range(y_max - step, y_min, -step):
        points.append((x_min, y))

    return points

def export_to_csv(filename, points):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x", "y"])
        for point in points:
            writer.writerow(point)

def plot_points(points):
    x_vals, y_vals = zip(*points)
    plt.figure(figsize=(6, 6))
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='blue')
    plt.title("Square Boundary Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('equal')
    plt.grid(True)
    plt.show()

# Square bounds (unit step)
x_min, x_max = 0, 10
y_min, y_max = 0, 10

# Generate points and export
boundary_points = generate_square_boundary_points(x_min, x_max, y_min, y_max)
export_to_csv("square_boundary.csv", boundary_points)

# Plot on canvas
plot_points(boundary_points)

