'''
Command line Argument format: 
py -m book [FilePath] [Key] [Sync]
if Key = 'None', it's treated as not given. 
Sync should be 'sync' to take effect. 
'''
print('Importing...')
from beepher import Beepher
from io import BytesIO
from math import sqrt
import pickle
from os import system as cmd
from time import time
import lockfile
from listen import listen
from friendly_time import friendlyTime 
try:
    from sys import argv, exit as sys_exit
except:
    print('Import sys failed. ')
    argv=['']

print('Loading classes and functions...')

def CriticalError(msg):
    input(msg)
    sys_exit('Critical Error')

def LockFile(filename):
    lock=lockfile.FileLock(filename)
    try:
        lock.acquire(1)
        return lock
    except:
        CriticalError('Another Beepher book instance is operating on that file. \nEnter to quit...')

def loadfilename():
    if len(argv)>=2:
        return argv[1]
    else:
        op=input('Path/filename=').lower()
        if '.beeph' not in op:
            if input('Wanna add ".beeph"? Enter to do it, anything else to not. ')=='':
                op+='.beeph'
        return op

def load_book(filename, key):
    beepher=Beepher(open(filename,'rb'),key,'r')
    if beepher.read(1)==b'':
        # file is empty
        input('The file is empty. Enter to create an empty Beepher book. ')
        save_book({},filename,key,None)
        return {}
    beepher.seek(0)
    return pickle.load(beepher)

def loadkey():
    if len(argv)>=3 and argv[2].lower() != 'none':
        return argv[2]
    else:
        return Beepher.askForKey()

def cls():
    print('\n'*40,flush=True)
    cmd("cls")

def my_help():
    print("Command List: ")
    print("> new")
    print("> list")
    print("> del")
    print("> copy")
    print("> rename")
    print("> save")
    print("> cls")
    print("> silent_search")
    print("> search_by_content")
    print("> show")
    print("> edit")
    print("> append")
    print("> Nothing: Exit")
    print("> Anything else: Search")

class Entry:
    def __init__(self):
        self.time=0
        self.content=''

class ClsBook:
    def __init__(self,book={}):
        self.book=book

    def rename(self,entry):
        NewName=input('|: ')
        if NewName=='':
            return entry
        if NewName in self.book:
            print('Error: Entry',NewName,'already exists. ')
            return entry
        self.book[NewName]=self.book.pop(entry)
        return NewName

    def save(self,filename,key,lock):
        file=open(filename,'wb')
        beepher=Beepher(file,key,'w')
        pickle.dump(self.book,beepher)
        if lock is None:
            file.close()
        else:
            assert lock.is_locked
            lock.release()
            file.close()
            lock.acquire()
        print("Saved. ")

    def newentry(self):
        print("Entry name: ")
        entry=input("|: ")
        if entry in self.book:
            print("Error: Entry already exists. ")
            return None
        else:
            self.book[entry]=Entry()
            print("Content: ")
            content=input("")
            while content != "":
                self.book[entry].content+=content+chr(10)
                content=input("")
            cls()
            self.book[entry].time=time()
            print("Entry established. ")
            return entry

    def sort(self,SortBy):
        assert SortBy=='last modified'
        EntryID=list(self.book)
        entry=[]
        for i in EntryID:
            entry.append(self.book[i])
        for i in range(len(EntryID)-1,0,-1):
            for k in range(i):
                if entry[k].time<entry[k+1].time:
                    entry[k+1],entry[k]=entry[k],entry[k+1]
                    EntryID[k],EntryID[k+1]=EntryID[k+1],EntryID[k]
        return dict(zip(EntryID,entry))

    def list_entry(self,SortBy=None):
        if SortBy is None:
            SortedBook=self.book
        else:
            SortedBook=self.sort(SortBy)
        page_pos=0
        for entry in SortedBook:
            print(friendlyTime(self.book[entry].time),'|:',entry)
            page_pos+=1
            if page_pos==20:
                page_pos=0
                if input("Enter to show more... ")!="":
                    break

    def DelEntry(self,entry):
        print("Really delete:",entry,"?")
        print("Retype entry name to confirm deletion. ")
        if input("I delete: ")==entry:
            self.book.pop(entry)
            print("Entry",entry,"deleted! ")
            return True
        else:
            print("Did NOT delete. ")
            return False

    def copy_entry(self,entry):
        print("Copy to? ")
        new_entry=input("|: ")
        if new_entry == '':
            return entry
        if new_entry in self.book:
            print("Error: Entry already exists: ",new_entry)
            return False
        else:
            self.book[new_entry]=Entry()
            self.book[new_entry].time=self.book[entry].time
            self.book[new_entry].content=self.book[entry].content
            print("Copied",entry,"to",new_entry,". ")
            return True

    def search_by_content(self,keyword):
        matches=[]
        for entry in self.book:
            if keyword.lower() in self.book[entry].content.lower():
                matches.append(entry)
        return ChooseFromEntries(matches)

    def silent_search(self,keyword):
        matches = [x for x in self.book.keys() if keyword.lower() in x.lower()]
        return ChooseFromEntries(matches)

    def show_content(self,entry):
        print()
        print('|:',entry)
        print('last modified at',friendlyTime(self.book[entry].time))
        print(self.book[entry].content)

    def edit_entry(self,entry):
        print('Left arrow (\\xe0K) to modify current line. ')
        print('"i" to insert line before current line. ')
        print('Backspace (\\x08) to delete current line. ')
        print('Enter (\\r) to navigate to the next line. ')
        print()
        print('|:',entry)
        edited=""
        line=""
        for i in range(len(self.book[entry].content)):
            chara=self.book[entry].content[i]
            if chara!='\n':
                line+=chara
            else:
                print(line+"> ",end='',flush=True)
                op=listen((b'\xe0K',b'i',b'\x08',b'\r'))
                if op==b'\xe0K':
                    print('\r',' '*len(line),'\r',end='')
                    edited+=input()+chr(10)
                elif op==b'i':
                    print('\r',' '*len(line),'\r',end='')
                    content=input()
                    while content != "":
                        edited+=content+chr(10)
                        content=input("")
                    edited+=line+chr(10)
                    print(line)
                elif op==b'\x08':
                    print("\r---Line deleted---",' '*len(line))
                elif op==b'\r':
                    edited+=line+chr(10)
                    print()
                line=""
        cls()
        print("New version: ")
        print(edited)
        print('Save? \"y\" to save, \"n\" to discard. >')
        op=listen((b'y',b'n'))
        if op==b"y":
            self.book[entry].content=edited
            self.book[entry].time=time()
            cls()
            print("Entry edited. ")
            return True
        else:
            cls()
            print("Change discarded. ")
            return False

    def append_entry(self,entry):
        self.show_content(entry)
        print("Append: ")
        content=input()
        while content != "":
            self.book[entry].content+=content+'\n'
            content=input()
        cls()
        self.book[entry].time=time()
        print("Append success. ")

