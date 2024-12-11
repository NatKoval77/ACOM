import cv2
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
    kernel = gauss / gauss.sum()
    return kernel


def filter(img, kernel):
    rows, cols = img.shape
    k_center = kernel.shape[0] // 2
    new_image = np.zeros_like(img)  # copy of img
    for i in range(k_center, rows - k_center):
        for j in range(k_center, cols - k_center):
            val = 0.0
            for k in range(kernel.shape[0]):
                for l in range(kernel.shape[1]):
                    img_x = i + k - k_center
                    img_y = j + l - k_center
                    val += img[img_x, img_y] * kernel[k, l]
            new_image[i, j] = min(max(int(val), 0), 255)
    return new_image


option = [(3, 1.0), (3, 3.0), (5, 1.0), (5, 3.0)]
img = cv2.imread('C:/edu/4-1/acom/lab3/cherry.jpg', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (340, 440))
cv2.imshow('initial size: ', img)
for size, sigma in option:
        kernel = mat_gauss(size, sigma)
        blured_img = filter(img, kernel)
        win = f"filtred img - size: {size}, sigma: {sigma}"
        cv2.imshow(win, blured_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
