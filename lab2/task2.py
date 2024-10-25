import cv2
import numpy as np


def cam_red():
    video = cv2.VideoCapture(0)
    while True:
        ok, frame = video.read()
        if ok:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # [0, 120, 120] - низ; [7, 255, 255] - верх; [172, 150, 150] - низ; [180, 255, 255] - верх
            # HSV в OpenCV представлено в виде полуокружности от 0 до 180 градусов
            redl1 = np.array([0, 120, 120])
            redu1 = np.array([7, 255, 255])
            redl2 = np.array([172, 150, 150])
            redu2 = np.array([180, 255, 255])
            red1 = cv2.inRange(hsv, redl1, redu1)
            red2 = cv2.inRange(hsv, redl2, redu2)
            red = cv2.add(red1, red2)
            redframe = cv2.bitwise_and(frame, frame, mask = red)
            cv2.imshow('Frame', frame)
            cv2.imshow('Mask', red)
            cv2.imshow('Red', redframe)         
            if cv2.waitKey(10) & 0xFF == 27:
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


cam_red()