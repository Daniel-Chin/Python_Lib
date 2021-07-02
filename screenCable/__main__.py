'''
Playback a section of your screen.  
Useful for sharing PPT (with speaker notes on) over Tencent (VooV) Meeting.  
Hit `ESC` or `q` to quit.  
Hit `Spacebar` to refresh view.  
Click and drag to resize the window.  
'''
WINDOW = 'screenCable'

import numpy as np
import cv2
from mss import mss
from time import sleep

def mouseEvent(event, x, y, flags, param):
    if flags == cv2.EVENT_FLAG_LBUTTON:
        rect['width'] = x
        rect['height'] = y

rect = {
    'left': 585, 'top': 200, 
    'width': 1195, 'height': 675, 
}
just_refreshed = False
try:
    cv2.namedWindow(WINDOW)
    cv2.setMouseCallback(WINDOW, mouseEvent)
    cv2.moveWindow(WINDOW, rect['left'], rect['top'])
    with mss() as sct:
        while True:
            cv2.imshow(
                WINDOW, 
                np.array(sct.grab(rect)), 
            )
            rect['left'], rect[
                'top'
            ], _, __ = cv2.getWindowImageRect(WINDOW)
            key_press = cv2.waitKey(
                200 if just_refreshed else 33
            ) & 0xFF
            if key_press in (
                ord('q'), 
                27, 
            ):
                raise KeyboardInterrupt
            elif key_press == ord(' '):
                cv2.destroyWindow(WINDOW)
                sleep(.2)
                just_refreshed = True
except KeyboardInterrupt:
    print('exiting...')
finally:
    cv2.destroyAllWindows()
    print('ok')
