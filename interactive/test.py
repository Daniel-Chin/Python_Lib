import multiprocessing
from getch import getch
from time import sleep

class t(multiprocessing.Process):
    def run(self):
        getch()

print('start')
t().start()
print('Thread startd.')
sleep(1)
print('This wont print')
input('Enter...')
