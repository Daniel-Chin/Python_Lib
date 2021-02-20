print('importing...')
import pyaudio
from time import time, sleep
import numpy as np
import scipy
from scipy import stats
from threading import Lock
from collections import namedtuple
import wave
import random
try:
    from interactive import listen
    from yin import yin
    from streamProfiler import StreamProfiler
    from harmonicSynth import HarmonicSynth, Harmonic
except ImportError as e:
    module_name = str(e).split('No module named ', 1)[1].strip().strip('"\'')
    print(f'Missing module {module_name}. Please download at')
    print(f'https://github.com/Daniel-Chin/Python_Lib/blob/master/{module_name}.py')
    input('Press Enter to quit...')
    raise e

print('Preparing...')
PAGE_LEN = 1024
N_HARMONICS = 20
DO_SWIPE = True
DO_PROFILE = True
# WRITE_FILE = None
WRITE_FILE = f'demo_{random.randint(0, 99999)}.wav'

MASTER_VOLUME = 1
SR = 22050
DTYPE = (np.int32, pyaudio.paInt32)
TWO_PI = np.pi * 2
HANN = scipy.signal.get_window('hann', PAGE_LEN, True)
PAGE_TIME = 1 / SR * PAGE_LEN
IMAGINARY_LADDER = np.linspace(0, TWO_PI * 1j, PAGE_LEN)

streamOutContainer = []
terminate_flag = 0
terminateLock = Lock()
profiler = StreamProfiler(PAGE_LEN / SR, DO_PROFILE)

if DO_PROFILE:
    _print = print
    def print(*a, **k):
        _print()
        _print(*a, **k)

def main():
    global terminate_flag, f, synth
    print('Press ESC to quit. ')
    terminateLock.acquire()
    synth = HarmonicSynth(N_HARMONICS, SR, PAGE_LEN, DTYPE[0], True, DO_SWIPE, .3)
    pa = pyaudio.PyAudio()
    streamOutContainer.append(pa.open(
        format = DTYPE[1], channels = 1, rate = SR, 
        output = True, frames_per_buffer = PAGE_LEN,
    ))
    if WRITE_FILE is not None:
        f = wave.open(WRITE_FILE, 'wb')
        f.setnchannels(1)
        f.setsampwidth(4)
        f.setframerate(SR)
    streamIn = pa.open(
        format = DTYPE[1], channels = 1, rate = SR, 
        input = True, frames_per_buffer = PAGE_LEN,
        stream_callback = onAudioIn, 
    )
    streamIn.start_stream()
    try:
        while streamIn.is_active():
            op = listen(b'\x1b', priorize_esc_or_arrow=True)
            if op == b'\x1b':
                print('Esc received. Shutting down. ')
                break
    except KeyboardInterrupt:
        print('Ctrl+C received. Shutting down. ')
    finally:
        print('Releasing resources... ')
        terminate_flag = 1
        terminateLock.acquire()
        terminateLock.release()
        streamOutContainer[0].stop_stream()
        streamOutContainer[0].close()
        if WRITE_FILE is not None:
            f.close()
        while streamIn.is_active():
            sleep(.1)   # not perfect
        streamIn.stop_stream()
        streamIn.close()
        pa.terminate()
        print('Resources released. ')

def sft(signal, freq_bin):
    # Slow Fourier Transform
    return np.abs(np.sum(signal * np.exp(IMAGINARY_LADDER * freq_bin))) / PAGE_LEN

def onAudioIn(in_data, sample_count, *_):
    global terminate_flag

    try:
        if terminate_flag == 1:
            terminate_flag = 2
            terminateLock.release()
            print('PA handler terminating. ')
            # Sadly, there is no way to notify main thread after returning. 
            return (None, pyaudio.paComplete)

        if sample_count > PAGE_LEN:
            print('Discarding audio page!')
            in_data = in_data[-PAGE_LEN:]

        profiler.gonna('typing')
        page = np.frombuffer(
            in_data, dtype = DTYPE[0]
        )

        profiler.gonna('yin')
        f0 = yin(page * HANN, SR, PAGE_LEN)
        # pitch = np.log(f0) * 17.312340490667562

        profiler.gonna('sft')
        harmonics = []
        for i in range(1, N_HARMONICS + 1):
            freq = f0 * i
            harmonics.append(Harmonic(
                freq, 
                sft(page * HANN, freq * PAGE_LEN / SR)
            ))
        
        profiler.gonna('eat')
        synth.eat(harmonics)

        profiler.gonna('mix')
        mixed = synth.mix()
        streamOutContainer[0].write(mixed, PAGE_LEN)
        if WRITE_FILE is not None:
            f.writeframes(mixed)

        profiler.display(same_line=True)
        profiler.gonna('idle')
        return (None, pyaudio.paContinue)
    except:
        terminateLock.release()
        import traceback
        traceback.print_exc()
        return (None, pyaudio.paAbort)

main()
