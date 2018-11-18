from terminalsize import get_terminal_size

def clearLine():
    '''
    Clears the current line, then \r. 
    Used when previously printed without \n. 
    '''
    terminal_width = get_terminal_size()[0] - 4
    print('\r', ' ' * terminal_width, end = '\r', sep = '')
