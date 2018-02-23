'''
Like dummy.pool, but queuing is automated. 
'''
from threading import Thread, Lock

class LockableInt(int):
    def __init__(self, value = None):
        super(__class__,self).__init__()
        self.value = value

def autopool(list_input, function, list_output = None, thread_num = 4):
    enu_input = list(enumerate(list_input))
    list_thread = []
    wall = Lockable(-1)
    for i in range(min(thread_num, len(list_input))):
        list_thread.append(MyThread(enu_input.pop[0], function, wall))
    wall.acquire()
    while enu_input:
        with wall:
            print(1)
