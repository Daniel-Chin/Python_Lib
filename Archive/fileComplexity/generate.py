from os import urandom

def writeRand(size, f):
    while size > 0:
        here = min(size, 4096)
        f.write(urandom(here))
        size -= here

for i in range(30):
    size = 2 ** i
    print(size)
    with open(f'{i}.data', 'wb') as f:
        writeRand(size, f)
