import qrcode
from colorama import Fore, Back, Style, init
init()

def printQR(data = None):
    qrCode = qrcode.main.QRCode()
    qrCode.add_data(data)
    matrix = qrCode.get_matrix()
    if len(matrix) % 2 == 1:
        matrix.append(matrix[0])
    iter_matrix = iter(matrix)
    for row_up in iter_matrix:
        row_down = next(iter_matrix)
        line = []
        for up, down in zip(row_up, row_down):
            if up ^ down:
                char = '▄'
            else:
                char = '⃪'
            if up:
                line.append(Fore.WHITE)
                line.append(Back.LIGHTBLACK_EX)
            else:
                line.append(Back.LIGHTWHITE_EX)
                line.append(Fore.BLACK)
            line.append(char)
        print(*line, sep = '')
    print(Style.RESET_ALL, end = '')

if __name__ == '__main__':
    print('You can print stuff before')
    printQR()
    print('And after. ')
    input('Enter...')
