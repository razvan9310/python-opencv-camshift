__author__ = 'razvan'

import cv2

clicked = False
x0 = -1
x1 = -1
y0 = -1
y1 = -1

def on_mouse(event, x, y, flags, params):
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
while True:
    ret, frame = capture.read()
    if x1 != -1:
        cv2.rectangle(frame, (x0, y0), (x1, y1), (255, 0, 0))
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()