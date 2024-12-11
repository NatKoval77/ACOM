import numpy as np


def mat_gauss(size, sigma):
    center = size // 2
    gauss = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            gauss[x, y] = (
                    (1 / (2 * np.pi * sigma ** 2)) *
                    np.exp(
                        -((x - center) ** 2 + (y - center) ** 2)
                        / (2 * sigma ** 2)
                    )
            )
    return gauss


sizes = [3, 5, 7]
sigma = 1.0

for size in sizes:
    gauss = mat_gauss(size, sigma)
    print("Gauss Kernel size ", size, "x", size, ": \n", gauss, "\n")

