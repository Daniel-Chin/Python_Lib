'''
Uses HarmonicSynth (precise) for the lower register 
and IfftSynth (fast) for the higher register.  
'''

import numpy as np
from harmonicSynth import HarmonicSynth, Harmonic
from ifftSynth import IfftSynth

BLANK = Harmonic(220, 0)

class HybridSynth:
    '''
    `max_out_of_tune`: smaller gives better precision but 
    slower to synth. (It decides the register cutoff.)  
    '''
    def __init__(
        self, n_harmonics, SR, PAGE_LEN, DTYPE, 
    ):
        self.n_harmonics = n_harmonics
        self.SR = SR
        self.PAGE_LEN = PAGE_LEN
        self.DTYPE = DTYPE
        self.bin_freq = SR / PAGE_LEN
        self.hSynth = HarmonicSynth(
            n_harmonics, SR, PAGE_LEN, DTYPE, 
            STUPID_MATCH=True, DO_SWIPE=False, 
        )
        self.iSynth = IfftSynth(SR, PAGE_LEN)
        self.ifft_signal = None
    
    def errorRange(self, freq):
        return np.log(
            (freq + self.bin_freq) / freq
        ) / 2 * 17.312340490667562
    
    def eat(self, harmonics, verbose=True):
        harmonics.sort(key=self.hSynth.getMag)
        low_harmonics = harmonics[:self.n_harmonics]
        high_harmonics = harmonics[self.n_harmonics:]
        if verbose and high_harmonics:
                print(
                    'ifft error', 
                    self.errorRange(high_harmonics[0].freq), 
                    'semitones. '
                )
        n_blank_harmonics = self.n_harmonics - len(low_harmonics)
        for _ in range(n_blank_harmonics):
            low_harmonics.append(BLANK)
        self.hSynth.eat(low_harmonics)
        self.ifft_signal = self.iSynth.eat(
            high_harmonics
        ).astype(self.DTYPE)
    
    def mix(self):
        return self.hSynth.mix() + self.ifft_signal
        # return self.ifft_signal
        # return self.hSynth.mix()

def test():
    import pyaudio
    SR = 22050
    PAGE_LEN = 1024
    hySynth = HybridSynth(3, SR, PAGE_LEN, np.float32)
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format = pyaudio.paFloat32, channels = 1, rate = SR, 
        output = True, frames_per_buffer = PAGE_LEN,
    )
    while True:
        # h = [Harmonic(f, 0) for f in range(220, SR, 220)]
        h = [Harmonic(f, .0005) for f in range(220, round(SR/4), 220)]
        h[0] = Harmonic(220 * 1, .05)
        h[1] = Harmonic(220 * 2, .03)
        h[2] = Harmonic(220 * 3, .04)
        h[3] = Harmonic(220 * 4, .005)
        h[4] = Harmonic(220 * 5, .007)
        h[5] = Harmonic(220 * 6, .01)
        hySynth.eat(h)
        mixed = hySynth.mix()
        stream.write(mixed, PAGE_LEN)

if __name__ == '__main__':
    test()
