import cv2


# completed first step of Canny algorithm - applying Gaussian filter to remove noises
def blur(src):
    img = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    cv2.imshow("Gray cherry", img)
    blured = cv2.GaussianBlur(img, (5, 5), 1.0)
    cv2.imshow("Blured cherry", blured)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


blur("C:/Users/Goe/PycharmProjects/cherry.jpg")
