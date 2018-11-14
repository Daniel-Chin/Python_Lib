'''
Windows only
'''
print('Loading...')
import keyboard
from listen import listen
import sys
from myhttp import *
import subprocess
import os
from time import sleep

PORT = 2338

trusted_ip = None

def main():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    ip_config = subprocess.check_output('ipconfig').decode('gbk')
    for line in ip_config.split('\r\n'):
        if 'IPv4' in line:
            print(line)
    print(f'Listening on port {PORT}...')
    server = MyServer(MyOneServer, PORT)
    server.start()
    print('Ctrl+C to stop.')
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        server.join()

class MyOneServer(OneServer):
    def handle(self, request):
        if request.target == '/':
            with open('page.html', 'rb') as f:
                respond(self.socket, f.read())
        elif request.target == '/click':
            keyboard.press('space')
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
