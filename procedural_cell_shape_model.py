import matplotlib.pyplot as plt
import numpy as np
import random
import math
from skimage import io


def cart2sph(x,y,z):
    XsqPlusYsq = x**2 + y**2
    r = math.sqrt(XsqPlusYsq + z**2)               # r
    elev = math.atan2(z, math.sqrt(XsqPlusYsq))     # theta
    az = math.atan2(y, x)                           # phi
    return r, elev, az


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


def get_cell_landmarks_random_sorted(cell, num_landmarks):
    num_points = num_landmarks
    print(cell.shape)
    zs, ys, xs = np.nonzero(cell)

    all_cell_point_locations = []
    for x, y, z in zip(xs, ys, zs):
        all_cell_point_locations.append((x, y, z))

    all_cell_point_locations_np = np.asarray(all_cell_point_locations)
    # print(all_cell_point_locations_np.shape)
    mean = np.sum(all_cell_point_locations_np, axis=0) / all_cell_point_locations_np.shape[0]

    sampled_cell_point_locations = random.sample(all_cell_point_locations, num_points)
    # sort cells by azimuth and incline

    sampled_cell_point_locations_with_spherical = []

    for point in sampled_cell_point_locations:
        radius, elevation, azimuth = cart2sph(point[0], point[1], point[2])
        sampled_cell_point_locations_with_spherical.append((point[0], point[1], point[2], radius, elevation, azimuth,
                                                            math.floor(point[2]/10)))


    # sorting in some kind of cylindrical coordinates
    #  sort by z and then each z bin by azimuth
    sampled_cell_point_locations_sorted_by_azimuth = sorted(sampled_cell_point_locations_with_spherical, key=lambda tup: tup[5])
    sampled_cell_point_locations_sorted_by_z_bin = sorted(sampled_cell_point_locations_sorted_by_azimuth, key=lambda tup: tup[6])

    landmarks_random = []

    for point in sampled_cell_point_locations_sorted_by_z_bin:
        # print(point)
        landmarks_random.append(point[0] - mean[0])
        landmarks_random.append(point[1] - mean[1])
        landmarks_random.append(point[2] - mean[2])

    return landmarks_random

def get_cell_landmarks_spherical_projection(cell, cell_filled_in, num_landmarks):
    num_points = num_landmarks
    print(cell.shape)
    zs, ys, xs = np.nonzero(cell)

    all_cell_point_locations = []

    for x, y, z in zip(xs, ys, zs):
        all_cell_point_locations.append((x, y, z))

    all_cell_point_locations_np = np.asarray(all_cell_point_locations)
    # print(all_cell_point_locations_np.shape)
    mean = np.sum(all_cell_point_locations_np, axis=0) / all_cell_point_locations_np.shape[0]

    # generate sphere
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

        sphere_xs.append(sphere_x * sphere_radius + mean[0])
        sphere_ys.append(sphere_y * sphere_radius + mean[1])
        sphere_zs.append(sphere_z * sphere_radius + mean[2])

    end_voxel = (math.floor(mean[0]), math.floor(mean[1]), math.floor(mean[2]))
    sampled_cell_point_locations_sphere = []

    for sphere_x, sphere_y, sphere_z in zip(sphere_xs, sphere_ys, sphere_zs):
        start_voxel = (math.floor(sphere_x), math.floor(sphere_y), math.floor(sphere_z))

        path = bresenham_3d(start_voxel[0], start_voxel[1], start_voxel[2], end_voxel[0], end_voxel[1], end_voxel[2])

        for location in path:
            if 0 <= location[2] < cell_filled_in.shape[0] and 0 <= location[1] < cell_filled_in.shape[1] and 0 <= \
                    location[0] < cell_filled_in.shape[2]:
                if cell_filled_in[location[2]][location[1]][location[0]] > 0:
                    sampled_cell_point_locations_sphere.append(location)
                    break

    # sampled_xs_sphere = []
    # sampled_ys_sphere = []
    # sampled_zs_sphere = []

    landmarks_sphere = []

    for point in sampled_cell_point_locations_sphere:
        landmarks_sphere.append(point[0] - mean[0])
        landmarks_sphere.append(point[1] - mean[1])
        landmarks_sphere.append(point[2] - mean[2])
        # print(point)
        # sampled_xs_sphere.append(point[0])
        # sampled_ys_sphere.append(point[1])
        # sampled_zs_sphere.append(point[2])

    return landmarks_sphere


