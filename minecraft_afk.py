import mouse
from time import sleep

def main():
    print('When we start, you will have 5 seconds to switch to Minecraft.')
    input('Press Enter to start..')
    sleep(5)
    while True:
        sleep(1)
        mouse.click()

main()
