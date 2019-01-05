'''
My laptop is weird. Running this script makes opening and terminating processes faster. 
Speculation: Taking CPU time away from Windows Defender? 
'''
from subprocess import Popen
from time import sleep
from os import kill

SIGKILL: int = 9

def main(): 
    while True:
        print('open')
        p: Popen = Popen('taskmgr')
        sleep(5)
        print('kill')
        kill(p.pid, SIGKILL)
        sleep(2)

if __name__ == '__main__':
    main()
