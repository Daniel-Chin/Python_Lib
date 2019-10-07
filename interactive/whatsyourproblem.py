from threading import Lock
lock = Lock()
def consumeNonWindows(timeout = -1, priorize_esc_or_arrow = True):
    '''
    `timeout`: 0 is nonblocking, -1 is wait forever.  
    Return None if timeout.  
    '''
    print('enter', timeout)
    if lock.acquire(timeout = timeout):
        print('acquired')
        if False:
            return 'yeah'
        else:
            
            return consumeNonWindows(timeout)
    else:
        print('acquire fail')
        return None

consumeNonWindows(1, True)
