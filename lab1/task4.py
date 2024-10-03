import cv2


def video():
    cap = cv2.VideoCapture(r'C:/edu/4-1/acom/lab1/venice.mp4')
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


def video_writer():
    video = cv2.VideoCapture(r'C:/edu/4-1/acom/lab1/venice.mp4')
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    writer = cv2.VideoWriter('C:/edu/4-1/acom/lab1/output.mp4', fourcc, 25, (w, h))

    while True:
        ok, vid = video.read()
        if ok:
            cv2.imshow('Video', vid)
            writer.write(vid)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    video.release()
    writer.release()
    cv2.destroyAllWindows()


video_writer()
