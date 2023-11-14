'''
Uses mido to play a midi file.  
'''

from __future__ import annotations

import mido
from myfile import sysArgvOrInput
from interactive import inputChin

VELOCITY_SCALE = 1

def channelMap(x: int):
    return 0

# def channelMap(x: int):
#     if x == 3:
#         return 0
#     return None

def main():
    filename = sysArgvOrInput()
    outputs = mido.get_output_names()
    for i, name in enumerate(outputs):
        print(i, name, sep = '\t')
    port_name = outputs[int(inputChin('> ', 0))]
    with mido.open_output(port_name) as port:
        down_keys = set()
        with mido.MidiFile(filename) as mid:
            print('playing...')
            try:
                for msg in mid.play():
                    print(msg)
                    if isinstance(msg, mido.MetaMessage):
                        continue
                    try:
                        msg.velocity = round(msg.velocity * VELOCITY_SCALE)
                        new_channel = channelMap(msg.channel)
                        if new_channel is None:
                            continue
                        msg.channel = new_channel
                    except AttributeError:
                        continue
                    port.send(msg)
                    if msg.type == 'note_on' and msg.velocity != 0:
                        down_keys.add(msg.note)
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        down_keys.discard(msg.note)
            except KeyboardInterrupt:
                print('Stop. ')
            finally:
                port.panic()
                # in case the MIDI device did not implement panic
                for note in down_keys:
                    port.send(mido.Message('note_off', note=note))
    print('ok')

main()
