
import numpy as np
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import random
import math


# Python3 code for generating points on a 3-D line
# using Bresenham's Algorithm
# source: https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/
def bresenham_3d(x1, y1, z1, x2, y2, z2):
    ListOfPoints = []
    ListOfPoints.append((x1, y1, z1))
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)
    if (x2 > x1):
        xs = 1
    else:
        xs = -1
    if (y2 > y1):
        ys = 1
    else:
        ys = -1
    if (z2 > z1):
        zs = 1
    else:
        zs = -1

    # Driving axis is X-axis"
    if (dx >= dy and dx >= dz):
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while (x1 != x2):
            x1 += xs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dx
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
            ListOfPoints.append((x1, y1, z1))

    # Driving axis is Y-axis"
    elif (dy >= dx and dy >= dz):
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while (y1 != y2):
            y1 += ys
            if (p1 >= 0):
                x1 += xs
                p1 -= 2 * dy
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
            ListOfPoints.append((x1, y1, z1))

    # Driving axis is Z-axis"
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while (z1 != z2):
            z1 += zs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dz
            if (p2 >= 0):
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            ListOfPoints.append((x1, y1, z1))
    return ListOfPoints



def normalize_vec(vec):
    length = math.sqrt(vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2])
    normalized = (vec[0] / length, vec[1] / length, vec[2] / length)
    return normalized

cell = np.zeros((5, 5, 5))
for i in range(5):
    for j in range(5):
        cell[i][2][j] = 1

cell = np.array(cell, dtype=bool)

xs = [2.5, 2.5]
ys = [0.5, 4.5]
zs = [2.5, 2.5]

ray = (xs[1] - xs[0], ys[1] - ys[0], zs[1] - zs[0])
# ray_norm = normalize_vec(ray)
# print(ray_norm)

xs_vox = [math.floor(x) for x in xs]
ys_vox = [math.floor(y) for y in ys]
zs_vox = [math.floor(z) for z in zs]

list_of_points = bresenham_3d(xs_vox[0], ys_vox[0], zs_vox[0], xs_vox[1], ys_vox[1], zs_vox[1])
print(list_of_points)

path = np.zeros((5, 5, 5))
path = np.array(path, dtype=bool)

for point in list_of_points:
    path[point[2]][point[1]][point[0]] = True



start_position = (math.floor(xs[0]), math.floor(ys[0]), math.floor(zs[0]))
print(start_position)





# and plot everything
ax = plt.figure().add_subplot(projection='3d')
ax.voxels(cell)
ax.voxels(path)
ax.plot(xs, ys, zs, color="red")

plt.show()