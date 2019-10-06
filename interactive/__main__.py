from interactive import *
import interactive


from interactive import charGettor as c
from time import sleep
from os import getpid
print('pid',getpid())
print(c.consume(timeout = 1))
sleep(1)
print(c.consume(timeout = 1))
'''


print('Demoing `inputChin`:')
a = inputChin('set X = ', 26)
print(a)
from console import console
print(interactive.__all__)
console(globals())
'''
