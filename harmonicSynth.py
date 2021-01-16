'''
Synthesize sound with harmonics.  
Interpolate between frames smartly.  
'''
import numpy as np
from collections import namedtuple

TWO_PI = np.pi * 2

Harmonic = namedtuple('Harmonic', ['freq', 'mag'])

class HarmonicSynth:
    def __init__(
        self, n_harmonics, SR, PAGE_LEN, DTYPE, 
        STUPID_MATCH, DO_SWIPE, CROSSFADE_RATIO, 
    ):
        self.PAGE_LEN = PAGE_LEN
        self.STUPID_MATCH = STUPID_MATCH
        self.DO_SWIPE = DO_SWIPE
        self.SR = SR
        self.CROSSFADE_LEN = round(CROSSFADE_RATIO * PAGE_LEN)
        self.SUSTAIN_ONES = np.ones((PAGE_LEN - self.CROSSFADE_LEN, ))
        self.n_harmonics = n_harmonics

        self.signal_2d = np.zeros((n_harmonics, PAGE_LEN), DTYPE)
        self.harmonics = [
            Harmonic(261.63, 0) for i in range(n_harmonics)
        ]
        self.osc = [Osc(
            i, self, h
        ) for i, h in enumerate(self.harmonics)]
    
    def mix(self):
        return np.sum(self.signal_2d, 0)
    
    def getMag(self, harmonic):
        return harmonic.mag

    def eat(self, harmonics):
        assert len(harmonics) >= self.n_harmonics
        harmonics.sort(key=self.getMag)
        # print(*[
        #     format(x, '4.0f') for x, _ in harmonics
        # ])
        if self.STUPID_MATCH:
            [osc.eat(*h, self.DO_SWIPE) for osc, h in zip(self.osc, harmonics)]
        else:
            unmatched_log_f = [
                np.log(freq)
                for freq, _ in harmonics
            ]
            unmatched = harmonics[:]
            harmonics = []
            # for i, ((freq, _), osc) in enumerate(zip(self.harmonics, self.osc)):
            for (freq, _), osc in zip(self.harmonics, self.osc):
                log_freq = np.log(freq)
                i_max = np.argmax(- np.abs(np.array(unmatched_log_f) - log_freq))
                loss = abs(log_freq - unmatched_log_f.pop(i_max))
                swipe_this = loss < .006
                # swipe_this = True
                # swipe_this = i_max < 3
                # print(format(loss, '6.3f'), end = '')
                harmonics.append(unmatched.pop(i_max))
                osc.eat(
                    *harmonics[-1], 
                    swipe = self.DO_SWIPE and swipe_this, 
                )
            print()
        self.harmonics = harmonics

class Osc():
    def __init__(self, i, synth, harmonic):
        self.LINEAR = np.arange(synth.PAGE_LEN + 1) * TWO_PI / synth.SR
        self.freq = harmonic.freq
        self.mag = harmonic.mag
        self.phase = 0
        self.i = i
        self.synth = synth
    
    def eat(self, new_freq, new_mag, swipe = True):
        if swipe:
            # print('swipe', end='')
            tau = self.LINEAR * np.linspace(
                self.freq, (new_freq + self.freq) * .5, self.synth.PAGE_LEN + 1
            )
            # mask = np.exp(np.linspace(np.log(self.mag + .0001), np.log(new_mag + .0001), self.synth.PAGE_LEN))
            if new_mag > self.mag:
                mask = np.concatenate((
                    self.synth.SUSTAIN_ONES * self.mag, 
                    np.exp(np.linspace(np.log(self.mag + .0001), np.log(new_mag + .0001), self.synth.CROSSFADE_LEN)), 
                ))
            else:
                mask = np.concatenate((
                    np.exp(np.linspace(np.log(self.mag + .0001), np.log(new_mag + .0001), self.synth.CROSSFADE_LEN)), 
                    self.synth.SUSTAIN_ONES * new_mag, 
                ))
        else:
            tau = self.LINEAR * new_freq
            mask = np.concatenate((
                np.exp(np.linspace(np.log(self.mag + .0001), np.log(new_mag + .0001), self.synth.CROSSFADE_LEN)), 
                self.synth.SUSTAIN_ONES * new_mag, 
            ))
        self.synth.signal_2d[self.i] = np.sin(
            tau[:-1] + self.phase
        ) * mask
        self.freq = new_freq
        self.mag = new_mag
        self.phase = (tau[-1] + self.phase) % TWO_PI
