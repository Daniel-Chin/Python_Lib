'''
Provides fake p2p, port forwarding. 

Ignored the thread-danger of sockets. 
Expect unexpected behaviors. 
'''
__all__ = ['Forwarder', 'fakeP2P', 'portForward', 'bothForward']
import socket
from threading import Thread
from interactive import listen

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
                print('recv') ###
            except:
                data = b''
                print('recv except') ###
            if data == b'':
                print('close') ###
                self.to.close()
                self.fro.close()
                return
            else:
                try:
                    print('try send') ###
                    self.to.sendall(data)
                    print('sent') ###
                except:
                    print('send except') ###
                    return

def bothForward(socket_1, socket_2):
    forwarder_1 = Forwarder(socket_1, socket_2)
    forwarder_2 = Forwarder(socket_2, socket_1)
    forwarder_1.start()
    forwarder_2.start()
    return (forwarder_1, forwarder_2)

def fakeP2P(port = 2333):
    s = socket.socket()
    s.bind(('', port))
    s.listen(2)
    print('Listening... ')
    p_1, addr = s.accept()
    print(addr)
    p_2, addr = s.accept()
    print(addr)
    forwarders = bothForward(p_1, p_2)
    print('Go! ')
    print('Enter to end...')
    [x.join() for x in forwarders]
    input('Ended. Enter... ')

def portForward(inside_port, inbound_port, afraid = False):
    '''
    Set `afraid` to True to manually accept connections. 
    '''
    outServerSocket = socket.socket()
    outServerSocket.bind(('', inbound_port))
    outServerSocket.listen(afraid and 1 or 10)
    allForwarders = []
    allSockets = []
    try:
        while True:
            print('listening at port %d...' % inbound_port)
            outSocket, addr = outServerSocket.accept()
            print('Inbound connection from', addr)
            if afraid == True:
                print('Accept? y/n')
                if listen(['y', 'n']) != b'y':
                    outSocket.close()
                    print('Refused. ')
                    continue
            inSocket = socket.socket()
            allSockets.append(outSocket)
            allSockets.append(inSocket)
            print('Connecting inside port', inside_port)
            inSocket.connect(('localhost', inside_port))
            allForwarders += bothForward(outSocket, inSocket)
            print('-= ESTABLISHED =-')
            print()
    except KeyboardInterrupt:
        print('Ctrl+C received. ')
    finally:
        print(allForwarders, allSockets)
        print('Closing all sockets...')
        [x.close() for x in allSockets]
        outServerSocket.close()
        print('Joining...')
        for forwarder in allForwarders:
            forwarder.join()
            print('1 joined') ###
        print('All have joined. ')

if __name__ == '__main__':
    print(__all__)
    from console import console
    console(globals())
