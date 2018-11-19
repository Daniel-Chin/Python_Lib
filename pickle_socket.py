'''
A socket that supports object transmission. 
'''
import socket
import pickle
from io import BytesIO
import sys
__all__ = ['PickleSocket', 'RemoteClosedUnexpectedly']

class PickleSocket():
    def __init__(self,upon_this_socket=None):
        if upon_this_socket is None:
            self.socket=socket.socket()
        else:
            self.socket=upon_this_socket
    
    def shakeHands(self,banner='This is a pickleSocket by Daniel Chin. ',echo=True):
        self.sendObj(banner)
        recved=self.recvObj()
        if recved==banner:
            if echo:
                print('Shake hands success.')
        else:
            print('Error: Shake hands failure! ')
            print('Banner:',banner)
            print('Received:',recved)
            input('Enter to exit...')
            sys.exit(1)
    
    def bind(self,address,local=False):
        '''
        if `local` is True, address is no longer a tuple, but a port int.
        '''
        if local:
            self.socket.bind(('127.0.0.1',address))
        else:
            self.socket.bind(address)
    
    def listen(self,capacity):
        self.socket.listen(capacity)
    
    def connect(self,address,AB=False,dorm=False,local=False):
        '''if AB or dorm is True, address is no longer a tuple, but a port int.'''
        if AB:
            self.socket.connect(('10.209.1.45',address))
        elif dorm:
            self.socket.connect(('10.209.23.186',address))
        elif local:
            self.socket.connect(('127.0.0.1',address))
        else:
            self.socket.connect(address)
    
    def sendObj(self,obj):
        io_obj=BytesIO()
        pickle.dump(obj,io_obj)
        size=io_obj.tell()
        io_obj.seek(0)
        sent=self.socket.sendfile(io_obj)
        while sent<size:
            sent+=self.socket.sendfile(io_obj)
    
    def recvObj(self):
        return pickle.load(IoSocket(self.socket))
    
    def send(self,*args):
        return self.socket.send(*args)
    
    def recv(self,*args):
        return self.socket.recv(*args)
    
    def accept(self):
        s,addr=self.socket.accept()
        s=self.__class__(s)
        return s,addr 
    
    def close(self):
        return self.socket.close()

class IoSocket:
    def __init__(self,socket):
        self.socket=socket
    
    def read(self,count=1):
        read=self.socket.recv(count)
        if read==b'':
            raise RemoteClosedUnexpectedly 
        return  read
    
    def readline(self):
        read=b''
        buffer=b''
        while read !=b'\n':
            read=self.read(1)
            buffer+=read
        return buffer

class RemoteClosedUnexpectedly(BaseException):
    pass
