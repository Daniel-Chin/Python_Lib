from socket import socket
import sys
from threading import Thread

DEFAULT_PORT = 2333
PAGE = 4096

def serveNow(port = DEFAULT_PORT):
    server = socket()
    server.bind(('', port))
    server.listen(10)
    try:
        while True:
            print('+ listening at port %d... ' % port)
            s, addr = server.accept()
            print('+ Connection from', addr, 'accepted. ')
            LoudReceiver(s).start()
    finally:
        server.close()

def getPort():
    if len(sys.argv) >= 2:
        return int(sys.argv[-1])
    else:
        op = input('Which port? (default %d) : ' % DEFAULT_PORT)
        if int(op) == 0:
            return DEFAULT_PORT
        else:
            return int(op)
class LoudReceiver(Thread):
    def __init__(self, socket):
        super(__class__, self).__init__()
        self.socket = socket
    
    def run(self):
        try:
            while True:
                print(' *', self.socket.recv(PAGE).decode())
        finally:
            self.socket.close()

if __name__ == '__main__':
    port = getPort()
    serveNow(port)
