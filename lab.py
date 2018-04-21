from pickle_socket import PickleSocket
from io import BytesIO as IO
import socket
import pickle
print('S=serverSock, s=server, c=client, IO, pickle')
S=PickleSocket()
S.bind(('',2333))
S.listen(1)
c=PickleSocket()
c.connect(('127.0.0.1',2333))
s,addr=S.accept()
