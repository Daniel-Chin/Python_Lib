from threading import Thread
from getch import getch
from time import sleep

class t(Thread):
    def run(self):
        getch()

print('start')
t().start()
print('Thread startd.')
sleep(1)
print('This wont print')
input('Enter...')
