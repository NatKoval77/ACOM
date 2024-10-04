import cv2

def cam_writer():
    video = cv2.VideoCapture(0)
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    writer = cv2.VideoWriter('C:/edu/4-1/acom/lab1/cam.mp4', fourcc, 25, (w, h))
    while True:
        ok, frame = video.read()
        if ok:
            cv2.imshow('Video', frame)
            writer.write(frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            break
    video.release()
    writer.release()
    cv2.destroyAllWindows()

cam_writer()