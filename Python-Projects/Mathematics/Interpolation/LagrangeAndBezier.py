import numpy as np
import matplotlib.pyplot as plt

def lagrange(x_points, y_points):
    final_formula = []
    for i, yp in enumerate(y_points):
        factor = yp / float(np.prod([x_points[i]-x_points[j] for j in range(len(x_points)) if j != i]))
        final_formula.append([factor, [-x_points[j] for j in range(len(x_points)) if j != i]])
    print(final_formula)

def get_point(x1, y1, x2, y2, t):
    delta_y = y2-y1
    delta_x = x2-x1
    return [x1 + delta_x * t, y1 + delta_y * t]

def bezier(cx, cy, num_samples):
    # Quadratic
    if len(cx) == 3:
        points = []
        for t in np.linspace(0, 1, num_samples):
            t = float(t)
            point_1 = get_point(cx[0], cy[0], cx[1], cy[1], t)
            point_2 = get_point(cx[1], cy[1], cx[2], cy[2], t)
            point_3 = get_point(point_1[0], point_1[1], point_2[0], point_2[1], t)
            points.append(point_3)
        return points
    
cx = [1, 2, 3]
cy = [2, 4, -1]
points = bezier(cx, cy, 100)
x_points = [p[0] for p in points]
y_points = [p[1] for p in points]

plt.plot(x_points, y_points)
for k in range(len(cx)):
    plt.plot(cx[k], cy[k], "bo")

plt.show()
