'''
Synthesizes an audio page from a spectrum.  
'''
import numpy as np
from collections import namedtuple

Harmonic = namedtuple('Harmonic', ['freq', 'mag'])

class IfftSynth:
    def __init__(self, SR, PAGE_LEN):
        self.SR = SR
        self.PAGE_LEN = PAGE_LEN
        self.SPECTRUM_SIZE = (PAGE_LEN // 2 + 1, )
        self.last_power = 0

    def getPower(self, harmonics):
        return sum([h.mag for h in harmonics])

    def eat(self, harmonics):
        spectrum = np.zeros(self.SPECTRUM_SIZE)
        for freq, mag in harmonics:
            try:
                spectrum[round(
                    freq / self.SR * self.PAGE_LEN
                )] += mag
            except IndexError:
                continue
        signal = np.fft.irfft(spectrum) * self.PAGE_LEN
        power = self.getPower(harmonics)
        mask = np.linspace(self.last_power / power, 1, self.PAGE_LEN)
        self.last_power = power
        return signal * mask * 2
        # For some reason you need a "* 2" 
