'''
Tools to do graphics in the terminal.  
`clearLine`: fill the current line with ' ' (whitespace)  
`eastAsianStrLen`: length of str as displayed on terminal (so chinese characters and other fullwidth chars count as 2 or more spaces)  
`displayAllColors`: display all colors that your terminal supports.  
`printTable`: print a table in the terminal.  
'''
__all__ = ['clearLine', 'eastAsianStrToWidths', 
    'eastAsianStrLen', 'eastAsianStrLeft', 'eastAsianStrRight', 
    'displayAllColors', 'eastAsianStrSparse', 'printTable', 
    'eastAsianStrPad']
from terminalsize import get_terminal_size
from unicodedata import east_asian_width

def clearLine():
    '''
    Clears the current line, then \r. 
    Used when previously printed without \n. 
    '''
    terminal_width = get_terminal_size()[0] - 1
    print('\r', ' ' * terminal_width, end = '\r', sep = '')

def eastAsianStrSparse(s, marks = []):
    chars = []
    marks_movement = {}
    for i, char in enumerate(s):
        if i in marks:
            marks_movement[i] = len(chars)
        chars.append(char)
        if east_asian_width(char) in 'AFNW':
            chars.append('')
    if marks:
        return chars, [marks_movement[x] for x in marks]
    else:
        return chars

def eastAsianStrToWidths(s, fullwidth_scale = 2):
    widths = []
    for char in s:
        if east_asian_width(char) in 'AFNW':
            widths.append(fullwidth_scale)
        else:
            widths.append(1)
    return widths

def eastAsianStrLen(s, fullwidth_scale = 2):
    return sum(eastAsianStrToWidths(s, fullwidth_scale))

def eastAsianStrLeft(s, n):
    widths = eastAsianStrToWidths(s)
    width = 0
    for i, w in enumerate(widths):
        width += w
        if width > n:
            return s[:i]
    return s

def eastAsianStrRight(s, n):
    widths = eastAsianStrToWidths(s)
    width = 0
    for i, w in reversed(tuple(enumerate(widths))):
        width += w
        if width >= n:
            return s[i:]
    return s

def eastAsianStrPad(s, padding, pad_char = ' '):
    return s + pad_char * (padding - eastAsianStrLen(s))

def displayAllColors():
    from colorama import init, Back, Fore, Style
    init()
    all_colors = [x for x in dir(Back) if x[0] != '_']
    for color in all_colors:
        print(Fore.RESET, ' ', Back.__getattribute__(color), color, end = '', flush = True, sep = '')
        print(Back.RESET, ' ', Fore.__getattribute__(color), color, end = '', flush = True, sep = '')
    print(Style.RESET_ALL)

def printTable(table):
    col_width = [0 for _ in table[0]]
    for line in table:
        for i, x in enumerate(line):
            line[i] = str(x)
            col_width[i] = max(col_width[i], eastAsianStrLen(line[i]))
    for line in table:
        print(' | ', end = '')
        for i, text in enumerate(line):
            print(eastAsianStrPad(text, col_width[i]), end=' | ')
        print()

if __name__ == '__main__':
    from console import console
    displayAllColors()
    printTable([
        ['ID', 'Name', 'Thing'], 
        ['32678941829045312', 'Daniel', 'This is a demo'], 
        ['340286501983078', 'Person B', 'Thing 2'], 
    ])
    console(globals())
