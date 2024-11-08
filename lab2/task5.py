import cv2
import numpy as np

cap = cv2.VideoCapture(0)
iLastX = iLastY = -1
alpha = 0.5

while True:
    ok, frame = cap.read()
    if ok:
        imgLines = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
        imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        red1 = cv2.inRange(imgHSV, np.array([0, 120, 120]), 
                            np.array([7, 255, 255]))
        red2 = cv2.inRange(imgHSV, np.array([172, 150, 150]), 
                            np.array([180, 255, 255]))
        red = cv2.bitwise_or(red1, red2)
        kernel = np.ones((5, 5), np.uint8)
        both = cv2.erode(red, kernel)
        both = cv2.dilate(red, kernel)
        both = cv2.dilate(red, kernel)
        both = cv2.erode(red, kernel)
        moments = cv2.moments(both)
        m01 = moments['m01']
        m10 = moments['m10']
        area = moments['m00']

        if area > 300:
            w = h = int(np.sqrt(area))
            w//=20
            h//=20
            posX = int(m10 / area)
            posY = int(m01 / area)

            if iLastX >= 0 and iLastY >= 0:
                posX = int(alpha * iLastX + (1-alpha)*posX)
                posY = int(alpha * iLastY + (1-alpha)*posY)
                cv2.rectangle(imgLines, (posX - w, posY - h), 
                    (posX + w, posY + h), (0, 0, 255), 2)

            iLastX = posX
            iLastY = posY

        imgOriginal = cv2.add(frame, imgLines)
        cv2.imshow("masked", both)
        cv2.imshow("with rectang's", imgOriginal)
        if cv2.waitKey(10) & 0xFF == 27:
            break
    else:
        break
    
cap.release()
cv2.destroyAllWindows()