'''
My misc little tools.  
'''
import os

class ChangeDir:
    def __init__(self, path):
        self.path = path
        self.home = []
    
    def __enter__(self):
        self.home.append(os.getcwd())
        os.chdir(self.path)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.home.pop(-1))

def debug(func, *args, **kw):
    try:
        func(*args, **kw)
    except Exception:
        import traceback
        traceback.print_exc()
        input('Enter...')
