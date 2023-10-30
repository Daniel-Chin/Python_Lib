'''
Uses mido to play a midi file.  
'''

from __future__ import annotations

import mido
from myfile import sysArgvOrInput
from interactive import inputChin

VELOCITY_SCALE = .5
FORCE_CHANNEL: int | None = 0

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
                    if isinstance(msg, mido.MetaMessage):
                        continue
                    try:
                        msg.velocity = round(msg.velocity * VELOCITY_SCALE)
                        if FORCE_CHANNEL is not None:
                            msg.channel = FORCE_CHANNEL
                    except AttributeError:
                        continue
                    port.send(msg)
            except KeyboardInterrupt:
                print('Stop. ')
    print('ok')

main()
