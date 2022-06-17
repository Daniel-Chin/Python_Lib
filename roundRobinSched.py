'''
Time-based round robin scheduling.  
'''
from typing import List, Callable
from time import perf_counter
import numpy as np

def roundRobinSched(tasks: List[Callable]):
    ages = np.zeros((len(tasks), ))
    while True:
        elected = ages.argmin()
        start = perf_counter()
        tasks[elected]()
        end   = perf_counter()
        ages[elected] += end - start

if __name__ == '__main__':
    from time import sleep
    from random import random
    tasks = []
    class Task:
        def __init__(self, t):
            self.t = t
        
        def __call__(self):
            sleep(self.t)
            print('slept for', self.t)
    for i in range(2):
        t = random() * .1
        tasks.append(Task(t))
    roundRobinSched(tasks)
