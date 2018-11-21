'''
Windows only. If not windows, console() calls IPython.embed(). 
Advantages over IPython: 
    1. Lighter
    2. Other threads can still print things when user is inputting commands
    3. Tab auto-completes your phrase, even under Windows! (I'm proud.) 
Issues: 
    1. If you wanna scroll up, you need to input().
    2. Reassigning module global variables will not be visible to module native codes. Sorry. 
    3. No multi-line code continuation yet
'''
import platform
from interactive import listen, strCommonStart
from .kernal import Kernal
from graphic_terminal import clearLine
import string

CURSOR = '|'

def console(namespace = {}, prompt = '>>> ', use_input = False, fixer = None):
    if platform.system() != 'Windows':
        from IPython import embed
        embed()
        return
    print('console.console Warning: no support for reassigning module global variables. ')
    history = []
    kernal = Kernal(namespace)
    next(kernal)
    while True:
        cursor_bright = True
        command = ''
        cursor = 0
        history_selection = len(history)
        if use_input:
            try:
                command = input(prompt)
            except EOFError:
                command = 'exit()'
        else:
            print(prompt + CURSOR, end='\r')
            while True:
                op = listen(timeout = .5)
                last_len = len(command)
                if op == b'\r':
                    clearLine()
                    print(prompt + command.replace('\x1a', '^Z'))
                    break
                elif op is None:
                    cursor_bright = not cursor_bright
                else:
                    cursor_bright = True
                    if op == b'\x08':
                        if cursor >= 1:
                            command = command[:cursor - 1] + command[cursor:]
                            cursor -= 1
                    elif op == b'\xe0S':
                        if cursor <= len(command):
                            command = command[:cursor] + command[cursor + 1:]
                    elif op == b'\xe0H':
                        history_selection -= 1
                        if history_selection in range(len(history)):
                            command = history[history_selection]
                            cursor = len(command)
                        else:
                            history_selection +=1
                    elif op == b'\xe0P':
                        history_selection += 1
                        if history_selection in range(len(history)):
                            command = history[history_selection]
                            cursor = len(command)
                        else:
                            history_selection -=1
                    elif op == b'\xe0K':
                        cursor -= 1
                        if cursor not in range(len(command) + 1):
                            cursor += 1
                    elif op == b'\xe0M':
                        cursor += 1
                        if cursor not in range(len(command) + 1):
                            cursor -= 1
                    elif op == b'\xe0G':
                        cursor = 0
                    elif op == b'\xe0O':
                        cursor = len(command)
                    elif op == b'\xe0s': # Ctrl Left
                        cursor = wordStart(command, cursor)
                    elif op == b'\xe0t': # Ctrl Right
                        cursor = wordEnd(command, cursor)
                    elif op == b'\x7f':  # Ctrl Backspace
                        old_cursor = cursor
                        cursor = wordStart(command, cursor)
                        command = command[:cursor] + command[old_cursor:]
                    elif op == b'\xe0\x93': # Ctrl Del
                        old_cursor = cursor
                        cursor = wordEnd(command, cursor)
                        command = command[:old_cursor] + command[cursor:]
                        cursor = old_cursor
                    elif op == b'\t':
                        # auto complete
                        legal_prefix = string.ascii_letters + string.digits + '_'
                        reversed_names = []
                        name_end = cursor
                        name_start = cursor - 1
                        while True:
                            if name_start >= 0 and command[name_start] in legal_prefix:
                                name_start -= 1
                            else:
                                reversed_names.append(command[name_start + 1:name_end])
                                name_end = name_start
                                name_start -= 1
                                if name_start < 0 or command[name_end] != '.':
                                    break
                        keyword = reversed_names.pop(0)
                        names = reversed(reversed_names)
                        to_search = kernal.send('dir(%s)' % '.'.join(names))
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
                            command = command[:cursor] + to_insert + command[cursor:]
                            cursor += len(to_insert)
                    elif op[0] in range(1, 26) or op[0] in (0, 224):
                        pass
                    else:
                        command = command[:cursor] + op.decode() + command[cursor:]
                        cursor += 1
                if cursor_bright:
                    cursor_show = CURSOR
                else:
                    cursor_show = '_'
                cursed_command = command[:cursor] + cursor_show + command[cursor:]
                clearLine()
                print(prompt + cursed_command.replace('\x1a', '^Z'), end='\r')
        if fixer is not None:
            command = fixer(command)
        if command in ('exit', 'exit()', '\x1a'):
            try:
                kernal.send('exit')
            except StopIteration:
                return
            assert False
        if command == '':
            continue
        history.append(command)
        result = kernal.send(command)
        next(kernal)
        if result is not None:
            print(result)

def wordStart(command, cursor):
    word_started = False
    i = cursor
    for i in range(cursor - 1, -1, -1):
        if command[i].isalpha():
            word_started = True
        else:
            if word_started:
                i += 1
                break
    return i

def wordEnd(command, cursor):
    word_started = False
    word_ended = False
    i = cursor
    for i in range(cursor, len(command)):
        if command[i].isalpha():
            if word_ended:
                break
            else:
                word_started = True
        else:
            if word_started:
                word_ended = True
    else:
        i = len(command)
    return i
