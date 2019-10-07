'''
Terminal interactivity utils. 
'''
__all__ = ['listen', 'strCommonStart', 'AbortionError', 
    'cls', 'askForFile', 'askSaveWhere', 'inputChin', 'multiLineInput', 
    'inputUntilValid', 
]

from .console_explorer import *
from .cls import cls
from colorama import init, Back, Fore, Style
init()
from terminalsize import get_terminal_size
from graphic_terminal import *
import string
from threading import Thread, Lock, Condition
from time import monotonic as monoTime, sleep
import atexit
from sys import stdout
try:
    import msvcrt
    is_windows = True
except ImportError:
    import getch
    is_windows = False

FPS = 30
CURSOR_WRAP = Back.GREEN + Fore.WHITE + '%s' + Style.RESET_ALL

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
        if is_windows:
            self.consume = self.consumeWindows
        else:
            self.consume = self.consumeNonWindows
            self.char_got = None
            self.consumeLock = Lock()
            self.produceLock = Lock()
            self.produceLock.acquire()
            self.go_on = True
            self.setDaemon(True)
            atexit.register(self.stop)
            self.start()

    def consumeWindows(self, timeout = -1):
        '''
        `timeout`: 0 is nonblocking, -1 is wait forever.  
        Return None if timeout.  
        '''
        if timeout == -1:
            return self.getFullCh()
        if timeout < 0:
            raise ValueError(f'timeout must > 0, got {timeout}')
        try:
            for i in range(timeout * FPS + 1):
                if msvcrt.kbhit():
                    return self.getFullCh()
                sleep(1 / FPS)
        except KeyboardInterrupt:
            # If ^C arrives when we sleep
            return b'\x03'  # Just for consistency. See ./charGettor_demo.py
        return None
    
    def consumeNonWindows(self, timeout = -1, priorize_esc_or_arrow = True):
        '''
        `timeout`: 0 is nonblocking, -1 is wait forever.  
        Return None if timeout.  
        '''
        if self.consumeLock.acquire(timeout = timeout):
            if self.char_got is not None:
                self.consumeLock.release()
                return self.popChar()
            else:
                self.priorize_esc_or_arrow = priorize_esc_or_arrow
                self.produceLock.release()
                return self.consume(timeout)
        else:
            return None
    
    def produce(self):
        self.produceLock.acquire()
        if self.go_on:
            self.ch_got = self.getFullCh()
            self.consumeLock.release()
    
    def popChar(self):
        try:
            return self.char_got
        finally:
            self.char_got = None
    
    if is_windows:
        def getFullCh(self):
            '''
            Returns bytes  
            '''
            first = msvcrt.getch()
            if first[0] in range(1, 128):
                full_ch = first
            else:   # \x00 \xe0 multi bytes scan code
                full_ch = first + msvcrt.getch()
            return full_ch
    else:
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
            print('first', ch)
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

class Universe:
    def __contains__(self, x):
        return True

def listen(choice = {}, timeout = -1):
    '''
    `choice`:  
        can be an iterable of choices or a single choice.   
        Elements can be byte or string.  
        If empty, accepts anything.  
    `timeout`:  
        in seconds. -1 is blocking. 
    Supports non-windows.  
    The function returns None if timeout.  
    Problems:  
        *There are several problems with this function that 
        you need to know about!*  
        Please see `help(CharGettor)`.  
    '''
    if choice:
        bChoice = set()
        for option in choice:
            if type(option) is str:
                option = option.encode()
            elif type(option) is int:
                option = bytes([option])
            if type(option) is not bytes:
                raise TypeError('`choice` argument type mismatch')
            bChoice.add(option)
    else:
        bChoice = Universe()
    
    stdout.flush()
    
    if timeout != -1:
        deadline = monoTime() + timeout
    while True:
        op = charGettor.consume(-1 if timeout == -1 else deadline - monoTime())
        if op and op in bChoice:
            return op
        if timeout != -1 and monoTime() > deadline:
            return None

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

def chooseFromEntries(matches):
    input('Warning: interactive/__init__/chooseFromEntries will be deprecated!!! Enter...')
    if len(matches)==1:
        return matches[0]
    elif matches==[]:
        print("No match. ")
        return None
    else:
        print("Multiple matches: ")
        no=0
        for i in matches:
            print(no,": ",i.name)
            no+=1
        print("Type entry ID to select. Enter to abort search. ")
        try:
            return matches[int(input("Entry ID: "))]
        except:
            print("Search aborted. ")
            return None

def printabilize(x):
    return x.replace('\x1a', '^Z').replace('\x12', '^R')

