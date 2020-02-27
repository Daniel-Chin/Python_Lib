'''
AFK tool for Minecraft.  
'''
import mouse
from time import sleep

def main():
    print('When we start, you will have 5 seconds to switch to Minecraft.')
    input('Press Enter to start..')
    print('Press Ctrl+C to stop.')
    sleep(5)
    print('Clicking...')
    while True:
        sleep(5)
        mouse.click()

main()