def ChooseFromEntries(matches):
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

def smart_entry_check(now_entry):
    if now_entry is None:
        print("No entry selected. ")
        return False
    else:
        return True

#Main
filename=loadfilename()
lock=LockFile(filename)
lock.release()
sync=False
if len(argv)>=4:
    if argv[3].lower()=='sync':
        sync=True
key=loadkey()
book=ClsBook(load_book(filename,key))
lock=LockFile(filename)
now_entry=None
print("Entry count: ",len(book.book))
stop=False
book_edited=False
BookEverEdited=False
while not stop:
    BookEverEdited=BookEverEdited or book_edited
    print()
    if smart_entry_check(now_entry):
        print("Now operating: ",now_entry)
    op=input(">> ")
    if op=="new":
        now_entry=book.newentry()
        book_edited=True
    elif op=="help":
        my_help()
    elif op=="list":
        print('Enter to list, "t" to list by time. >')
        if listen((b't',b'\r'))==b't':
            book.list_entry(SortBy='last modified')
        else:
            book.list_entry()
    elif op=="del":
        if smart_entry_check(now_entry):
            if book.DelEntry(now_entry):
                book_edited=True
                now_entry=None
    elif op=="copy":
        if smart_entry_check(now_entry):
            if book.copy_entry(now_entry):
                book_edited=True
    elif op=="rename":
        book_edited=True
        if smart_entry_check(now_entry):
            now_entry=book.rename(now_entry)
    elif op=="save":
        book_edited=False
        book.save(filename, key, lock)
    elif op=="cls":
        cls()
    elif op=="silent_search":
        now_entry=book.silent_search(input("Keyword: "))
    elif op=="search_by_content":
        now_entry=book.search_by_content(input("Keyword: "))
        if now_entry is not None:
            book.show_content(now_entry)
    elif op=="show":
        if smart_entry_check(now_entry):
            book.show_content(now_entry)
    elif op=="edit":
        if smart_entry_check(now_entry):
            if book.edit_entry(now_entry):
                book_edited =True
    elif op=="append":
        if smart_entry_check(now_entry):
            book_edited=True
            book.append_entry(now_entry)
    elif op=="":    #exit
        if book_edited:
            print("Type \"save\" to SAVE. ")
            print("Type \"discard\" to NOT save. ")
            op=input("I choose to ")
            if op=="save":
                book_edited=False
                book.save(filename, key, lock)
                input("Press Enter... ")
                stop=True
            elif op=="discard":
                print("It is NOT saved. ")
                input("Press Enter... ")
                stop=True
            else:
                print("Did not exit. ")
        else:
            stop=True
    else:
        now_entry=book.silent_search(op)
        if now_entry is not None:
            book.show_content(now_entry)
lock.release()
cls()
print("Beepher book ends. ")
if sync and BookEverEdited:
    cmd('git commit -a -m "Auto upload"')
    cmd('git push https://github.com/Daniel-Chin/Sync master')
sys_exit(0)
