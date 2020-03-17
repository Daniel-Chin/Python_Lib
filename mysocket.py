'''
My socket utils. Provides `recvall`, `recvFile`, `sendFileJdt`, and `findAPort`.  
'''
import jdt
from socket import socket
import os
from pickle_socket import PickleSocket
from interactive import inputUntilValid, inputChin

PAGE = 4096
RUSH = 128
RUSHxPAGE = RUSH * PAGE

def recvFile(s, file_len, to_filename):
    '''
    receive a file from a socket with known length. 
    '''
    assert type(s) is socket
    j = jdt.CommJdt(file_len, msg = to_filename)
    with open(to_filename, 'wb+') as to_file:
        left = file_len
        while left:
            for _ in range(RUSH):
                left -= to_file.write(s.recv(min(left, PAGE)))
            recved = s.recv(min(left, PAGE))
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

def sendFileJdt(s, file):
    assert type(s) is socket
    save_pos = file.tell()
    total = file.seek(0, os.SEEK_END)
    if not total:
        print('mysocket Warning: file.seek did not return file size, using plan B. Daniel: change it to `seek() or tell()`')
        total = file.tell()
    file.seek(save_pos)
    j = jdt.CommJdt(total, msg = 'send')
    estimated_sent = 0
    read = None
    while read != b'':
        if estimated_sent > total:
            print('mysocket warning: OMG it actually happens! estimation drifted up! ')
        else:
            j.update(estimated_sent)
        for i in range(RUSH):
            read = file.read(PAGE)
            s.sendall(read)
        estimated_sent += RUSHxPAGE
    j.complete()

def findAPort(hostname = 'localhost', search_range = range(3000, 4000)):
    '''
    finds an available port in `range`, default 3000~4000.  
    Returns (socket, port), where socket is binded but not listening.  
    '''
    for port in search_range:
        serverSock = socket()
        try:
            serverSock.bind((hostname, port))
            return (serverSock, port)
        except OSError:
            serverSock.close()

def pair(port, host_ip = 'localhost', handshake_msg = 'mysocket.pair'):
    '''
    Establish pickleSocket pair with minimum security (asks user to confirm IP)  
    '''
    role = inputUntilValid('Client or Server?', 'cs')
    s = PickleSocket()
    if role == 's':
        s.bind((host_ip, port))
        s.listen(1)
        print(f'Waiting for connection @ {host_ip}:{port}...')
        cs, addr = s.accept()
        print('Connection from', addr)
        if inputUntilValid('Accept?', 'yn') != 'y':
            cs.close()
            s.close()
            print('Refused.')
            return
        cs.shakeHands(handshake_msg)
        return cs
    elif role == 'c':
        ip = inputChin('IP = ', 'localhost')
        s.connect((ip, port))
        print('Waiting for server to accept...')
        try:
            s.shakeHands(handshake_msg)
        except ConnectionResetError:
            print('The server rejected.')
            return
        return s, ip

if __name__ == '__main__':
    pair(2333)
