'''
Scroll whatever you are reading with voice.  
'''
import pyaudio
from scipy import signal
import numpy as np
from time import sleep
import keyboard

DECAY = 10
CAP = 70
THRESHOLD = 50
SCROLL_COOLDOWN = .15

CHUNK = 1024
SAMPLE_FORMAT = pyaudio.paFloat32
CHANNELS = 2
FS = 44100  # Record at 44100 samples per second

SECOND_PER_CHUNK = CHUNK / FS
DECAY_PER_CHUNK = DECAY * SECOND_PER_CHUNK

def getPower(stream):
  data = stream.read(CHUNK)
  x = np.frombuffer(data)
  _, power = signal.periodogram(x, FS)
  return np.log(sum(power))

class Stream:
  def __init__(self, p):
    self.p = p
  
  def __enter__(self):
    self.s = self.p.open(format=SAMPLE_FORMAT,
      channels=CHANNELS,
      rate=FS,
      frames_per_buffer=CHUNK,
      input=True,
    )
    print('Recording...')
    return self.s
  
  def __exit__(self, a, b, c):
    self.s.stop_stream()
    self.s.close()
    print('Finished recording')

def main():
  room_power = getRoomPower()
  print('Room noise level =', room_power)
  input('Press Enter to start scrolling with voice...')
  WAIT = 1
  print(f'Wait {WAIT} seonds...')
  sleep(WAIT)
  print('You can now scroll with your voice!')
  acc = 0
  cooldown = 0
  with Stream(p) as stream:
    while True:
      cooldown -= SECOND_PER_CHUNK
      acc += getPower(stream) - room_power
      acc -= DECAY_PER_CHUNK
      acc = min(CAP, acc)
      acc = max(0, acc)
      if acc > THRESHOLD:
        if cooldown <= 0:
          scroll()
          cooldown = SCROLL_COOLDOWN

def getRoomPower():
  TIME = 3
  print(f'Record the room sound for {TIME} seconds.')
  print('Make regular noide during the process.')
  input('Press Enter...')
  WAIT = .5
  print(f'Wait {WAIT} seconds...')
  sleep(WAIT)
  n_chunks = int(TIME * FS / CHUNK)
  acc = 0
  with Stream(p) as stream:
    for i in range(n_chunks):
      acc += getPower(stream)
      print(f'{i} / {n_chunks}', end = '\r', flush = True)
  return acc / n_chunks

def scroll():
  keyboard.send('DOWN')

p = pyaudio.PyAudio()
try:
  main()
finally:
  p.terminate()
