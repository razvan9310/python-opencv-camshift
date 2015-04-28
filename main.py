__author__ = 'razvan'

import cv2
import numpy as np
import sys

clicked = False
x0 = -1
x1 = -1
y0 = -1
y1 = -1

awaiting_face = True
face_x0 = 0
face_x1 = 0
face_y0 = 0
face_y1 = 0

def on_mouse(event, x, y, flags, params):
    if not awaiting_face:
        return
    global clicked, x0, x1, y0, y1
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        x0 = x
        y0 = y
        x1 = -1
    elif event == cv2.EVENT_MOUSEMOVE:
        if clicked:
            x1 = x
            y1 = y
    elif event == cv2.EVENT_LBUTTONUP:
        clicked = False

capture = cv2.VideoCapture(0)
cv2.namedWindow('Video', 0)
cv2.resizeWindow('Video', 640, 480)
cv2.setMouseCallback('Video', on_mouse)
ret, frame = capture.read()
while True:
    ret, frame = capture.read()
    if ret:
        if x1 != -1:
            cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), thickness=2)
        cv2.imshow('Video', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('f'):
            if awaiting_face:
                face_x0 = x0
                face_x1 = x1
                face_y0 = y0
                face_y1 = y1
                awaiting_face = False
                break
    else:
        break

if awaiting_face:
    sys.exit(1)

track_window = (x0, y0, x1 - x0, y1 - y0)
roi = frame[y0: y1, x0: x1]
hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while not awaiting_face:
    ret, frame = capture.read()
    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        cv2.ellipse(frame, ret, (0, 0, 255), 2)
        cv2.imshow('Video', frame)

        key = cv2.waitKey(60) & 0xFF
        if key == ord('q'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()