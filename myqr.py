import qrcode
from colorama import Fore, Back, Style, init
init()

def printQR(data = None, invert = True):
    qrCode = qrcode.main.QRCode()
    qrCode.add_data(data)
    matrix = qrCode.get_matrix()
    for row in matrix:
        line = []
        for pixel in row:
            if pixel ^ invert:
                line.append(Back.WHITE)
            else:
                line.append(Back.BLACK)
        print(*line, end = '  \n', sep = '  ')
    print(Style.RESET_ALL, end = '')

if __name__ == '__main__':
    print('You can print stuff before')
    printQR()
    print('And after. ')
    input('Enter...')
