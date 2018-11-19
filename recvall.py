'''
Receive `size` bytes from `socket`. Blocks until gets all. 
Somehow doesn't handle socket closing. 
I will fix that when I have time. 
'''

def recvall(socket, size, use_list = True):
    if use_list:
        left = size
        buffer = []
        while left > 0:
            buffer.append(socket.recv(left))
            left -= len(buffer[-1])
        recved = b''.join(buffer)
    else:
        recved = b''
        while len(recved) < size:
            recved += socket.recv(left)
    return recved
