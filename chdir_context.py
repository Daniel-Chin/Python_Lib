'''
A context to temporarily cd to another directory.  
Frequently useful: Chdir2(__file__)  
'''
import os

class ChdirStack:
    def __init__(self, to):
        self.stack = []
        self.to = to
    
    def __enter__(self):
        self.stack.append(os.getcwd())
        os.chdir(self.to)
    
    def __exit__(self, type, value, traceback):
        os.chdir(self.stack.pop(-1))

def Chdir2(_file_):
    return ChdirStack(os.path.dirname(_file_))

if __name__ == '__main__':
    print('demo')
    print('Going from', os.getcwd())
    with Chdir2(__file__):
        print('to', os.getcwd())
    print('and back to', os.getcwd())
    input('enter...')
