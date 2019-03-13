from myfile import sysArgvOrInput
from subprocess import Popen

with open(sysArgvOrInput(), 'rb') as f:
    with open('temp', 'wb+') as o:
        p = Popen('python', stdin = f, stdout = o)
        p.wait()
    f.seek(0)
    src = f.read()
with open('temp', 'rb') as o:
    output = o.read()
if src == output:
    print('quine')
else:
    print('not quine')
    print(src)
    print(output)
input('enter...')
