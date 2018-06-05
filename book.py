'''
sys.argv[1] in ('sun', 'pad') 
'''
print('Importing...')
import platform
from beepher import Beepher
from io import BytesIO
from math import sqrt
import pickle
from os import system, listdir
from time import time
from listen import listen
from friendly_time import friendlyTime 
import sys
if platform.system() == 'Linux':
    PATH = '/sdcard/Daniel/Beeph/'
else:
    PATH = ''

print('Loading classes and functions...')

def main():
    print('MAIN')
    filename = loadFilename()
    key = input('? ')
    cls()
    book = Book(filename, key)
    try:
        book._mainloop()
    except EOFError:
        pass
    finally:
        if book.unsaved_change:
            print('Type "save" to SAVE. ')
            print('Type "discard" to NOT save. ')
            op = ''
            while op not in ('save', 'discard'):
                op = input('I choose to ')
            if op == 'save':
                book.save()
                input('Press Enter... ')
            elif op == 'discard':
                print('It is NOT saved. ')
                input('Press Enter... ')
    cls()
    print('Beepher book ends. ')

def loadFilename():
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        print()
        if platform.system() == 'Linux':
            list_dir = [x.lower() for x in listdir(PATH)]
            [print(name) for name in list_dir]
            filename = input('filename=').lower()
            if filename not in list_dir:
                filename += '.beeph'
                assert filename in list_dir, 'No such file. '
            return PATH + filename
        else:
            return input('path\\filename.beeph: ')

if platform.system() == 'Windows':
    def cls():
        system('cls')
else:
    def cls():
        system('clear')

class Entry:
    def __init__(self):
        self.time = 0
        self.content = ''
    
    def copy(self):
        entry = Entry()
        entry.time = self.time
        entry.content = self.content
        return entry

