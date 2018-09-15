'''
Record, play, save, and load macros. 
Windows only.
PROTECTION: global hooked button to stop macro = Windows Key 
'''
__all__ = ['record', 'play', 'save', 'load', 'MismatchError']
from console import console
from time import time, sleep
from ctypes import windll, Structure, c_long, byref
import win32api, win32con
import keyboard
from threading import Thread
from os import path, listdir
import pickle
import sys

DATA = path.join(path.dirname(__file__), 
                 'data_' + path.basename(__file__).rstrip('.py'))

def main():
    print(__all__)
    console(globals())

class POINT(Structure):
    _fields_ = [('x', c_long), ('y', c_long)]

def getPos():
    point = POINT()
    windll.user32.GetCursorPos(byref(point))
    return (point.x, point.y)

class Action:
    __slots__ = ['pos', 'delta_time', 'key']

    def __init__(self, pos, delta_time = 0, key = 'LEFT'):
        self.pos = pos
        self.delta_time = delta_time
        self.key = key
    
    def do(self):
        win32api.SetCursorPos(self.pos)
        key = self.key
        if key not in ('LEFT', 'RIGHT'):
            name = key.scan_code or key.name
            keyboard.press(name) if key.event_type == keyboard.KEY_DOWN else keyboard.release(name)
        else:
            win32api.mouse_event(win32con.__dict__ \
                ['MOUSEEVENTF_' + key + 'DOWN'], *self.pos, 0, 0)
            win32api.mouse_event(win32con.__dict__ \
                ['MOUSEEVENTF_' + key + 'UP'], *self.pos, 0 ,0)
    
    def __repr__(self):
        return str(self.pos) + ' ' + str(self.key)

class Sleep:
    __slots__ = ['delta_time']

    def __init__(self, delta_time):
        self.delta_time = delta_time
    
    def do():
        pass
    
    def __repr__(self):
        return 'Sleep(%f)' % self.delta_time

class MismatchError(BaseException):pass
def passKeyUp(keyDown):
    try:
        assert keyDown.event_type == 'down'
        keyUp = keyboard.read_event()
        assert keyUp.name == keyDown.name and keyUp.event_type == 'up'
        return keyUp
    except AssertionError:
        print('\nError: mismatch:', keyDown, 'and', keyUp)
        raise MismatchError

class Macro(list):
    def __init__(self):
        self.default_interval = .2
        self.deploy_delay = 2
    
    def play(self, n_times = 1):
        sleep(self.deploy_delay)
        failsafe = Failsafe()
        failsafe.start()
        try:
            for i in range(n_times):
                for action in self:
                    assert failsafe.green
                    if action.delta_time == 0:
                        sleep(self.default_interval)
                    else:
                        sleep(action.delta_time)
                    assert failsafe.green
                    action.do()
        except AssertionError:
            print('Macro is stopped! ')
            return
        n_wins = 0
        while failsafe.green:
            if n_wins > 5:
                print("Oh no! The failsafe won't join. ")
                print('Please help him by pressing Enter. ')
                failsafe.join()
            keyboard.press_and_release('win')
            sleep(self.default_interval)
            keyboard.press_and_release('win')
            n_wins += 1
            failsafe.join(self.default_interval)
        print('Macro successfully executed. ')
    
    def __repr__(self):
        return '\n'.join([str(x) for x in self] + 
            ['Tip: use record.last to access the last recording. '])

class Failsafe(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.green = True
    
    def run(self):
        try:
            keyboard.wait('win')
        except KeyError:
            print('(FYI, we got a key error from keyboard lib again. )')
        finally:
            self.green = False

def record():
    macro = Macro()
    try:
        while True:
            op = keyboard.read_event()
            if op.name == '\\':
                help = 'l : left click, r : right click, ' + \
                       '\\, t : sleep, esc'
                print(help, end = '\r', flush = True)
                opUp = passKeyUp(op)
                superKey = keyboard.read_event()
                print(' ' * len(help), end = '\r')
                passKeyUp(superKey)
                if superKey.name == 'l':
                    print('Left click')
                    macro.append(Action(getPos(), key = 'LEFT'))
                elif superKey.name == 'r':
                    print('Right click')
                    macro.append(Action(getPos(), key = 'RIGHT'))
                elif superKey.name == '\\':
                    print('\\')
                    macro.append(Action(getPos(), key = op))
                    macro.append(Action(getPos(), key = opUp))
                elif superKey.name == 't':
                    print('Sleep')
                    macro.append(Sleep(macro.default_interval))
                elif superKey.name == 'esc':
                    print('End')
                    try:
                        first = macro[0].key
                        if first.name == 'enter' and first.event_type == 'up':
                            macro.pop(0)
                    except IndexError:
                        pass
                    record.last = macro
                    return macro
                else:
                    print('Invalid super key. ', ' ' * 6)
            elif 'win' in op.name:
                print('Sorry, Windows key is reserved for Failsafe. ')
            else:
                if op.event_type == 'down':
                    print(op.name)
                macro.append(Action(getPos(), key = op))
    except MismatchError:
        return None

def play(macro):
    macro.play()

def save(macro):
    name = input('Give your macro a name: ')
    path_name = path.join(DATA, name)
    if path.isfile(path_name):
        print(name, 'already exists.')
        return
    with open(path_name, 'wb+') as f:
        pickle.dump(macro, f)
    print('Success. ')

def load():
    '''
    * to load all. 
    '''
    list_dir = listdir(DATA)
    print('Your macros: {')
    [print('   ', x) for x in list_dir]
    name = input('} which to load? ')
    if name == '*':
        result = {}
        for name in list_dir:
            with open(path.join(DATA, name), 'rb') as f:
                macro = pickle.load(f)
            result[name] = macro
    else:
        with open(path.join(DATA, name), 'rb') as f:
            result = pickle.load(f)
    load.last = result
    return result

if __name__ == '__main__':
    main()
    sys.exit(0)
