import numpy as np


def mat_gauss(size, sigma, normalize=False):
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
    if normalize:
        kernel = gauss / gauss.sum()
    else:
        kernel = gauss
    return kernel


sizes = [3, 5, 7]
sigma = 1.0

for size in sizes:
    unnormal = mat_gauss(size, sigma)
    normal = mat_gauss(size, sigma, normalize=True)

    print("Unnormal Gauss Kernel size ", size, "x", size, ": \n", unnormal, "\n")
    print("Normal Gauss Kernel size ", size, "x", size, ": \n", normal, "\n")

