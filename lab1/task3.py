import cv2


def video():
    cap = cv2.VideoCapture('C:/edu/4-1/acom/lab1/venice.mp4')
    while True:
        ok, frame = cap.read()
        if ok:
            frame = cv2.resize(frame, (640, 480))
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.imshow('video', hsv)
            if cv2.waitKey(10) & 0xFF == 27:
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


video()
