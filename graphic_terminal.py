'''
Tools to do graphics in the terminal.
'''
from terminalsize import get_terminal_size
from unicodedata import east_asian_width

def clearLine():
    '''
    Clears the current line, then \r. 
    Used when previously printed without \n. 
    '''
    terminal_width = get_terminal_size()[0] - 4
    print('\r', ' ' * terminal_width, end = '\r', sep = '')

def eastAsianStrLen(s, fullwidth_scale = 2):
    length = 0
    for char in s:
        if east_asian_width(char) in 'AFNW':
            length += fullwidth_scale
        else:
            length += 1
    return length
