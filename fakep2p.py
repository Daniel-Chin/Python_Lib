'''
Fake p2p. 
Connect, send(b'OK'), forward...
'''
# fake: CHUNK = 1024
import socket
from threading import Thread, Condition, Lock
from listen import listen

def fakeP2P(port = 2333):
    s = socket.socket()
    s.bind(('', port))
    s.listen(2)
    print('Listening... ')
    p_1, addr = s.accept()
    print(addr)
    p_2, addr = s.accept()
    print(addr)
    list_forwarder = []
    list_forwarder.append(Forwarder(p_1, p_2))
    list_forwarder.append(Forwarder(p_2, p_1))
    print('Go! ')
    print('Enter to end...')
    while listen([b'\r'],.5) is None:
        pass
    for forwarder in list_forwarder:
        with forwarder.condition:
            forwarder.do_stop = True
            while not forwarder.has_stopped:
                forwarder.condition.wait()
    input('Ended. Enter... ')

class Forwarder(Thread):
    def __init__(self, fro, to):
        Thread.__init__(self)
        self.condition = Condition()
        self.do_stop = False
        self.has_stopped = False
        to.sendall(b'OK')
        self.to = to
        self.fro = fro
    
    def goOn(self):
        with self.condition:
            return not self.do_stop
    
    def run(self):
        while self.goOn():
            try:
                data = self.fro.recv(1024)
            except:
                data = b''
            if data == b'':
                with self.condition:
                    self.do_stop = True 
            else:
                self.to.sendall(data)
        with self.condition:
            self.has_stopped = True
            self.client.close()
            self.condition.notify()

if __name__ == '__main__':
    fakeP2P()
