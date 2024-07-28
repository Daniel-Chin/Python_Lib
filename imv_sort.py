'''
Sort files and pass them to imv.  
'''

import os

def main():
    files = os.popen(
        'ls -1t', 
    ).read().strip().split('\n')
    command = f'imv {" ".join(files)}'
    print(command)
    os.system(command)

if __name__ == '__main__':
    main()
