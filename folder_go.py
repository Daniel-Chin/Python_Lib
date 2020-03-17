'''
To transmit a folder over the internet.  
Can continue on half-done job. Auto retry.  
Does not include subfolders.  
'''

PORT = 2346
HANDSHAKE_MSG = 'FOLDER GO'

import os
from os.path import isfile
from mysocket import recvFile, sendFileJdt, pair, shipFile
from pickle_socket import PickleSocket
from myfile import hashFile
from time import sleep
import traceback
from interactive import inputChin

def session(role = None, ip = None):
  '''
  `ip` = target ip for client  
  `ip` = trusted ip for server  
  '''
  if role is None:
    role, s, ip = pair(PORT, host_ip='')
  else:
    if role == 's':
      ss = PickleSocket()
      while True:
        try:
          ss.bind(('', PORT))
          break
        except OSError as e:
          print(e)
      ss.listen(1)
      s, addr = ss.accept()
      if addr[0] == ip:
        s.shakeHands(HANDSHAKE_MSG)
      else:
        s.close()
        ss.close()
        session(role, ip)
        return
    elif role == 'c':
      s = PickleSocket()
      s.connect((ip, PORT))
      s.shakeHands(HANDSHAKE_MSG)
  
  try:
    dir_diff = computeDirDiff(role, s)

    print("Today's tasks:")
    print(*dir_diff, sep='\n')
    print()

    for i, filename in enumerate(dir_diff):
      print('File', i + 1, '/', len(dir_diff))
      shipFile(role.replace('c', 'r'), s, filename)
  except:
    print()
    traceback.print_exc()
    print('Retry...')
    sleep(1)
    session(role, ip)

def computeDirDiff(role, s:PickleSocket):
  list_dir = [x for x in os.listdir() if isfile(x)]
  if role == 'c':
    s.sendObj(len(list_dir))
    for filename in list_dir:
      s.sendObj(filename)
      s.sendObj(hashFile(filename))
    return s.recvObj()
  elif role == 's':
    already_good = []
    total = s.recvObj()
    for _ in range(total):
      filename = s.recvObj()
      my_hash = None
      if isfile(filename):
        my_hash = hashFile(filename)
      their_hash = s.recvObj()
      if my_hash is not None and their_hash == my_hash:
        already_good.append(filename)
    result = [x for x in list_dir if x not in already_good]
    s.sendObj(result)
    return result

def main():
  print('Welcome to Folder Go.')
  os.chdir(inputChin('Path = ', os.getcwd()))
  print('In here, there are', len(os.listdir()), 'items.')
  print('Warning: Some may be overwritten.')
  print()
  session()

if __name__ == '__main__':
  main()
