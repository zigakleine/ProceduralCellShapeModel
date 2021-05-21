from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import random
import math

def cart2sph(x,y,z):
    XsqPlusYsq = x**2 + y**2
    r = math.sqrt(XsqPlusYsq + z**2)               # r
    elev = math.atan2(z, math.sqrt(XsqPlusYsq))     # theta
    az = math.atan2(y, x)                           # phi
    return r, elev, az

img_names = ["AICS-10_48_4.ome.tif"]

# 5: anotirana celica
# 0: observed membrana
# 7: anotiran rob celice(membrana)

img = io.imread("./images/" + img_names[0])
cell = img[:, 7, :, :]

print(cell.shape)
zs, ys, xs = np.nonzero(cell)

all_cell_point_locations = []

for x, y, z in zip(xs, ys, zs):
    all_cell_point_locations.append((x, y, z))

all_cell_point_locations_np = np.asarray(all_cell_point_locations)
print(all_cell_point_locations_np.shape)
mean = np.sum(all_cell_point_locations_np, axis=0) / all_cell_point_locations_np.shape[0]

all_cell_point_locations = [(p[0] - mean[0], p[1] - mean[1], p[2] - mean[2]) for p in all_cell_point_locations]

num_points = 200
sampled_cell_point_locations = random.sample(all_cell_point_locations, num_points)
# sort cells by azimuth and incline

sampled_cell_point_locations_with_spherical = []

for point in sampled_cell_point_locations:
    radius, elevation, azimuth = cart2sph(point[0], point[1], point[2])

    sampled_cell_point_locations_with_spherical.append((point[0], point[1], point[2], radius, elevation, azimuth))

# sorted by elevation
sampled_cell_point_locations_sorted_by_elevation = sorted(sampled_cell_point_locations_with_spherical, key=lambda tup: tup[4]+tup[5])
#sampled_cell_point_locations_sorted_by_azimuth = sorted(sampled_cell_point_locations_sorted_by_elevation, key=lambda tup: tup[5])

sampled_xs = []
sampled_ys = []
sampled_zs = []

for point in sampled_cell_point_locations_sorted_by_elevation:
    print(point)
    sampled_xs.append(point[0])
    sampled_ys.append(point[1])
    sampled_zs.append(point[2])



ax2 = plt.axes(projection='3d')
ax2.scatter3D(sampled_xs, sampled_ys, sampled_zs, color="blue")
ax2.scatter3D(0, 0, 0, color="red")
ax2.set_title("Cell with random sampling")
plt.show()


print(len(sampled_xs))