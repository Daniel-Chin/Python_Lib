'''
Terminal interactivity utils. 
'''
#===============================================================================
# I do not know why this was here. 
# if 'flush' not in getargspec(print).args:
#     print_3 = print
#     def print(*args, flush = False, **kw):
#         print_3(*args, **kw)
#===============================================================================
__all__ = ['listen', 'strCommonStart']
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
    # if sys.getwindowsversion() >= (10, 0, 17134) and False: # Strange windows update on 2018/10/22
    #     __getFullCh = getFullCh
    #     def getFullCh():
    #         ch = __getFullCh()
    #         if len(ch) == 1:
    #             assert msvcrt.getch() == b'\x00'
    #         return ch
except ImportError:
    msvcrt = None

def listen(choice=None, timeout=0):
    '''
    choice can be a list of choices or a single choice. 
    Elements can be b'' or ''.
    If timeout=0, it's blocking. 
    timeout is in second. 
    Supports non-windows. 
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
            op = eval('b"%s"' % input())
            if op == b'':
                return b'\r'    # So android doesn't need to type "\r"
        else:
            print(bChoice)
            op = None
            while op not in bChoice:
                op = eval('b"%s"' % input())
                if op == b'' and b'\r' in bChoice:
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

def strCommonStart(list_strs, known_len = 0):
    '''
    Find the common start for a list of strings. 
    Useful for auto-complete for the user. 
    `known_len` is known length of common start - for performance. 
    '''
    columns = zip(* list_strs)
    i = -1  # in case one string is ''
    for i, column in enumerate(columns):
        if i >= known_len:
            shifted_column = iter(column)
            next(shifted_column)
            if not all(x == y for x, y in zip(column, shifted_column)):
                i -= 1
                break
    return list_strs[0][:i + 1]

if __name__=='__main__':
    from console import console
    console(globals())
