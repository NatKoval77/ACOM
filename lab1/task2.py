import cv2

img1 = cv2.imread('C:/edu/4-1/acom/lab1/cherry.jpg', cv2.IMREAD_ANYCOLOR)
img2 = cv2.imread('C:/edu/4-1/acom/lab1/cherry.jpg', cv2.IMREAD_REDUCED_GRAYSCALE_2)
img3 = cv2.imread('C:/edu/4-1/acom/lab1/cherry.jpg', cv2.IMREAD_COLOR)

cv2.namedWindow('first', cv2.WINDOW_AUTOSIZE)
cv2.imshow('first', img1)
cv2.namedWindow('second', cv2.WINDOW_FULLSCREEN)
cv2.imshow('second', img2)
cv2.namedWindow('third', cv2.WINDOW_NORMAL)
cv2.imshow('third', img3)

cv2.waitKey(0)
cv2.destroyAllWindows()
