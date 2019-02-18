'''
Sets up a server, displays a QR code. Scan it to go to a web page. Exchange raw texts!  
Useful for sending a URL from the phone to the laptop.  
Warning: No authentication or encryption. Don't type in secrets. Don't assume who the remote is.  
'''
print('Loading...')
from myhttp import *
import qrcode
from local_ip import getLocalIP
import os, sys
import urllib
from threading import Thread

PORT = 2339

def main():
    server = Server(MyOneServer, PORT)
    server.start()
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    potential_ip = getLocalIP()
    imgs = []
    class ShowImgThread(Thread):
        def __init__(self, img):
            Thread.__init__(self)
            self.img = img
        
        def run(self):
            self.img.show()
    potential_ip = {*potential_ip} - {'192.168.56.1'}
    # Cisco Anyconnect shit
    for ip in potential_ip:
        addr = 'http://%s:%d' % (ip, PORT)
        try:
            imgs.append(qrcode.make(addr))
        except Exception as e:
            print('Error 198456', e)
        print(addr)
    [ShowImgThread(x).start() for x in imgs]
    try:
        input()
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
        elif request.target.startswith('/msg'):
            msg = urllib.parse.unquote(request.target[4:])
            print(msg)
            respond(self.socket, b'Yup')
        elif request.target in ['/favicon.ico']:
            pass
        else:
            print('Unknown request:', request.target)

if __name__ == '__main__':
    main()
    sys.exit(0)
