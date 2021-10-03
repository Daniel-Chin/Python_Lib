import keyboard as kb
from time import time, sleep

is_q_down = False
is_v_down = False
def onKey(x):
    global is_q_down, is_v_down
    if x.name == '0' and x.event_type == 'down':
        if is_q_down:
            kb.release('q')
        else:
            kb.press('q')
        is_q_down = not is_q_down
    if x.name == 'q' and x.event_type == 'up':
        is_q_down = False
    if x.name == '=' and x.event_type == 'down':
        if is_v_down:
            kb.release('v')
        else:
            kb.press('v')
        is_v_down = not is_v_down
    if x.name == 'v' and x.event_type == 'up':
        is_v_down = False

kb.hook(onKey)
print('Good to go...')
try:
    while True:
        sleep(10)
except KeyboardInterrupt:
    print('bye')
finally:
    kb.unhook_all()
