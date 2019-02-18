'''
Sets up a server, displays a QR code. Scan it to go to a web page. Exchange raw texts!  
Useful for sending a URL from the phone to the laptop.  
Warning: No authentication or encryption. Don't type in secrets. Don't assume who the remote is.  
'''
print('Loading...')
from myhttp import *
import qrcode
from local_ip import getLocalIP
import os

PORT = 2339

def main():
    server = MyServer(MyOneServer, PORT)
    server.start()
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    potential_ip = getLocalIP()
