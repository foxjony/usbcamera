# USB 2.0 Camera 2K 4MP (RGB Video 2560x1440, 30 fps) (MCU F5253) ($36)
# USB 2.0 Camera 4K 8MP (RGB Video 3840x2160, 30 fps) (MCU IMX415) ($63)
# 5-50mm Lens
# https://a.aliexpress.com/_EutRLJ5

# https://www.youtube.com/watch?v=lM8DNAKpuBc
# https://youtrack.jetbrains.com/issue/IDEA-278224/Failed-to-start-powershell-cmd-on-windows
# https://stackoverflow.com/questions/19448078/python-opencv-access-webcam-maximum-resolution
# https://tproger.ru/translations/opencv-python-guide/#lines
# https://pythonpip.ru/opencv/funktsii-risovaniya-v-opencv
# https://gist.github.com/nochekaiser/ab4b3b8b8ceaad7db7c0c303b0ff661d

# Navigation:
# <Esc>                         - Exit Program
# <Mouse Double Left Click>     - Zoom x2
# <q>                           - Exit Zoom
# <p>                           - Add Red Center
# <o>                           - Add Green Circle
# <i>                           - Clear Center end Circle
# Monitor 1920x1080

import numpy as np
import cv2

p = 0
o = 0

def mousecall(event, x, y, flags, param):
    #if event == cv2.EVENT_LBUTTONUP: zoomin(x, y)
    if event == cv2.EVENT_LBUTTONDBLCLK: zoomin(x, y)
    if event == cv2.EVENT_RBUTTONDBLCLK: zoomout()

def mousenone(event, x, y, flags, param): return 0

def zoomin(x, y):
    cv2.setMouseCallback('frame', mousenone)

    while (True):
        ret, img = cap.read()
        x1 = x - 640
        if x1 < 0: x1 = 0
        x2 = x + 640
        if x2 > 2560: x2 = 2560
        y1 = y - 360
        if y1 < 0: y1 = 0
        y2 = y + 360
        if y2 > 1440: y2 = 1440

        pts1 = np.float32([[x1, y1], [x2, y1], [x1, y2], [x2, y2]])
        pts2 = np.float32([[0, 0], [1280, 0], [0, 720], [1280, 720]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, M, (1280, 720))
        cv2.imshow('frame', dst)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            zoomout()
            break

def zoomout():
    ret, img = cap.read()
    cv2.imshow('frame', img)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)     # 800 Not
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 576)     # 600 Not

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 1920, 1000)

while True:
    cv2.setMouseCallback('frame', mousecall)
    ret, frame = cap.read()

    if p == 1:
        cv2.line(frame, (1280, 730), (1280, 740), (0, 0, 255), 1)
        cv2.line(frame, (1280, 710), (1280, 700), (0, 0, 255), 1)
        cv2.line(frame, (1290, 720), (1300, 720), (0, 0, 255), 1)
        cv2.line(frame, (1270, 720), (1260, 720), (0, 0, 255), 1)

    if o == 1: cv2.circle(frame, (1280, 720), 40, (0, 255, 0), 1)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('p'): p = 1
    elif key & 0xFF == ord('o'): o = 1
    elif key & 0xFF == ord('i'): p = 0; o = 0
    elif key & 0xFF == 27: break

print('Resolution: '+str(frame.shape[1])+' x '+str(frame.shape[0]))
cap.release()
cv2.destroyAllWindows()
