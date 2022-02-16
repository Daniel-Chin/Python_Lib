'''
Move cursor with Pro Controller.  
'''
# Borrowed code from https://stackoverflow.com/questions/66049843/i-am-trying-to-control-mouse-movement-with-an-xbox-controller-using-pygame
import pygame
import mouse

def main():
    pygame.init()
    x = 0; y = 0

    print('Controllers:')
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        j = pygame.joystick.Joystick(i)
        print(' ', j.get_name())
        j.init()
        joysticks.append(j)

    while True:
        for event in pygame.event.get():
            if event.type is pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    mouse.click()
            elif event.type == pygame.JOYAXISMOTION:
                print(event.axis, event.value)
                if event.axis == 4 or event.axis == 0:
                    if event.value > 0.25:
                        x += 25
                    elif event.value < - 0.25:
                        x -= 25
                if event.axis == 3 or event.axis == 1:
                    if event.value > 0.25:
                        y += 25
                    elif event.value < -0.25:
                        y -= 25
        mouse.move(x, y)

main()
