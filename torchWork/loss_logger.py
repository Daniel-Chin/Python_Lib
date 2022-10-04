import os
import sys

from indentprinter import IndentPrinter
from torchWork.loss_tree import Loss

class LossLogger:
    def __init__(
        self, filename=None, print_every: int = 1, 
    ) -> None:
        if filename is None:
            self.filename = None
        else:
            self.filename = os.path.abspath(filename)
        self.print_every = print_every

    def __write(self, file, epoch_i, lossRoot: Loss, loss_weights):
        def p(*a, **kw):
            print(*a, file=file, **kw)
        p('Finished epoch', epoch_i, ':',)
        with IndentPrinter(p, 2 * ' ') as p:
            self.dfs(p, lossRoot, loss_weights)
    
    def eat(
        self, epoch_i: int, lossRoot: Loss, loss_weights, 
        verbose=True, 
    ):
        if self.filename is not None:
            with open(self.filename, 'a') as f:
                self.__write(f, epoch_i, lossRoot, loss_weights)
        if verbose and epoch_i % self.print_every == 0:
            self.__write(sys.stdout, epoch_i, lossRoot, loss_weights)
            sys.stdout.flush()

    def dfs(self, p, loss: Loss, loss_weights):
        p(loss.name, '=', loss.sum(loss_weights))
        with IndentPrinter(p, 2 * ' ') as p:
            for name, weight, sub_weights in loss_weights:
                child = loss.__getattribute__(name)
                if sub_weights is None:
                    p(name, '=', child)
                else:
                    self.dfs(p, child, sub_weights)

    def clearFile(self):
        with open(self.filename, 'w'):
            pass
