'''
Supports non-Windows. 
'''
''' I do not know why it is here. 
if 'flush' not in getargspec(print).args:
    print_3 = print
    def print(*args, flush = False, **kw):
        print_3(*args, **kw)
'''

try:
    import msvcrt
    from time import sleep
    
    def GetFullCh():
        first=msvcrt.getch()
        if first in (b'\x00', b'\xe0'):
            return first + msvcrt.getch()
        else:
            return first
    
    def listen(choice=None,timeout=0):
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
        print('',end='',flush=True)
        if timeout != 0:
            fps=30
            for i in range(int(timeout*fps)):
                if msvcrt.kbhit():
                    break
                sleep(1/fps)
            else:
                return None
        op=GetFullCh()
        while not (choice is None or op in bChoice):
            op=GetFullCh()
        return op

except ImportError:
    def listen(choice=None,timeout=0):
        print(choice)
        op = input()
        if '\\x' in op:
            return chr(int(op.split('\\x')[1], 16)).encode()
        else:
            return op.encode()

if __name__=='__main__':
    from console import console
    console({})
