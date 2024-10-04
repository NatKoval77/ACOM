
import cv2
import numpy as np


def cam_show():
    video = cv2.VideoCapture(0)
    while True:
        ok, frame = video.read()
        if ok:
            height, width, _ = frame.shape # высота ширина
            up_angle = ( width // 5, height // 2 - 30)
            down_angle = (4 * width // 5, height // 2 + 30)
            up_ang = ( width // 2 - 30, height // 6)
            down_ang = (width // 2 + 30, 5 * height // 6)
            center = frame[height // 2, width // 2]
            if center[2] > center[1] and center[2] > center[0]:
                color = (0, 0, 255) #Red
            elif center[1] > center[2] and center[1] > center[0]:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            cv2.rectangle(frame, up_angle, down_angle, color, -1) #BGR (Red 255)
            cv2.rectangle(frame, up_ang, down_ang, color, -1)
            cv2.imshow('COLOR PLUS', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()

cam_show()