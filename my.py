'''
My misc little tools. 
'''
class LockableInt(int):
    def __init__(self, value = None):
        super(__class__,self).__init__()
        self.value = value

def autopool(list_input, function, list_output = None, thread_num = 4):
    '''
    Like dummy.pool, but queuing is automated. 
    '''
    from threading import Thread, Lock
    enu_input = list(enumerate(list_input))
    list_thread = []
    wall = Lockable(-1)
    for i in range(min(thread_num, len(list_input))):
        list_thread.append(MyThread(enu_input.pop[0], function, wall))
    wall.acquire()
    while enu_input:
        with wall:
            print(1)

def debug(func, *args, **kw):
    try:
        func(*args, **kw)
    except Exception:
        import traceback
        traceback.print_exc()
        input('Enter...')
