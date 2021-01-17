'''
Profiles the computation time of a series of actions in a real-time stream-base application.  
Run the script to see a demo.  
'''

from time import time
from terminalsize import get_terminal_size

class StreamProfiler:
    def __init__(self, as_percentage_of = None, DO_PROFILE = True):
        self.as_percentage_of = as_percentage_of
        self.DO_PROFILE = DO_PROFILE

        self.tasks = {}
        self.now_task = None
        self.last_gonna = None
    
    def display(self, same_line = False):
        if not self.DO_PROFILE:
            return
        self.gonna('display')
        buffer = []
        for task_name, task_time in self.tasks.items():
            if self.as_percentage_of is not None:
                str_time = '{:4.0%}'.format(task_time / self.as_percentage_of)
            else:
                str_time = format(task_time * 1000, '3.0f') + ' ms'
            buffer.append(task_name + ' ' + str_time + '.')
        space = get_terminal_size()[0] - sum([len(x) for x in buffer]) - 2
        margin = space // (len(buffer) - 1)
        line = (' ' * margin).join(buffer)
        if same_line:
            print('', line, end = '\r', flush = True)
        else:
            print('', line)
        self.done()
        for i in self.tasks:
            if i != 'display':
                self.tasks[i] = 0
    
    def gonna(self, task_name):
        if not self.DO_PROFILE:
            return
        self.done()
        self.now_task = task_name
        self.last_gonna = time()
    
    def done(self):
        if not self.DO_PROFILE:
            return
        if self.now_task is not None:
            self.tasks[self.now_task] = time() - self.last_gonna
            self.now_task = None

if __name__ == '__main__':
    from time import sleep
    from random import random

    p = StreamProfiler(1)
    for _ in range(500):
        p.gonna('read')
        sleep(.001)

        p.gonna('trans')
        sleep(.03)

        p.gonna('pitch')
        sleep(.1 * random())

        p.display(False)
        p.gonna('idle')

        sleep(.9)   # Spurious. In reality, "idle" will be the time inbetween callbacks.  
