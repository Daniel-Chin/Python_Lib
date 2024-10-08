'''
Uses mido to play a midi file.  
'''

from __future__ import annotations

import typing as tp

import mido
from myfile import sysArgvOrInput
from interactive import inputChin

def any2zero(x: int):   # an example channel remap
    return 0

def identity(x: int):
    return x

def askOutput():
    outputs = mido.get_output_names()   # type: ignore
    for i, name in enumerate(outputs):
        print(i, name, sep = '\t')
    selected = outputs[int(inputChin('> ', '0'))]
    print(f'{selected = }')
    return selected

def main(
    filename: str | None = None, 
    midi_output_name: str | None = None,
    channel_remap: tp.Callable[[int], int | None] = identity,
    scale_velocity: float = 1.0, 
    discard_meta: bool = True, 
    verbose: bool = True, 
):
    '''
    `channel_remap`: return None to discard message.  
    '''
    filename = filename or sysArgvOrInput()
    midi_output_name = midi_output_name or askOutput()
    with mido.open_output(midi_output_name) as port:    # type: ignore
        down_keys = set()
        with mido.MidiFile(filename) as mid:
            if verbose:
                print('playing...')
            try:
                for msg in mid.play(meta_messages = not discard_meta):
                    if verbose:
                        print(msg)
                    try:
                        msg.velocity = round(msg.velocity * scale_velocity)
                        new_channel = channel_remap(msg.channel)
                        if new_channel is None:
                            continue
                        msg.channel = new_channel
                    except AttributeError:
                        pass    # allow control_change
                    port.send(msg)
                    if msg.type == 'note_on' and msg.velocity != 0:
                        down_keys.add(msg.note)
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        down_keys.discard(msg.note)
            except KeyboardInterrupt:
                if verbose:
                    print('Stop. ')
            finally:
                port.panic()
                # in case the MIDI device did not implement panic
                for note in down_keys:
                    port.send(mido.Message('note_off', note=note))
    if verbose:
        print('ok')

if __name__ == '__main__':
    main()
