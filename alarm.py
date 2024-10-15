'''
An alarm clock because the Win10 Alarm App HCI is trash.  
Added support for linux because aur/timer doesn't support repeating until dismissed.
'''
import datetime as dt
from time import sleep
import chime

def main():
  chime.theme('zelda')

  while True:
    print('[a]: alarm mode. Give the target time.')
    print('[t]: timer mode. Give the duration.')
    op = input('> ').lower()
    if op in 'at':
      break
  
  now = dt.datetime.now

  if op == 'a':
    h = int(input('Hour (24h): '))
    m = int(input('Minute: '))
    target = dt.datetime.combine(dt.date.today(), dt.time(h, m, 0))
    delta = target - now()
  elif op == 't':
    dh = int(input('# of hours: '))
    dm = int(input('# of minutes: '))
    delta = dt.timedelta(hours=dh, minutes=dm)
    target = now() + delta
  print('target', target)
  print('now', now())
  print('delta', delta)

  chime.info()
  while input('Can you hear the sound now? y/n >').lower() != 'y':
    chime.info()

  print('Alarm is ticking...')
  while delta.days >= 0:
    sleep(max(.1, min(60, delta.seconds * .9)))
    delta = target - now()
  
  while True:
    try:
      print('Alarm!!! Ctrl+C to dismiss...')
      chime.info(sync=True)
      sleep(1)
    except KeyboardInterrupt:
      print('Alarm dismissed.')
      break

main()
