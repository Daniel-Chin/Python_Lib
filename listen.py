'''
Supports non-Windows. 
'''
#===============================================================================
# I do not know why this is here. 
# if 'flush' not in getargspec(print).args:
#     print_3 = print
#     def print(*args, flush = False, **kw):
#         print_3(*args, **kw)
#===============================================================================

from time import sleep
FPS = 30

try:
    import msvcrt
    import sys
    def getFullCh():
        first=msvcrt.getch()
        if first in (b'\x00', b'\xe0'):
            return first + msvcrt.getch()
        else:
            return first
    if sys.getwindowsversion() >= (10, 0, 17134):
        __getFullCh = getFullCh
        def getFullCh():
            ch = __getFullCh()
            if len(ch) == 1:
                assert msvcrt.getch() == b'\x00'
            return ch

except ImportError:
    msvcrt = None

def listen(choice=None, timeout=0):
    '''
    choice can be a list of choices or a single choice. 
    Elements can be b'' or ''.
    If timeout=0, it's blocking. 
    timeout is in second. 
    '''
    if choice is not None:
        if type(choice) in (bytes, str):
            choice = (choice, )
        bChoice=[]
        for i in choice:
            if type(i) is bytes:
                bChoice.append(i)
            else:
                bChoice.append(i.encode())
    print('', end = '', flush = True)     # Just to flush
    if msvcrt is None:
        if choice is None:
            return eval('b"%s"' % input())
        else:
            print(bchoice)
            op = None
            while op not in bchoice:
                op = eval('b"%s"' % input())
                if op == b'' and b'\r' in bchoice:
                    return b'\r'    # So android doesn't need to type "\r"
            return op
    if timeout != 0:
        for i in range(int(timeout*FPS)):
            if msvcrt.kbhit():
                op = getFullCh()
                if choice is None or op in bChoice:
                    return op
            sleep(1/FPS)
        return None
    op=getFullCh()
    while not (choice is None or op in bChoice):
        op=getFullCh()
    return op

if __name__=='__main__':
    from console import console
    console({})
