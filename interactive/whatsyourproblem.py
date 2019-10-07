from threading import Lock, Thread
import atexit
from time import sleep

class CharGettor(Thread):
    '''
    On non-windows, we do not have `msvcrt.kbhit`.  
    Also, `getch` does not take `timeout` argument.  
    Hence, it is fundamentally impossible 
    to provide a seamless non-blocking interface for getch.  
    This class chooses to use a deamon thread.  
    Drawbacks:  
    * If the program exits while the thread is waiting for a char, 
        the user needs to press a key to let the deamon thread join.  
    * A `timeout` = 0 does not guarantee a read from the keyboard buffer.  
    * After a timeout, the user's next key press will be 
        "eaten" and saved to `char_got`, so `input()` will not 
        get it.  
    For a detailed demo of these drawbacks and their solutions,  
    see ./charGettor_demo.py
    On Windows, things work just fine, except we use repeated 
    polling of `msvcrt.kbhit`, `FPS` times per sec.  
    '''
    def __init__(self):
        super().__init__()
        self.consume = self.consumeNonWindows
        self.char_got = None
        self.consumeLock = Lock()
        self.produceLock = Lock()
        self.produceLock.acquire()
        self.go_on = True
        self.setDaemon(True)
        atexit.register(self.stop)
        self.start()

    def consumeNonWindows(self, timeout = -1, priorize_esc_or_arrow = True):
        '''
        `timeout`: 0 is nonblocking, -1 is wait forever.  
        Return None if timeout.  
        '''
        print('enter', timeout)
        if self.consumeLock.acquire(timeout = timeout):
            print('acquired')
            if self.char_got is not None:
                self.consumeLock.release()
                return self.popChar()
            else:
                self.priorize_esc_or_arrow = priorize_esc_or_arrow
                self.produceLock.release()
                return self.consume(timeout)
        else:
            print('acquire fail')
            return None
    
    def produce(self):
        self.produceLock.acquire()
        if self.go_on:
            sleep(2)
            self.consumeLock.release()

    def run(self):
        while self.go_on:
            self.produce()
    def stop(self):
        self.go_on = False
        self.produceLock.release()
        if self.consumeLock.locked():
            print(f'{self.__class__}: Program not terminating? '
              + 'Press a key. ')
        self.join()
    
    def popChar(self):
        try:
            return self.char_got
        finally:
            self.char_got = None
    def getFullCh(self):
        '''
        Returns bytes  
        Problem: 
            on Linux, function keys and arrow keys  
            scan code is multi bytes, starting with \x1b.  
            However, ESC scan code is single byte \x1b,  
            which means it is impossible to differentiate.  
            The caller of this function has to know in advance 
            whether the user is expected to press ESC or 
            arrow keys.  
            Set `priorize_esc_or_arrow` to True or False.  
        The parsing scheme of function keys is not researched.  
        Please open an issue if you have the docs of Linux scan codes.  
        '''
        ch = getch.getch()
        if ch == '\x1b':
            if not self.priorize_esc_or_arrow:
                new = getch.getch()
                ch += new
                if new in '[O': 
                    new = ''
                    while new in ';' + string.digits:
                        new = getch.getch()
                        ch += new
                    assert new in '~' + string.ascii_uppercase
                else:
                    pass    # alt + regular
        return ch.encode()

charGettor = CharGettor()
charGettor.consume(1)
