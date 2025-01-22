import cv2
import numpy as np


# completed second step of Canny algorithm - gradients of brightness function are calculated
def blur_grad(src):
    img = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    cv2.imshow("Gray cherry", img)
    blured = cv2.GaussianBlur(img, (5, 5), 1.0)
    cv2.imshow("Blured cherry", blured)

    sobel_x = cv2.Sobel(blured, cv2.CV_64F, 1, 0, ksize=3)  # array of Gx
    sobel_y = cv2.Sobel(blured, cv2.CV_64F, 0, 1, ksize=3)  # array of Gy
    len_grad = np.sqrt(sobel_x ** 2 + sobel_y ** 2)  # value(magnitude) of gradient is length of vector
    fee = np.arctan(sobel_y, sobel_x)

    print("value of gradient = ", len_grad)
    print("fee = ", fee)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


blur_grad("C:/Users/Goe/PycharmProjects/cherry.jpg")
