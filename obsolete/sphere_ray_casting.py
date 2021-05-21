import numpy as np
import matplotlib.pyplot as plt
import math


num_points = 1000
turn_fraction = (1.0 + math.sqrt(5.0)) / 2.0
indices = np.arange(0, num_points, dtype=float) + 0.5
ax = plt.axes(projection='3d')

xs = []
ys = []
zs = []

sphere_radius = 3

for index in indices:
    r = (index / num_points)
    inclination = np.arccos(1 - 2 * r)
    azimuth = 2 * math.pi * turn_fraction * index

    x = math.sin(inclination) * math.cos(azimuth)
    y = math.sin(inclination) * math.sin(azimuth)
    z = math.cos(inclination)

    xs.append(x*sphere_radius*1000)
    ys.append(y*sphere_radius*1000)
    zs.append(z*sphere_radius*1000)


ax.scatter3D(xs, ys, zs, s=3)
ax.scatter3D(0, 0, 0, s=10)
plt.show()
