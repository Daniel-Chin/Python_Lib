'''
Playback a section of your screen.  
Useful for sharing PPT (with speaker notes on) over Tencent (VooV) Meeting.  
'''
import numpy as np
import cv2
from mss import mss

RECT = {
    'left': 585, 'top': 200, 
    'width': 1195, 'height': 675, 
}

try:
    with mss() as sct:
        while True:
            cv2.imshow(
                'screenCable', 
                np.array(sct.grab(RECT)), 
            )
            if cv2.waitKey(33) & 0xFF in (
                ord('q'), 
                27, 
            ):
                raise KeyboardInterrupt
except KeyboardInterrupt:
    print('exiting...')
finally:
    cv2.destroyAllWindows()
    print('ok')
