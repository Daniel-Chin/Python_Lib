'''
Iterate through all files in this repo
build a readme.md for Github. 
'''
SUPPRESS = [
    'Archive/catch_eof/1.py',
    'Archive/hash_math/1.py', 
    'Archive/Magic.py', 
    'Beer on the Wall/Data/bamboozle.py', 
    'Beer on the Wall/Data/English.py', 
    'Beer on the Wall/Data/main.py', 
    'Beer on the Wall/Data/Song.py', 
    'Beer on the Wall/Data/Sound.py', 
    'Beer on the Wall/Data/troll.py', 
    'Color_Tiles/Mac_Install.py', 
    'Color_Tiles/Mac_Launcher.py', 
    'Color_Tiles/Read_Me.txt',
    'Color_Tiles/Windows_Install.py', 
    'console/__main__.py', 
    'console_explorer.py', 
    'DanielSecureChat/daniel_secure_chat.py', 
    'Find Vera/CharFinder.py', 
    'Find Vera/Chars.txt', 
    'Find Vera/flush_test.py', 
    'interactive/cls.py', 
    'interactive/__main__.py', 
    'listen.py', 
    'resize_image.py', 
    'To the Earth/Bin/Design.txt', 
    'To the Earth/Bin/Draft-Ab.txt', 
    'To the Earth/Bin/Draft.txt', 
    'To the Earth/Bin/EditSave.py', 
    'To the Earth/Bin/Weapons.txt', 
    'multi_term/another_term.py', 
    'multi_term/__main__.py', 
    'interactive/legacy/charGettor_demo.py', 
    'interactive/key_codes.py', 
]

import sys
import os
from os import path
from myfile import openAsciize

def main():
    os.chdir(path.dirname(path.abspath(__file__)))
    with open('readme.md', 'w') as out:
        with open('readme_head.md', 'r') as f:
            out.write(f.read())
        documentate('', out, depth = 1)
    input('Done. Enter...')

def documentate(cd, out, depth, folder_documented = False):
    if depth >= 2:
        try:
            with open('readme.md', 'r') as f:
                print('#' * depth, cd, file = out)
                doc = f.read().strip()
                if len(doc) < 3:
                    print('EMPTY README', cd)
                out.write(doc)
                out.write('\n\n')
            folder_documented = True
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
                        identifier = cd + node
                        if identifier not in SUPPRESS and not folder_documented:
                            print('No doc for file', identifier)
        else:   # isdir
            if node in ('.git', '__pycache__'):
                continue
            os.chdir(node)
            documentate(cd + node + '/', out, depth + 1, folder_documented)
            os.chdir('..')

main()
sys.exit(0)
