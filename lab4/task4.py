import cv2
import numpy as np


# completed third step of Canny algorithm - gradient direction found and non-maxima suppression is completed
def blur_grad(src):
    img = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    cv2.imshow("Gray cherry", img)
    blured = cv2.GaussianBlur(img, (3, 3), 5.0)  # better (3, 3) & 5.0
    cv2.imshow("Blured cherry", blured)

    sobel_x = cv2.Sobel(blured, cv2.CV_64F, 1, 0, ksize=3)  # array of Gx
    sobel_y = cv2.Sobel(blured, cv2.CV_64F, 0, 1, ksize=3)  # array of Gy
    len_grad = np.sqrt(sobel_x ** 2 + sobel_y ** 2)  # value(magnitude) of gradient is length of vector
    fee = np.arctan2(sobel_y, sobel_x)

    rows, columns = len_grad.shape
    tg_fee = np.tan(fee)
    sub = np.zeros((rows, columns))
    non_max = np.zeros((rows, columns), dtype=np.uint8)
    for r in range(1, rows - 1):
        for c in range(1, columns - 1):
            # 0 gradient direction
            if (sobel_x[r, c] > 0 > sobel_y[r, c] and tg_fee[r, c] < -2.414) | (
                    sobel_x[r, c] < 0 and sobel_y[r, c] < 0 and tg_fee[r, c] > -2.414):
                sub[r, c] = len_grad[r, c]
            # 1
            elif sobel_x[r, c] > 0 > sobel_y[r, c] and tg_fee[r, c] < -0.414:
                sub[r, c] = len_grad[r, c]
            # 2
            elif (sobel_x[r, c] > 0 > sobel_y[r, c] and tg_fee[r, c] > -0.414) | (
                    sobel_x[r, c] > 0 and sobel_y[r, c] > 0 and tg_fee[r, c] < 0.414):
                sub[r, c] = len_grad[r, c]
            # 3
            elif sobel_x[r, c] > 0 and sobel_y[r, c] > 0 and tg_fee[r, c] < 2.414:
                sub[r, c] = len_grad[r, c]
            # 4
            elif (sobel_x[r, c] > 0 and sobel_y[r, c] > 0 and tg_fee[r, c] > 2.414) | (
                    sobel_x[r, c] < 0 < sobel_y[r, c] and tg_fee[r, c] < -2.414):
                sub[r, c] = len_grad[r, c]
            # 5
            elif sobel_x[r, c] < 0 < sobel_y[r, c] and tg_fee[r, c] < -0.414:
                sub[r, c] = len_grad[r, c]
            # 6
            elif (sobel_x[r, c] < 0 < sobel_y[r, c] and tg_fee[r, c] > -0.414) | (
                    sobel_x[r, c] < 0 and sobel_y[r, c] < 0 and tg_fee[r, c] < 0.414):
                sub[r, c] = len_grad[r, c]
            # 7
            elif sobel_x[r, c] < 0 and sobel_y[r, c] < 0 and tg_fee[r, c] < 2.414:
                sub[r, c] = len_grad[r, c]

            maxim = np.max(sub[r - 1:r + 2, c - 1:c + 2])  # not include operation
            # px is greater or equal than maximum value among the neighbors
            if len_grad[r, c] >= maxim:
                non_max[r, c] = len_grad[r, c]

    cv2.imshow("Non-max cherry", non_max)

    max_grad = np.max(len_grad)
    low_level = max_grad // 25
    high_level = max_grad // 10
    threshold = np.zeros((rows, columns), dtype=np.uint8)
    low = 40  # better low level
    high = 15  # better high level
    # double threshold filtering
    for r in range(1, rows):
        for c in range(1, columns):
            if non_max[r,c] >= 35:
                threshold[r,c] = 255
            elif non_max[r,c] <= 15:
                threshold[r,c] = 0

    cv2.imshow("Canny", threshold)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


blur_grad("C:/Users/Goe/PycharmProjects/cherry.jpg")
