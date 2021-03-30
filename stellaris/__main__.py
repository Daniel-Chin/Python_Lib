'''
Stellaris game assistant.  
Assignes hotkey to planet prev/next button.  
'''

DEFAULT_POS = [750, 100]
BUTTON_DISTANCE = 35

import mouse
import keyboard
from time import sleep

pos = DEFAULT_POS[:]

def main():
    keyboard.add_hotkey('p', clickPrev)
    keyboard.add_hotkey('[', clickNext)
    keyboard.add_hotkey('shift+p', setPrev)
    print('go...')
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print('Ctrl+C received. Quiting...')
    finally:
        keyboard.unregister_all_hotkeys()
        print('All resources released. ')

def clickPrev():
    print('prev')
    mouse.move(*pos)
    sleep(.1)
    mouse.click()

def clickNext():
    print('prev')
    mouse.move(pos[0] + BUTTON_DISTANCE, pos[1])
    sleep(.1)
    mouse.click()

def setPrev():
    x, y = mouse.get_position()
    pos[0] = x
    pos[1] = y
    print(x, y)

main()
