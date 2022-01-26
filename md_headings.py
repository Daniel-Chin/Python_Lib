'''
Print the headings of a markdown file.  
'''

from myfile import parseArgsOrInput

def main():
    filename = parseArgsOrInput()
    print()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                line = line.lstrip(' \t')
                line = line.rstrip('\r\n')
                print(line)
                # line = line.lstrip('#')
    print()

main()
