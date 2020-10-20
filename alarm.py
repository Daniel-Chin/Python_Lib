'''
An alarm clock because the Win10 Alarm App HCI is trash.  
'''
import datetime as dt
from time import sleep
from winsound import Beep

def main():
  h = int(input('Hour (24h): '))
  m = int(input('Minute: '))
  target = dt.datetime.combine(dt.date.today(), dt.time(h, m, 0))
  now = dt.datetime.now
  delta = target - now()
  print('target', target)
  print('now', now())
  print('delta', delta)

  beep()
  while input('Can you hear the sound now? y/n >').lower() != 'y':
    beep()

  print('Alarm is ticking...')
  while delta.days >= 0:
    sleep(max(.1, min(60, delta.seconds * .9)))
    delta = target - now()
  
  beep()
  input('Alarm!!! Enter...')

def beep():
  Beep(440, 300)
  Beep(880, 300)
  Beep(440, 300)
  Beep(880, 300)
  Beep(440, 300)
  Beep(880, 300)

main()
