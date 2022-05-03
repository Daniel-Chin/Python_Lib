'''
pyTorch utils.  
'''

import os
import sys

class LossLogger:
    def __init__(
        self, filename=None, print_every: int = 1, 
    ) -> None:
        if filename is None:
            self.filename = None
        else:
            self.filename = os.path.abspath(filename)
        self.print_every = print_every

    def __write(self, file, epoch_i, **kw):
        print('Finished epoch', epoch_i, ':', file=file)
        for k, v in kw.items():
            try:
                v = v.item()
            except AttributeError:
                pass
            print(' ', k, '=', v, file=file)
    
    def eat(self, epoch_i, verbose=True, **kw):
        if self.filename is not None:
            with open(self.filename, 'a') as f:
                self.__write(f, epoch_i, **kw)
        if verbose and epoch_i % self.print_every == 0:
            self.__write(sys.stdout, epoch_i, **kw)
    
    def clearFile(self):
        with open(self.filename, 'w'):
            pass
