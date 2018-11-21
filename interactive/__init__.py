'''
Terminal interactivity utils. 

One vulnerability in `listen`. Do help(listen) for details. 
'''
#===============================================================================
# I do not know why this was here. 
# if 'flush' not in getargspec(print).args:
#     print_3 = print
#     def print(*args, flush = False, **kw):
#         print_3(*args, **kw)
#===============================================================================
__all__ = ['listen', 'strCommonStart', 'AbortionError', 'cls', 'askForFile', 'askSaveWhere']
from time import sleep
from .console_explorer import *
from .cls import cls

FPS = 30

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
        for i in range(int(timeout * FPS)):
            if msvcrt.kbhit():
                op = getFullCh()
                if bChoice == [] or op in bChoice:
                    return op
            sleep(1/FPS)
        return None
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
