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
            cv2.rectangle(frame, up_angle, down_angle, (0, 0, 255), 2) #BGR (Red 255)
            up_ang = ( width // 2 - 30, height // 6)
            down_ang = (width // 2 + 30, 5 * height // 6)
            cv2.rectangle(frame, up_ang, down_ang, (0, 0, 255), 2)
            cv2.imshow('Target', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()

cam_show()