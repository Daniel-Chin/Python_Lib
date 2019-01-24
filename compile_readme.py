'''
Iterate through all files in this repo
build a readme.md for Github. 
'''
import sys
import os
from os import path
from myfile import openAsciize

def main():
    os.chdir(path.dirname(path.abspath(__file__)))
    with open('readme.md', 'w+') as out:
        with open('readme_head.md', 'r') as f:
            out.write(f.read())
        documentate('', out, depth = 1)

def documentate(cd, out, depth):
    if depth >= 2:
        try:
            with open('readme.md', 'r') as f:
                print('#' * depth, cd, file = out)
                doc = f.read().strip()
                if len(doc) < 3:
                    print('EMPTY README', cd)
                out.write(doc)
                out.write('\n\n')
        except:
            pass
    for node in os.listdir():
        if path.isfile(node):
            ext = path.splitext(node)[-1]
            if ext in ('.py', '.txt', 'pyw'):
                with openAsciize(node) as f:
                    documented = False
                    for line in f:
                        line = line.decode().strip('\r\n')
                        if line == "'''":
                            documented = True
                            break
                        if line == '' or line[0] == '#':
                            continue
                        break
                    if documented:
                        print('#' * (depth+1), cd+node, file = out)
                        buffer = []
                        for line in f:
                            line = line.decode().strip('\r\n')
                            if line == "'''":
                                break
                            buffer.append(line)
                        print(*buffer, file = out, end = '\n\n', sep = '  \n')
                    else:
                        print('No doc for file', cd, node)
        else:   # isdir
            if node in ('.git', '__pycache__'):
                continue
            os.chdir(node)
            documentate(cd + node + '/', out, depth + 1)
            os.chdir('..')

main()
sys.exit(0)
