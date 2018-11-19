'''
Provides fake p2p, port forwarding. 

Ignored the thread-danger of sockets. 
Expect unexpected behaviors. 
'''
__all__ = ['Forwarder', 'fakeP2P', 'portFoward', 'bothFoward']
import socket
from threading import Thread

CHUNK = 4096

class Forwarder(Thread):
    def __init__(self, fro, to):
        Thread.__init__(self)
        self.to = to
        self.fro = fro
    
    def run(self):
        while True:
            try:
                data = self.fro.recv(CHUNK)
            except:
                data = b''
            if data == b'':
                self.to.close()
                self.fro.close()
                return
            else:
                self.to.sendall(data)

def bothFoward(socket_1, socket_2):
    fowarder_1 = Forwarder(socket_1, socket_2)
    fowarder_2 = Forwarder(socket_2, socket_1)
    fowarder_1.start()
    fowarder_2.start()
    return (fowarder_1, fowarder_2)

def fakeP2P(port = 2333):
    s = socket.socket()
    s.bind(('', port))
    s.listen(2)
    print('Listening... ')
    p_1, addr = s.accept()
    print(addr)
    p_2, addr = s.accept()
    print(addr)
    fowarders = bothFoward(p_1, p_2)
    print('Go! ')
    print('Enter to end...')
    [x.join() for x in fowarders]
    input('Ended. Enter... ')

def portFoward(inside_port, inbound_port):
    outServerSocket = socket.socket()
    outServerSocket.bind(('', inbound_port))
    outServerSocket.listen(10)
    while True:
        print('listening at port %d...' % inbound_port)
        outSocket, addr = outServerSocket.accept()
        print('Inbound connection from', addr)
        inSocket = socket.socket()
        print('Connecting inside port', inside_port)
        inSocket.connect(('localhost', inside_port))
        bothFoward(outSocket, inSocket)
        print('-= ESTABLISHED =-')
        print()

if __name__ == '__main__':
    print(__all__)
    from console import console
    console(globals())
