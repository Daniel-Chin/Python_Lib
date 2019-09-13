'''
Windows only. If not windows, `console()` calls `IPython.embed()`. 
Usage: `console(globals())` or `console({**locals(), **globals()})`
Advantages over IPython:  
    1. Lighter  
    2. Other threads can still print things when user is inputting commands  
    3. Tab auto-completes your phrase, even under Windows! (I'm proud.)  
    4. Tired of having to `import` to test your module everytime you make an edit? `restart()` is what you need here.  
Issues:  
    1. Reassigning module global variables will not be visible to module native codes. Sorry.  
    2. For unknown reasons, you cannot declare any name present in kernal.py that is invisible to the env.  
    3. iniline generator cannot access namespace. I can't stably replicate this issue, and I don't know what this is about.  
Fixed Issues:  
    1. If you wanna scroll up, you don't need to input() anymore!  
    2. Multi-line code continuation is implemented!  
    3. If input command is longer than terminal width, camera rolls.  
Future:  
    1. Consider adding a dynamic `return` feature.  
    2. `traceback` is deleted every 
'''
import platform
from interactive import inputChin
from .kernal import Kernal
import random

def console(namespace = {}, prompt = '>>> ', use_input = False, fixer = None):
    if platform.system() != 'Windows':
        if namespace:
            for name in namespace:
                if not name.startswith('_') or name == '__file__':
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
            try:
                command = inputChin(prompt, '', history, kernal)
            except EOFError:
                command = 'exit()'
            if not command:
                continue
            stripped = command.strip()
            long_string = stripped.count("'''") % 2 == 1
            if long_string or stripped[:1] == '@' or stripped[-1:] in ':({[\\': 
                # `:1` so blank input doesnt trigger IndexError
                got = command
                while True:
                    history.append(got)
                    got = inputChin('... ', '', history, kernal)
                    command += '\n' + got
                    if long_string:
                        if got.count("'''") % 2 == 1:
                            break
                    else:
                        if not got:
                            break
        if fixer is not None:
            command = fixer(command)
        if command in ('exit', 'exit()'):
            try:
                kernal.send('exit')
            except StopIteration:
                return
            assert False
        if command == '':
            continue
        if command == '\x12':   #^R
            command = 'restart()'
        if command == 'help':
            print('Module `console`:')
            print(__doc__)
        history.append(command.split('\n')[-1])
        result = kernal.send(command)
        next(kernal)
        if result is not None:
            print(result)
