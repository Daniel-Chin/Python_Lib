'''
My socket utils. Provides `recvall`, `recvFile`, and `sendFileJdt`. 
'''
import jdt
from socket import socket

def recvFile(s, file_len, to_filename):
    '''
    receive a file from a socket with known length. 
    '''
    assert type(s) is socket
    j = jdt.CommJdt(file_len, msg = to_filename)
    with open(to_filename, 'wb+') as to_file:
        left = file_len
        while left:
            for i in range(128):
                left -= to_file.write(s.recv(min(left, 4096)))
            recved = s.recv(min(left, 4096))
            if recved == b'':
                if left:
                    assert False
            else:
                left -= to_file.write(recved)
                j.update(file_len - left)
        j.complete()

def recvall(s, size, use_list = True):
    '''
    Receive `size` bytes from socket `s`. Blocks until gets all. 
    Somehow doesn't handle socket closing. 
    I will fix that when I have time. 
    '''
    if use_list:
        left = size
        buffer = []
        while left > 0:
            buffer.append(s.recv(left))
            left -= len(buffer[-1])
        recved = b''.join(buffer)
    else:
        recved = b''
        while len(recved) < size:
            recved += s.recv(left)
    return recved
