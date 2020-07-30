'''
Worried that your async callbacks may fire in the middle of and `update()` and cause race condition?  
This module schedules async callbacks for tkinter.  
'''

__all__ = [ 'sched', 'tkAsync' ]

from tkinter import TclError

default_root = None

def sched(*args, **kw):  # only use this when your app has only 1 window
  default_root.sched(*args, **kw)

class TkAsync:    
  def __init__(self, root):
    self.root = root
    self.scheded = []
    root.mainloop = self.mainloop
    root.sched = self.sched
  
  def mainloop(self):
    while True:
      for func, args, kw in self.scheded:
        func(*args, **kw)
      try:
        self.root.update()
      except TclError as e:
        if 'application has been destroyed' in e.args[0]:
          break
        raise e
  
  def sched(self, func, *args, **kw):
    self.scheded.append((func, args, kw))

def tkAsync(root):
  global default_root
  TkAsync(root)
  default_root = root
