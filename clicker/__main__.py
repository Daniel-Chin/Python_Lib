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
import subprocess
import os
from time import sleep

PORT = 2338

trusted_ip = None

def main():
    server = MyServer(MyOneServer, PORT)
    server.start()
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    ip_config = subprocess.check_output('ipconfig').decode('gbk')
    for line in ip_config.split('\r\n'):
        if 'IPv4' in line:
            print(line)
    print(f'Listening on port {PORT}...')
    print('Ctrl+C to stop.')
    try:
        while True:
            sleep(1)
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
