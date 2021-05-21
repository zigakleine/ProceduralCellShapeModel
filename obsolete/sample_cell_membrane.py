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

img_names = ["AICS-10_48_4.ome.tif"]

# 5: anotirana celica
# 0: observed membrana
# 7: anotiran rob celice(membrana)

img = io.imread("./images/" + img_names[0])
cell = img[:, 7, :, :]
cell_filled_in = img[:, 5, :, :]

import numpy as np
from scipy import signal



import numpy as np
from scipy import signal

# # first build the smoothing kernel
# sigma = 0.01     # width of kernel
# x = np.arange(-3,4,1)   # coordinate arrays -- make sure they contain 0!
# y = np.arange(-3,4,1)
# z = np.arange(-3,4,1)
# xx, yy, zz = np.meshgrid(x,y,z)
# kernel = np.exp(-(xx**2 + yy**2 + zz**2)/(2*sigma**2))
#
#
# cell = signal.convolve(cell, kernel, mode="same")


print(cell.shape)
zs, ys, xs = np.nonzero(cell)

all_cell_point_locations = []

for x, y, z in zip(xs, ys, zs):
    all_cell_point_locations.append((x, y, z))


all_cell_point_locations_np = np.asarray(all_cell_point_locations)
print(all_cell_point_locations_np.shape)
mean = np.sum(all_cell_point_locations_np, axis=0) / all_cell_point_locations_np.shape[0]



num_points = 1000
turn_fraction = (1.0 + math.sqrt(5.0)) / 2.0
indices = np.arange(0, num_points, dtype=float) + 0.5
sphere_radius = 1000

sphere_xs = []
sphere_ys = []
sphere_zs = []

for index in indices:
    radius = index / num_points
    inclination = np.arccos(1 - 2 * radius)
    azimuth = 2 * math.pi * turn_fraction * index

    sphere_x = math.sin(inclination) * math.cos(azimuth)
    sphere_y = math.sin(inclination) * math.sin(azimuth)
    sphere_z = math.cos(inclination)

    sphere_xs.append(sphere_x*sphere_radius + mean[0])
    sphere_ys.append(sphere_y*sphere_radius + mean[1])
    sphere_zs.append(sphere_z*sphere_radius + mean[2])

end_voxel = (math.floor(mean[0]), math.floor(mean[1]), math.floor(mean[2]))
sampled_cell_point_locations_sphere = []

for sphere_x, sphere_y, sphere_z in zip(sphere_xs, sphere_ys, sphere_zs):
    start_voxel = (math.floor(sphere_x), math.floor(sphere_y), math.floor(sphere_z))

    path = bresenham_3d(start_voxel[0], start_voxel[1], start_voxel[2], end_voxel[0], end_voxel[1], end_voxel[2])

    for location in path:
        if 0 <= location[2] < cell_filled_in.shape[0] and 0 <= location[1] < cell_filled_in.shape[1] and 0 <= location[0] < cell_filled_in.shape[2]:
            if cell_filled_in[location[2]][location[1]][location[0]] > 0:
                sampled_cell_point_locations_sphere.append(location)
                break

sampled_cell_point_locations = random.sample(all_cell_point_locations, num_points)
# sort cells


sampled_xs_sphere = []
sampled_ys_sphere = []
sampled_zs_sphere = []

sampled_xs = []
sampled_ys = []
sampled_zs = []

for point in sampled_cell_point_locations_sphere:
    # print(point)
    sampled_xs_sphere.append(point[0])
    sampled_ys_sphere.append(point[1])
    sampled_zs_sphere.append(point[2])

for point in sampled_cell_point_locations:
    # print(point)
    sampled_xs.append(point[0])
    sampled_ys.append(point[1])
    sampled_zs.append(point[2])




ax = plt.axes(projection='3d')
ax.scatter3D(sampled_xs_sphere, sampled_ys_sphere, sampled_zs_sphere, color="blue")
ax.scatter3D(mean[0], mean[1], mean[2],  color="red")
ax.set_title("Cell with sphere sampling")
plt.show()

ax2 = plt.axes(projection='3d')
ax2.scatter3D(sampled_xs, sampled_ys, sampled_zs, color="blue")
ax2.scatter3D(mean[0], mean[1], mean[2], color="red")
ax2.set_title("Cell with random sampling")
plt.show()


ax3 = plt.axes(projection='3d')
ax3.scatter3D(sphere_xs, sphere_ys, sphere_zs, color="blue")
ax3.scatter3D(mean[0], mean[1], mean[2], color="red")
ax3.set_title("Sphere")
plt.show()


print(len(sampled_xs), len(sampled_xs_sphere))
# for layer in cell:
#     plt.imshow(layer)
#     plt.show()