def pdm(landmarks, eigenshape_num):

    landmarks = np.array(landmarks)

    # print(landmarks.shape)
    mean = np.sum(landmarks, axis=0) / landmarks.shape[0]
    # ax.scatter3D(mean[0::3], mean[1::3], mean[2::3], color="green")

    covariance_matrix = np.zeros((landmarks.shape[1], landmarks.shape[1]))
    for landmarks_cell in landmarks:
        # print(landmarks_cell)
        covariance_matrix += np.matmul((landmarks_cell - mean), np.transpose(landmarks_cell - mean))

    covariance_matrix = covariance_matrix / (landmarks.shape[0] - 1)

    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    eigenvalues = np.asarray(list(map(lambda x: x.real, eigenvalues)))
    eigenvectors = np.asarray(list(map(lambda x: x.real, eigenvectors)))

    i = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[i]
    eigenvectors = eigenvectors[:, i]

    print("eigenvals", eigenvalues)
    print("eigenvecs", eigenvectors)

    #k = random.uniform(-1.0, 1.0)
    new_shape = mean + (1 * math.sqrt(abs(eigenvalues[eigenshape_num])) * eigenvectors[eigenshape_num])

    xs = new_shape[0::3]
    ys = new_shape[1::3]
    zs = new_shape[2::3]

    plot_size = 200
    ax = plt.axes(projection='3d')
    ax.set_title("Eigenshape " + str(eigenshape_num + 1) )
    ax.scatter3D(xs, ys, zs, s=3, color="blue")
    ax.set_xlim3d(-plot_size, plot_size)
    ax.set_ylim3d(-plot_size, plot_size)
    ax.set_zlim3d(-plot_size, plot_size)
    plt.show()


if __name__ == "__main__":

    #random.seed(23)

    img_names = ["AICS-10_48_4.ome.tif", "AICS-10_40_1.ome.tif", "AICS-10_63_6.ome.tif", "AICS-10_33_7.ome.tif",
                  "AICS-10_3_7.ome.tif",] #"AICS-10_34_5.ome.tif", "AICS-10_42_6.ome.tif", "AICS-10_70_4.ome.tif",
                 #"AICS-10_55_2.ome.tif", "AICS-10_46_1.ome.tif",] # end here!!! "AICS-10_28_1.ome.tif", "AICS-10_52_1.ome.tif",
                 # "AICS-10_82_1.ome.tif", "AICS-10_47_2.ome.tif", "AICS-10_31_1.ome.tif", "AICS-10_32_5.ome.tif",
                 # "AICS-10_59_9.ome.tif", "AICS-10_34_6.ome.tif", "AICS-10_68_4.ome.tif", "AICS-10_37_2.ome.tif",
                 # "AICS-10_54_2.ome.tif", "AICS-10_36_1.ome.tif", "AICS-10_29_1.ome.tif", "AICS-10_47_1.ome.tif",
                 # "AICS-10_46_2.ome.tif", "AICS-10_64_6.ome.tif", "AICS-10_73_2.ome.tif", "AICS-10_37_3.ome.tif",
                 # "AICS-10_58_9.ome.tif", "AICS-10_70_3.ome.tif", "AICS-10_64_3.ome.tif", "AICS-10_51_3.ome.tif",
                 # "AICS-10_35_1.ome.tif", "AICS-10_58_5.ome.tif", "AICS-10_63_8.ome.tif", "AICS-10_44_10.ome.tif",
                 # "AICS-10_43_3.ome.tif", "AICS-10_64_2.ome.tif", "AICS-10_33_1.ome.tif", "AICS-10_27_1.ome.tif",
                 # "AICS-10_39_1.ome.tif", "AICS-10_71_3.ome.tif", "AICS-10_31_4.ome.tif", "AICS-10_53_7.ome.tif",
                 # "AICS-10_56_2.ome.tif", "AICS-10_0_7.ome.tif", "AICS-10_63_3.ome.tif", "AICS-10_51_1.ome.tif",
                 # "AICS-10_60_7.ome.tif", "AICS-10_35_3.ome.tif" ]

    # 5: anotirana celica
    # 0: observed membrana
    # 7: anotiran rob celice (membrana)

    landmarks = []

    for img_name in img_names:
        img = io.imread("./images/" + img_name)
        cell = img[:, 7, :, :]
        cell_filled_in = img[:, 5, :, :]

        #landmarks_cell = get_cell_landmarks_spherical_projection(cell, cell_filled_in, 400)
        landmarks_cell = get_cell_landmarks_random_sorted(cell, 800)
        landmarks.append(landmarks_cell)

    for eigenshape_num in range(3):
        pdm(landmarks, eigenshape_num)