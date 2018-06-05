print('importing...')
from recvfile import recvFile
from listen import listen
from pickle_socket import PickleSocket
from tkinter import Tk,filedialog
from socket import gethostname,gethostbyname
import sys
from os.path import getsize,basename,isfile,splitext

print('loading...')
port=2337

def main():
    global port
    s=PickleSocket()
    print('My IP =',gethostbyname(gethostname()))
    print('Server or Client? s/c')
    if listen((b's',b'c')) == b's':
        s.bind(('',port))
        s.listen(1)
        print('Listening...')
        s,addr=s.accept()
        print('Connection from',addr)
        print('Accept? y/n')
        if listen((b'y',b'n')) == b'n':
            s.close()
            input('Aborted. Enter to exit...')
            sys.exit(1)
    else:
        ip=input('Connect to IP: ')
        print('Connecting...')
        s.connect((ip,port))
    print('Connected! ')
    s.shakeHands('One ship python by Daniel Chin. ')
    
    esc=b'\x1b'
    op=b''
    while op != esc:
        if op==b's':
            send(s)
        elif op==b'r':  #Cannot use ELSE, cuz op maybe esc. 
            recv(s)
        print('Send, receive, or exit? s/r/esc')
        op=listen((b's',b'r',esc))
    s.close()

def send(s):
    root=Tk()
    root.withdraw()
    filename=filedialog.askopenfilename(title='Choose file to send',initialdir='D:/')
    if filename=='':
        s.sendObj(0)
        return None
    size=getsize(filename)
    print('Sending...')
    s.sendObj(basename(filename))
    s.sendObj(size)
    s.socket.sendfile(open(filename,'rb'))
    print('File sent:',filename)

def recv(s):
    print('Waiting for sender...')
    basename=s.recvObj()
    size=s.recvObj()
    path='D:/downloads/'
    print('Default receive path:',path)
    print('Use it, or change? Enter/c')
    if listen((b'c',b'\r'))==b'c':
        root=Tk()
        root.withdraw()
        filename=filedialog.asksaveasfilename(title='Where to receive',initialdir='D:/',initialfile=basename)
        if filename=='':
            s.close()
            input('Error: filename="". Enter to exit...')
            sys.exit(1)
    else:    
        filename=path+basename
    while isfile(filename):
        base,ext=splitext(filename)
        base+='2'
        filename=base+ext
    recvFile(s.socket,size,filename)
    print('File received:',filename)

if __name__=='__main__':
    main()
    sys.exit(0)
