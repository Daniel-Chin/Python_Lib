'''
This is to be imported. 
Class Beepher is like an IO wrapper. 
Beepher(raw, key)
'''
from math import sqrt
from io import BytesIO,TextIOWrapper
from listen import listen

class Machine:
    def __init__(self,key):
        self.fluctuator=10
        self.primes = [3, 4, 5, 7]
        # Make sure 7 < 11
        self.beeflength=int(len(key)/2)
        self.beef=[]
        for i in range(self.beeflength):
            self.beef.append((ord(key[2*i]  )%16)*16 +\
                              ord(key[2*i+1])%16 \
                            )

    def next(self):
        self.fluctuator += 1
        for ZuiXiao_SuYinShu in self.primes:
            if self.fluctuator % ZuiXiao_SuYinShu == 0:
                break
        else:
            ZuiXiao_SuYinShu = self.fluctuator
            self.primes.append(self.fluctuator)
        intnewbeef = (sum(self.beef) + ZuiXiao_SuYinShu) % 256
        self.beef.pop(0)
        self.beef.append(intnewbeef)
        return intnewbeef

def liu(raw,int_beef):
    return bytes([int.from_bytes(raw,"big") ^ int_beef])

def liu2(int_raw,int_beef):
    return bytes([int_raw ^ int_beef])

class Beepher:
    def askForKey():
        '''
        Windows only. 
        '''
        key=''
        op=b''
        while op != b'\r':
            if op==b'\x08':
                print('\rkey =',' '*len(key),end='')
                key=key[0:-1]
            else:
                key+=op.decode()
            print('\rkey =','*'*len(key),flush=True,end='')
            op=listen()
            while len(op)==2:
                op=listen()
        print('\rKey Inserted. ',' '*len(key))
        return key

    def __init__(self,thing,key,mode):
        '''
        mode can be 'r' or 'w'. 
        If key is None, askForKey will be called. 
        '''
        assert mode in ('r','w')
        self.mode=mode
        if mode=='r':
            self.raw=thing
        else:
            self.out=thing
        self.origin=thing.tell()
        assert type(thing) is not TextIOWrapper
        if key is None:
            key=self.askForKey()
        self.key=key
        self.machine=Machine(key)

    def __iter__(self):
        assert self.mode=='r'
        return self

    def __next__(self):
        read=self.raw.read(1)
        if read==b'':
            raise StopIteration
        else:
            return liu(read, self.machine.next())

    def read(self,size):
        assert self.mode=='r'
        b=b''
        for i in range(size):
            read=self.raw.read(1)
            if read==b'':
                break
            b+=liu(read,self.machine.next())
        return b

    def readline(self):
        assert self.mode=='r'
        b=b''
        for i in self:
            if i==b'\n':
                b+=b'\n'
                break
            b+=i
        return b

    def thing(self):
        if self.mode=='r':
            return self.raw
        else:
            return self.out

    def tell(self):
        return self.thing().tell()-self.origin

    def seek(self,pos):
        self.machine.__init__(self.key)
        for i in range(pos):
            self.machine.next()
        abso_pos=pos+self.origin
        return self.thing().seek(abso_pos)

    def write(self,buffer):
        assert self.mode=='w'
        for b in buffer:
            self.out.write(liu2(b,self.machine.next()))
