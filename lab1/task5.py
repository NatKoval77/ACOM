import cv2


def cam_show():
    video = cv2.VideoCapture(0)

    while True:
        ok, frame = video.read()
        if ok:
            frame = cv2.resize(frame, (640, 480))
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.imshow('HSV', hsv)
            cv2.imshow('RGB', frame)
            if cv2.waitKey(10) & 0xFF == 27:
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


cam_show()