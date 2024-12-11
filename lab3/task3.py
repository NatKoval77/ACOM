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


size = 5
sigma = 1.0
kernel = mat_gauss(size, sigma)
img = cv2.imread('C:/edu/4-1/acom/lab3/cherry.jpg', cv2.IMREAD_GRAYSCALE)
blured_img = filter(img, kernel)
cv2.imshow('initial img: ', img)
cv2.imshow('filtred img: ', blured_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
