import cv2


def video_rewrite():
    video = cv2.VideoCapture(r'C:/Users/Goe/PycharmProjects/lab5/Rogue.mp4')
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output = cv2.VideoWriter('C:/Users/Goe/PycharmProjects/lab5/Output.mp4', fourcc, fps, (w, h))
    _, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_frame = cv2.GaussianBlur(gray, (15, 15), 1)

    while True:
        ok, frame = video.read()
        if ok:
            gauss2fr = cv2.GaussianBlur(frame, (15, 15), 1)
            now_frame = cv2.cvtColor(gauss2fr, cv2.COLOR_BGR2GRAY)
            frame_diff = cv2.absdiff(now_frame, prev_frame)
            _, thresh_frame = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            flag = False

            for c in contours:
                print(cv2.contourArea(c))
                if cv2.contourArea(c) > 200:
                    flag = True
                    break

            if flag:
                output.write(frame)

            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

            prev_frame = now_frame
        else:
            break

    video.release()
    output.release()
    print("Record complete!")
    cv2.destroyAllWindows()


def play_rewrote(src):
    cap = cv2.VideoCapture(src)
    while True:
        ok, frame = cap.read()
        if ok:
            cv2.imshow('video', frame)
            if cv2.waitKey(50) & 0xFF == 27:
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


video_rewrite()
play_rewrote('C:/Users/Goe/PycharmProjects/lab5/Output.mp4')
