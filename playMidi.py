'''
Uses mido to play a midi file.  
'''

import sys
import mido
from myfile import sysArgvOrInput
from interactive import inputChin

def main():
    filename = sysArgvOrInput()
    outputs = mido.get_output_names()
    for i, name in enumerate(outputs):
        print(i, name, sep = '\t')
    port_name = outputs[int(inputChin('> ', 0))]
    with mido.open_output(port_name) as port:
        with mido.MidiFile(filename) as mid:
            print('playing...')
            try:
                for msg in mid.play():
                    print(msg)
                    port.send(msg)
            except KeyboardInterrupt:
                print('Stop. ')
    print('ok')

main()
