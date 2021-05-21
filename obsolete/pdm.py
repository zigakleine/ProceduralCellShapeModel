import math
import numpy as np
import matplotlib.pyplot as plt
import random

def displace_curve_randomly(x_curve, y_curve, margin):
    x_displaced = []
    y_displaced = []
    for x, y in zip(x_curve, y_curve):
        x_new = x + random.uniform(-margin, margin)
        y_new = y + random.uniform(-margin, margin)

        x_displaced.append(x_new)
        y_displaced.append(y_new)
    return x_displaced, y_displaced

def create_curve(idx):
    if idx == 0:
        N = 40
        v = 1.0

        v = np.linspace(5 * math.pi, 0, N)
        x = np.cos(v) * v
        y = np.sin(v) * v

        return x, y

    elif idx == 1:
        N = 40

        v = np.linspace(5 * math.pi, -5 * math.pi, N)
        print(v)
        x = np.cos(v) * v
        y = v

        return x, y

    elif idx == 2:
        # theta goes from 0 to 2pi
        theta = np.linspace(0, 2 * np.pi, 40)
        r = 15
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        return x, y


def pdm(landmarks):
    ax = plt.axes(projection='3d')
    landmarks = np.array(landmarks)

    print(landmarks.shape)
    mean = np.sum(landmarks, axis=0) / landmarks.shape[0]
    ax.scatter3D(mean[0::3], mean[1::3], mean[2::3], color="green")

    covariance_matrix = np.zeros((landmarks.shape[1], landmarks.shape[1]))
    for landmarks_set in landmarks:
        # print(landmarks_set)
        covariance_matrix += np.matmul((landmarks_set - mean), np.transpose(landmarks_set - mean))

    covariance_matrix = covariance_matrix / (landmarks.shape[0] - 1)

    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    eigenvalues = np.asarray(list(map(lambda x: x.real, eigenvalues)))
    eigenvectors = np.asarray(list(map(lambda x: x.real, eigenvectors)))

    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    print("eigenvals", eigenvalues)
    print("eigenvecs", eigenvectors)

    k = random.uniform(-1.0, 1.0)

    new_shape = mean + (k * 3 * math.sqrt(abs(eigenvalues[0])) * eigenvectors[0])

    xs = new_shape[0::3]
    ys = new_shape[1::3]
    zs = new_shape[2::3]

    ax.scatter3D(xs, ys, zs, color="blue")
    plt.show()

landmarks = []

for i in range(80):
    idx=0
    x_curve, y_curve = create_curve(idx)
    x_disp, y_disp = displace_curve_randomly(x_curve, y_curve, 2.0)

    landmarks_row = []
    for x, y in zip(x_disp, y_disp):
        landmarks_row.append(x)
        landmarks_row.append(y)
    landmarks.append(landmarks_row)

    plt.plot(x_disp, y_disp, color="red")


landmarks = np.array(landmarks)

print(landmarks.shape)

mean = np.sum(landmarks, axis=0) / landmarks.shape[0]

plt.plot(mean[0::2], mean[1::2], color="green")

covariance_matrix = np.zeros((landmarks.shape[1], landmarks.shape[1]))

for landmarks_set in landmarks:
    #print(landmarks_set)
    covariance_matrix += np.matmul((landmarks_set - mean), np.transpose(landmarks_set - mean))

covariance_matrix = covariance_matrix / (landmarks.shape[0] - 1)

eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

eigenvalues = np.asarray(list(map(lambda x: x.real, eigenvalues)))
eigenvectors = np.asarray(list(map(lambda x: x.real, eigenvectors)))

idx = eigenvalues.argsort()[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]


print("eigenvals", eigenvalues)
print("eigenvecs", eigenvectors)

k = random.uniform(-1.0, 1.0)

new_shape = mean + (k * 3 * math.sqrt(abs(eigenvalues[0])) * eigenvectors[0]) + (k * 3 * math.sqrt(abs(eigenvalues[1])) * eigenvectors[1])

xs = new_shape[0::2]
ys = new_shape[1::2]

plt.plot(xs, ys, color="blue")

plt.show()

# napari