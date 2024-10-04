import cv2

cam = cv2.VideoCapture(1)

while True:
    ok, frame = cam.read()
    if ok:
        cv2.imshow("Android_cam", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    else:
        break
cam.release()
cv2.destroyAllWindows()