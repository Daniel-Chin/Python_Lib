'''
Light-weight wav player. 
'''
import sys
import simpleaudio as sa
from os import path

try:
    if path.isfile(sys.argv[1]):
        sa.WaveObject.from_wave_read(sa.wave.open(sys.argv[1])).play()
    else:
        input('File doesn\'t exist. ')
except IndexError:
    input('Please open a file with this app. ')
input('Enter to quit...')
sys.exit(0)
