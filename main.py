import threading
import winsound
import cv2
import imutils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap_set = cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap_set = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_,start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_status = False
alarm_counter = 0

def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_status:
            break
        print("ALARM!")
        winsound.Beep(2500, 1000)
    alarm = False

while True:
    _,frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_status:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        diff_frame = cv2.absdiff(frame_bw, start_frame)
        thresh_frame = cv2.threshold(diff_frame, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if thresh_frame.sum() > 300:
            print(thresh_frame.sum())
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow('Camera', thresh_frame)
    else:
        cv2.imshow('Camera', frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord('t'):
        alarm_status = not alarm_status
        alarm_counter = 0
    if key_pressed == ord('q'):
        alarm_status = False
        break
cap.release()
cv2.destroyAllWindows()
         


