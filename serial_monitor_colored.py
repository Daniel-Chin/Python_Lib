'''
PySerial already has a CLI monitor, but when it receives 
color formatting codes, it tries to print unprintable 
characters. Let's fix that.  
Also, we attach a time stamp to each line.  
'''
from time import sleep
from datetime import datetime
import argparse

import serial
import colorama

class ArgParser:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "port_name", type=str, 
        )
        parser.add_argument(
            "baud_rate", type=int, 
        )
        args = parser.parse_args()

        self.port_name: str = args.port_name
        self.baud_rate: int = args.baud_rate

def main():
    colorama.init()
    argParser = ArgParser()
    last_e_repr = None
    same_e_acc = 0
    while True:
        try:
            with serial.Serial(
                argParser.port_name, argParser.baud_rate, 
                timeout=1, 
            ) as s:
                print('\n\nSerial opened:', s.name)
                print('Baud rate:', argParser.baud_rate)
                print('==========')
                just_newline = True
                while True:
                    try:
                        if s.in_waiting:
                            data = s.read(s.in_waiting)
                        else:
                            sleep(.1)
                            continue
                    except KeyboardInterrupt:
                        print('bye')
                        return
                    for byte in data:
                        text = chr(byte)
                        if text == '\n':
                            print()
                            just_newline = True
                        else:
                            if just_newline:
                                just_newline = False
                                print(datetime.now().strftime(
                                    '%H:%M:%S', 
                                ), end=' ')
                            # text = repr(text)[1:-1]
                            print(text, end='')
                    print(end='', flush=True)
        except serial.serialutil.SerialException as e:
            e_repr = f'{e} {e.args}'
            if last_e_repr == e_repr:
                same_e_acc += 1
                print(f'The above exception repeated {same_e_acc} times. ', end='\r', flush=True)
            else:
                last_e_repr = e_repr
                print('\n\n', e_repr, '\n', sep='')
                same_e_acc = 0
            try:
                sleep(1)
            except KeyboardInterrupt:
                print('bye')
                return

main()
