'''
receive a file from a socket with known length. 
'''
import jdt
from socket import socket as Socket

def recvFile(socket,file_len,to_filename):
    assert type(socket) is Socket
    j=jdt.CommJdt(file_len, msg = to_filename)
    with open(to_filename,'wb+') as to_file:
        left=file_len
        while left:
            for i in range(128):
                left-=to_file.write(socket.recv(min(left,4096)))
            recved=socket.recv(min(left,4096))
            if recved == b'':
                if left:
                    assert False
            else:
                left-=to_file.write(recved)
                j.update(file_len-left)
        j.complete()
