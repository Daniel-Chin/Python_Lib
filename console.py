'''
Windows only. 
'''
from listen import listen as __listen
from os import system as cmd
__CURSOR = '|'

def console(globals, prompt = '>>> '):
    for name in globals:
        if name[0] != '_':
            exec(name + '=globals[\''+name+'\']')
    history = []
    while True:
        cursor_bright = True
        command = ''
        cursor = 0
        history_selection = len(history)
        print(prompt + __CURSOR, end='\r')
        while True:
            op = __listen(timeout = .5)
            last_len = len(command)
            if op == b'\r':
                print(prompt + command + ' ')
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
                    else:
                        history_selection +=1
                elif op == b'\xe0P':
                    history_selection += 1
                    if history_selection in range(len(history)):
                        command = history[history_selection]
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
                elif op[0] == 224:
                    pass
                else:
                    command = command[:cursor] + op.decode() + command[cursor:]
                    cursor += 1
            padding = max(0, last_len - len(command))
            if cursor_bright:
                cursor_show = __CURSOR
            else:
                cursor_show = '_'
            cursed_command = command[:cursor] + cursor_show + command[cursor:]
            print(prompt + cursed_command + ' '*padding, end='\r')
        if command in ('exit', 'exit()'):
            return
        if command == '':
            continue
        history.append(command)
        if command == 'cls':
            cmd('cls')
        else:
            try:
                try:
                    result = eval(command + '\r')
                    if result is not None:
                        print(result)
                except SyntaxError:
                    exec(command + '\r')
            except Exception as e:
                print(e)

if __name__ == '__main__':
    console({})
