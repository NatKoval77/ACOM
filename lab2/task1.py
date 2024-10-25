import cv2
import numpy as np


def cam_hsv():
    video = cv2.VideoCapture(0)
    while True:
        ok, frame = video.read()
        if ok:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.imshow('HSV', hsv)
            if cv2.waitKey(10) & 0xFF == 27:
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


cam_hsv()