_abbr = '...'
ABBR = [*'...']
ABBR[0] = Back.MAGENTA + Fore.WHITE + ABBR[0]
ABBR[-1] += Style.RESET_ALL
ABBR_LEN = len(_abbr) + 1
def printWithCursor(prompt, line, cursor):
    if cursor == len(line):
        line += ' '
    chars, [cursor] = eastAsianStrSparse(line, [cursor])
    chars[cursor] = CURSOR_WRAP % chars[cursor]
    width = get_terminal_size()[0] - eastAsianStrLen(prompt) - 1
    offset = min(cursor - width // 2, len(chars) - width)
    if offset > 0:
        chars = chars[offset + ABBR_LEN:]
        if chars[0] == '':
            chars.pop(0)
        chars = ABBR + [' '] + chars
    offset = len(chars) - width
    if offset > 0:
        if chars[-offset] == '':
            offset += 1
        chars = chars[:-offset - ABBR_LEN]
        chars += [' '] + ABBR
    line = ''.join(chars)
    print(prompt, printabilize(line), end = '\r', flush = True, sep = '')

def inputChin(prompt = '', default = '', history = [], kernal = None, cursor = None):
    '''
    `kernal` for tab key auto complete. 
    '''
    default = str(default)
    line = default
    if cursor is None:
        cursor = len(line)
    history_selection = len(history)
    while True:
        printWithCursor(prompt, line, cursor)
        op = listen()
        last_len = len(line)
        if op in b'\r\n':
            clearLine()
            print(prompt + printabilize(line))
            if '\x1a' in line:  # ^Z
                raise EOFError(f'"{printabilize(line)}"')
            return line
        elif op == b'\x08': # backspace
            if cursor >= 1:
                line = line[:cursor - 1] + line[cursor:]
                cursor -= 1
        elif op == b'\xe0S':    # del
            if cursor <= len(line):
                line = line[:cursor] + line[cursor + 1:]
        elif op == b'\xe0H':    # up
            history_selection -= 1
            if history_selection in range(len(history)):
                line = history[history_selection]
                cursor = len(line)
            else:
                history_selection += 1
        elif op == b'\xe0P':    # down
            history_selection += 1
            if history_selection in range(len(history)):
                line = history[history_selection]
                cursor = len(line)
            else:
                history_selection -= 1
        elif op == b'\xe0K':    # left
            cursor -= 1
            if cursor not in range(len(line) + 1):
                cursor += 1
        elif op == b'\xe0M':    # right
            cursor += 1
            if cursor not in range(len(line) + 1):
                cursor -= 1
        elif op == b'\xe0G':    # home
            cursor = 0
        elif op == b'\xe0O':    # end
            cursor = len(line)
        elif op == b'\xe0s': # Ctrl Left
            cursor = wordStart(line, cursor)
        elif op == b'\xe0t': # Ctrl Right
            cursor = wordEnd(line, cursor)
        elif op == b'\x7f':  # Ctrl Backspace
            old_cursor = cursor
            cursor = wordStart(line, cursor)
            line = line[:cursor] + line[old_cursor:]
        elif op == b'\xe0\x93': # Ctrl Del
            old_cursor = cursor
            cursor = wordEnd(line, cursor)
            line = line[:old_cursor] + line[cursor:]
            cursor = old_cursor
        elif op == b'\t':
            # auto complete
            if kernal is not None:
                legal_prefix = string.ascii_letters + string.digits + '_'
                reversed_names = []
                name_end = cursor
                name_start = cursor - 1
                while True:
                    if name_start >= 0 and line[name_start] in legal_prefix:
                        name_start -= 1
                    else:
                        reversed_names.append(line[name_start + 1:name_end])
                        name_end = name_start
                        name_start -= 1
                        if name_start < 0 or line[name_end] != '.':
                            break
                keyword = reversed_names.pop(0)
                names = reversed(reversed_names)
                to_search = kernal.send('dir(%s)' % '.'.join(names)) or []
                if len(reversed_names) == 0:
                    # include builtins
                    to_search += dir(__builtins__)
                next(kernal)
                candidates = [x for x in to_search if x.startswith(keyword)]
                if len(candidates) >= 1:
                    if len(candidates) == 1:
                        to_become = candidates[0]
                    if len(candidates) > 1:
                        clearLine()
                        print('auto-complete: ', end = '')
                        [print(x, end = '\t') for x in candidates]
                        print()
                        to_become = strCommonStart(candidates, len(keyword))
                    to_insert = to_become[len(keyword):]
                    line = line[:cursor] + to_insert + line[cursor:]
                    cursor += len(to_insert)
        elif op == b'\x1b':  # ESC
            line = ''
            cursor = 0
        elif op[0] in range(1, 18) or op[0] in range(19, 26) or op[0] in (0, 224):
            pass    # invalid char
        else:   # typed char
            line = line[:cursor] + op.decode('ANSI') + line[cursor:]
            cursor += 1
        clearLine()

def wordStart(line, cursor):
    word_started = False
    i = cursor
    for i in range(cursor - 1, -1, -1):
        if line[i].isalpha():
            word_started = True
        else:
            if word_started:
                i += 1
                break
    return i

def wordEnd(line, cursor):
    word_started = False
    word_ended = False
    i = cursor
    for i in range(cursor, len(line)):
        if line[i].isalpha():
            if word_ended:
                break
            else:
                word_started = True
        else:
            if word_started:
                word_ended = True
    else:
        i = len(line)
    return i

def multiLineInput(toIO = None):
    if toIO is None:
        buffer = []
        def append(s):
            buffer.append(s)
    else:
        def append(s):
            toIO.write(s)
            toIO.write('\n')
    try:
        while True:
            append(input())
    except EOFError:
        if toIO is None:
            return '\n'.join(buffer)
        else:
            return toIO

def inputUntilValid(prompt, validator, case_sensitive = False, legalize = None):
    '''
    `validator` can be a function returning boolean, or an iter.  
    '''
    try:
        if not case_sensitive:
            validator = [x.lower() for x in validator]
        else:
            validator = {*validator}
        is_iter = True
        prompt += ' ' + '/'.join(validator) + ' > '
    except TypeError:
        is_iter = False
    while True:
        candidate = input(prompt)
        if not case_sensitive:
            candidate = candidate.lower()
        if legalize is not None:
            try:
                candidate = legalize(candidate)
            except:
                continue
        if (is_iter and candidate in validator) or (not is_iter and validator(candidate)):
            return candidate

charGettor = CharGettor()
