'''
Windows only. If not windows, `console()` calls `IPython.embed()`. 
Advantages over IPython:  
    1. Lighter  
    2. Other threads can still print things when user is inputting commands  
    3. Tab auto-completes your phrase, even under Windows! (I'm proud.)  
Issues:  
    1. Reassigning module global variables will not be visible to module native codes. Sorry.  
Fexed Issues:  
    1. If you wanna scroll up, you don't need to input() anymore!  
    2. Multi-line code continuation is implemented!  
'''
import platform
from interactive import inputChin
from .kernal import Kernal
import random

def console(namespace = {}, prompt = '>>> ', use_input = False, fixer = None):
    if platform.system() != 'Windows':
        if namespace:
            for name in namespace:
                if not name.startswith('_'):
                    exec(f'{name}=namespace["{name}"]')
            del name
        del namespace
        from IPython import embed
        embed()
        return
    if random.randint(0, 5) == 0:
        print('console.console Warning: no support for reassigning module global variables. ')
    else:
        print('No global. ')
    history = []
    kernal = Kernal(namespace)
    next(kernal)
    while True:
        if use_input:
            try:
                command = input(prompt)
            except EOFError:
                command = 'exit()'
        else:
            command = inputChin(prompt, '', history, kernal)
            if command[-1] == ':':
                got = command
                while got != '':
                    history += got
                    got = inputChin('... ', '', history, kernal)
                    command += '\n' + got
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
        history.append(command.split('\n')[-1])
        result = kernal.send(command)
        next(kernal)
        if result is not None:
            print(result)