class Book:
    '''
    All public methods can be called by user thru input(). 
    '''
    def __init__(self, filename, key):
        self.unsaved_change = False
        self.now = None
        self.filename = filename
        self.key = key
        beepher = Beepher(open(filename,'rb'), key, 'r')
        if beepher.read(1) == b'':
            # file is empty
            input('The file is empty. Enter to create an empty Beepher book. ')
            self.dict = {}
        else:
            beepher.seek(0)
            self.dict = pickle.load(beepher)
            print('Entry count:', len(self.dict))
    
    def _mainloop(self):
        while True:
            print()
            if self._smartEntryCheck():
                print('Now operating:', self.now)
            op = input(">> ")
            methods = self.help(do_print = False)
            name = op.split(' ')[0]
            try:
                method = methods[name]
                try:
                    method(*op.split(' ')[1:])
                except TypeError:
                    help(method)
                    print('Oops. You gave wrong params. ')
                continue
            except KeyError:
                pass
            if op == '':
                cls()
            elif op == 'exit':
                break
            else:
                self.silentSearch(op)
                if self.now is not None:
                    self.show()
    
    def help(self, do_print = True):
        methods = {}
        for name in dir(self):
            attr = getattr(self, name)
            if name[0] != '_' and callable(attr):
                methods[name] = attr
        if do_print:
            print('Commands: ')
            [print('>', name) for name in methods]
        return methods
    
    def cls(self):
        cls()
    
    def _smartEntryCheck(self):
        if self.now is None:
            print("No entry selected. ")
            return False
        else:
            return True
    
    def new(self, entry_name = None):
        if entry_name is None:
            print('Entry name: ')
            entry_name = input('|: ')
        if self.__isValidEntryName(entry_name):
            self.dict[entry_name] = Entry()
            print('Content: ')
            self.dict[entry_name].content = multilineInput()
            cls()
            self.dict[entry_name].time = time()
            self.now = entry_name
            print('Entry established. ')
            self.unsaved_change = True
    
    def __isValidEntryName(self, entry_name):
        if entry_name == '':
            msg = 'Error: Entry name cannot be blank. '
        elif entry_name in self.dict:
            msg = 'Error: Entry ' + entry_name + ' already exists. '
        elif entry_name in self.help(do_print = False):
            msg = 'Error: Reserved keyword: ' + entry_name
        else:
            return True
        print(msg)
        return False
    
    def show(self):
        if self._smartEntryCheck():
            print()
            print('|:', self.now)
            print('last modified at', friendlyTime(
                self.dict[self.now].time))
            print(self.dict[self.now].content)
    
    def list(self):
        print('Enter to list by name, "t" to list by time. >')
        if listen((b't', b'\r')) == b't':
            sortedDict = self.__sort('last modified')
        else:
            sortedDict = self.dict
        page_pos=0
        for key, entry in sortedDict.items():
            print(friendlyTime(entry.time), '|:', key)
            page_pos += 1
            if page_pos == 20:
                page_pos = 0
                if input('Enter to show more... ') != '':
                    break
    
    def __sort(self, sort_by):
        assert sort_by == 'last modified'
        keys = list(self.dict)
        entrys = []
        for i in keys:
            entrys.append(self.dict[i])
        for i in range(len(keys)-1, 0, -1):
            for k in range(i):
                if entrys[k].time < entrys[k+1].time:
                    entrys[k+1],entrys[k] = entrys[k],entrys[k+1]
                    keys[k],keys[k+1] = keys[k+1],keys[k]
        return dict(zip(keys, entrys))
    
    def silentSearch(self, keyword = None):
        if keyword is None:
            keyword = input('Keyword: ')
        matches = [x for x in self.dict.keys() if keyword.lower() in x.lower()]
        self.now = chooseFromEntries(matches)
    
    def save(self):
        file = open(self.filename, 'wb')
        beepher = nb(file, self.key, 'w')
        pickle.dump(self.dict, beepher)
        file.close()
        self.unsaved_change = False
        print('Saved. ')
    
    def rename(self, new_name = None):
        if self._smartEntryCheck():
            if new_name is None:
                new_name = input('|: ')
            if self.__isValidEntryName(new_name):
                self.dict[new_name] = self.dict.pop(self.now)
                self.now = new_name
                self.unsaved_change = True
    
    def delete(self):
        if self._smartEntryCheck():
            print('Really delete:', self.now, '?')
            print('Type entry name to confirm deletion. ')
            if input('I delete: ') == self.now:
                self.dict.pop(self.now)
                print('Entry', self.now, 'deleted! ')
                self.now = None
                self.unsaved_change = True
            else:
                print('Did NOT delete. ')
    
    def copy(self, new_entry_name = None):
        if self._smartEntryCheck():
            print('Copy to? ')
            if new_entry_name is None:
                new_entry_name = input('|: ')
            if not self.__isValidEntryName(new_entry_name):
                print('Did not copy. ')
            else:
                self.dict[new_entry_name] = self.dict[self.now].copy()
                print('Copied', self.now, 'to', new_entry_name, '. ')
                self.unsaved_change=True
    
    def searchByContent(self, keyword = None):
        if keyword is None:
            keyword = input('keyword: ')
        matches = []
        for name, entry in self.dict.items():
            if keyword.lower() in entry.content.lower():
                matches.append(name)
        self.now = chooseFromEntries(matches)
        if self.now is not None:
            self.show()
    
    def edit(self):
        if self._smartEntryCheck():
            print('Left arrow (\\xe0K) to modify current line. ')
            print('"i" to insert line before current line. ')
            print('Backspace (\\x08) to delete current line. ')
            print('Enter (\\r) to navigate to the next line. ')
            print()
            print('|:', self.now)
            edited = []
            for line in self.dict[self.now].content.split('\n'):
                print(line + "> ", end='', flush=True)
                op = listen((b'\xe0K',b'i',b'\x08',b'\r'))
                if op == b'\xe0K':
                    print('\r', ' '*len(line), '\r', end='', flush = True)
                    edited.append(input())
                elif op == b'i':
                    print('\r', ' '*len(line), '\r', end='')
                    edited.append(multilineInput())
                    edited.append(line)
                    print(line)
                elif op==b'\x08':
                    print("\r---Line deleted---", ' '*len(line))
                elif op==b'\r':
                    edited.append(line)
                    print()
            cls()
            edited = '\n'.join(edited)
            print('Old version: ')
            print(self.dict[self.now])
            print()
            print('New version: ')
            print(edited)
            print('Save? "y" to save, "n" to discard. >', end = '', flush = True)
            op = listen((b'y', b'n'))
            if op == b'y':
                self.dict[self.now].content = edited
                self.dict[self.now].time = time()
                cls()
                print('Entry edited. ')
                self.unsaved_change = True
            else:
                cls()
                print('Change discarded. ')
    
    def append(self):
        if self._smartEntryCheck():
            self.show()
            print('Append: ')
            to_append = multilineInput()
            cls()
            self.dict[self.now].content += '\n' + to_append
            self.dict[self.now].time = time()
            self.unsaved_change = True
            print('Append success. ')

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
            print(no,": ",i)
            no+=1
        print("Type entry ID to select. Enter to abort search. ")
        try:
            return matches[int(input("Entry ID: "))]
        except:
            print("Search aborted. ")
            return None

def multilineInput():
    buffer = []
    content = input()
    while content != '':
        buffer.append(content)
        content = input()
    return '\n'.join(buffer)

if __name__ == '__main__':
    main()
    sys.exit(0)
