'''
Windows only. 
Use your phone to send UP and DOWN to your computer! 
Useful for reading in Kindle. 

WARNING: Running this may open vulnerabilities for your computer. 
Don't run this if you don't know what you are doing. 
Only run this if you are in a safe network, or inside a firewall. 
I am not responsible if someone attacks your computer through this server. 
'''
print('Loading...')
import keyboard
from interactive import listen
import sys
from myhttp import *
import os
from time import sleep
from myqr import printQR
from local_ip import getLocalIP

PORT = 2338

trusted_ip = None

def main():
    server = MyServer(MyOneServer, PORT)
    server.start()
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    potential_ip = {*getLocalIP()} - {'192.168.56.1'} # Cisco Anyconnect shit
    addrs = ['http://%s:%d' % (ip, PORT) for ip in potential_ip]
    if len(potential_ip) < 3:
        print(*addrs, sep = ' ' * 4)
        printQR(*addrs)
    else:
        for addr in addrs:
            print(addr)
            printQR(addr)
            print()
    print('Ctrl+C to stop.')
    print('Q to display QR code for phone scan.')
    try:
        while True:
            op = listen(timeout = 1)
            if op == b'\x03':
                raise KeyboardInterrupt
            elif op == b'q':
                [ShowImgThread(x).start() for x in imgs]
            elif op == b'\r':
                print()
    except KeyboardInterrupt:
        print('Received ^C. ')
    finally:
        server.close()
        server.join()

class MyOneServer(OneServer):
    def handle(self, request):
        if request.target == '/':
            with open('page.html', 'rb') as f:
                respond(self.socket, f.read())
        elif request.target == '/down':
            keyboard.press('down')
            respond(self.socket, b'Yup')
        elif request.target == '/up':
            keyboard.press('up')
            respond(self.socket, b'Yup')
        elif request.target in ['/favicon.ico']:
            pass
        else:
            print('Unknown request:', request.target)

class MyServer(Server):
    def onConnect(self, addr):
        global trusted_ip
        if trusted_ip is None:
            trusted_ip = addr[0]
        elif addr[0] != trusted_ip:
            print('SOMEONE IS ATTACKING!', addr)
            self.close()

if __name__ == '__main__':
    main()
    sys.exit(0)
