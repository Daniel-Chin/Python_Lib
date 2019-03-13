'''
Terminal interactivity utils. 

One vulnerability in `listen`. Do help(listen) for details. 
'''
__all__ = ['listen', 'strCommonStart', 'AbortionError', 
    'cls', 'askForFile', 'askSaveWhere', 'inputChin', 'multiLineInput']
from time import sleep
from .console_explorer import *
from .cls import cls
from colorama import init, Back, Fore, Style
init()
from terminalsize import get_terminal_size
from graphic_terminal import *
import string

FPS = 30
CURSOR_WRAP = Back.GREEN + Fore.WHITE + '%s' + Style.RESET_ALL

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

def listen(choice = [], timeout = 0):
    '''
    Vulnerability Warning: 
        This function calls `evel`. User can eval any element repr in bChoice. 
        If you supply this function with normal arguments, you should be safe. 
        Don't let the `choice` argument depend on previous user input! 
    choice can be an iterable of choices or a single choice. 
    Elements can be b'' or ''.
    If timeout=0, it's blocking. 
    timeout is in second. 
    Supports non-windows. 
    '''
    try:
        bChoice = list(x.encode() for x in choice)
    except AttributeError:
        bChoice = list(choice)
    print('', end = '', flush = True)     # Just to flush
    if msvcrt is None:
        if bChoice == []:
            op = input()
            if op == '':
                return b'\r'    # So android doesn't need to type "\r"
        else:
            print(bChoice)
            repr_bChoice = [str(x) for x in bChoice]
            op = None
            while op not in repr_bChoice:
                print("b'    '\rb'", end = '', flush = True)
                op = "b'%s'" % input()
                if op == "b''" and b'\r' in bChoice:
                    return b'\r'    # So android doesn't need to type "\r"
            return eval(op)
    if timeout != 0:
        try:
            for i in range(int(timeout * FPS)):
                if msvcrt.kbhit():
                    op = getFullCh()
                    if bChoice == [] or op in bChoice:
                        return op
                sleep(1/FPS)
            return None
        except KeyboardInterrupt:
            return b'\x03'  # ^C. For consistency when calling listen(timeout=0) and ^C. 
    op = getFullCh()
    while not (bChoice == [] or op in bChoice):
        op = getFullCh()
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
    print(prompt, line.replace('\x1a', '^Z').replace('\x12', '^R'), end = '\r', flush = True, sep = '')

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
        if op == b'\r':
            clearLine()
            print(prompt + line.replace('\x1a', '^Z').replace('\x12', '^R'))
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
            line = line[:cursor] + op.decode() + line[cursor:]
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
