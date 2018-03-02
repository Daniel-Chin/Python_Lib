import os
import sys
import time

now = '_'.join(format(x, '02') for x in time.gmtime()[:6])
dirname = os.path.dirname(__file__)
os.rename(__file__, os.path.join(dirname, now + '.pyw'))
