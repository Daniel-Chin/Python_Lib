import sys
from forcemap import forceMap
from console import console
from os import system as cmd
from pickle_socket import PickleSocket
from time import time

TIMEOUT = 10
THREADS = 16

def main():
    global hosts, result, s
    ss = PickleSocket()
    ss.bind(('localhost', 2333))
    ss.listen(1)
    print('listening...')
    s, addr = ss.accept()
    s.shakeHands()
    result = forceMap(ping, range(256**2), THREADS)
    hosts = [x for x in result if x is not None]
    cmd('cls')
    print('There are:', len(hosts))
    console(globals())

def ping(i):
    ip = '10.209'
    ip += '.' + str(i // 256)
    ip += '.' + str(i % 256)
    start = time()
    cmd('ping ' + ip)
    if time() - start < TIMEOUT:
        s.sendObj((True, ip))
        return ip
    else:
        s.sendObj((False, ip))
        return None

main()
sys.exit(0)
