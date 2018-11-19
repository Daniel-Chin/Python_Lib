'''
Unreliable file utils
'''
import os
from os import path
from listen import listen

def copy():
    '''
    Copies only binary content, leaving meta data. 
    '''
    src_name = input('from: ')
    dest_name = input('to: ')
    if path.isfile(dest_name):
        print('Destination file alreay exists. Overwrite? Y/N')
        if listen([b'y', b'n']) != b'y':
            print('Aborted. ')
            return
    with open(src_name, 'rb') as src:
        with open(dest_name, 'wb+') as dest:
            dest.write(src.read())
    print('Done! ')

def delete():
    '''
    Fill file with zeros and delete. 
    '''
    filename = input('file: ')
    if not path.isfile(filename):
        print("Doesn't exist. ")
        return
    size = os.stat(filename).st_size
    with open(filename, 'wb') as f:
        f.write(bytearray(size))
    os.remove(filename)
    print('Done! ')

if __name__ == '__main__':
    from console import console
    console(globals())
