'''
Windows only. If not windows, start IPython. 
Advantage over IPython: 
    1. Lighter
    2. Other threads can still print things when user is inputting commands
Issue: 
    If you wanna scroll up, you need to input(). 
'''
import platform
from listen import listen
from kernal import Kernal

CURSOR = '|'

def console(namespace = {}, prompt = '>>> '):
    if platform.system() != 'Windows':
        from IPython import embed
        embed()
        return
    history = []
    kernal = Kernal(namespace)
    next(kernal)
    while True:
        cursor_bright = True
        command = ''
        cursor = 0
        history_selection = len(history)
        print(prompt + CURSOR, end='\r')
        while True:
            op = listen(timeout = .5)
            last_len = len(command)
            if op == b'\r':
                print(prompt + command.replace('\x1a', '^Z') + ' ')
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
                    word_started = False
                    for cursor in range(cursor - 1, -1, -1):
                        if command[cursor].isalpha():
                            word_started = True
                        else:
                            if word_started:
                                cursor += 1
                                break
                elif op == b'\xe0t': # Ctrl Right
                    word_started = False
                    word_ended = False
                    for cursor in range(cursor, len(command)):
                        if command[cursor].isalpha():
                            if word_ended:
                                break
                            else:
                                word_started = True
                        else:
                            if word_started:
                                word_ended = True
                    else:
                        cursor = len(command)
                elif op[0] in range(1, 26) or op[0] in (0, 224):
                    pass
                else:
                    command = command[:cursor] + op.decode() + command[cursor:]
                    cursor += 1
            padding = max(0, last_len - len(command)) * 2
            if cursor_bright:
                cursor_show = CURSOR
            else:
                cursor_show = '_'
            cursed_command = command[:cursor] + cursor_show + command[cursor:]
            print(prompt + cursed_command.replace('\x1a', '^Z') + ' '*padding, end='\r')
        if command in ('exit', 'exit()', '\x1a'):
            try:
                kernal.send('exit')
            except StopIteration:
                return
            assert False
        if command == '':
            continue
        history.append(command)
        kernal.send(command)

if __name__ == '__main__':
    console({})
