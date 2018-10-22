'''
Progress bar. 
'''
from time import time
from math import log

class _JdtAlreadyClosedError(BaseException):
    '''Cannot update Jdt after complete. '''

class _CannotDisplayMultiJdts(BaseException):
    pass

def smartUnit(size,is_speed=False):
    if size==0:
        return '   0  '
    if is_speed:
        magnitude=int(log(size,1024))
    else:
        magnitude=int(log(size/9,1024))
    magnitude=min(magnitude,3)
    return format(size/1024**magnitude,'4.0f')+ \
         {0:'B ',1:'KB',2:'MB',3:'GB'}[magnitude]

class CommJdt:
    '''
    msg [****____] 50% Total: 44MB Done: 22MB Speed: 1MB/s 
    '''
    occupied=False
    
    def __init__(self,goal,msg='',width=15):
        if self.__class__.occupied:
            raise _CannotDisplayMultiJdts
        self.__class__.occupied=True
        self.active=True
        self.width=width
        self.goal=goal
        self.msg=msg
        self.last_time=time()
        self.last_done=0

    def update(self,done):
        if not self.active:
            raise _JdtAlreadyClosedError
        dt=time()-self.last_time
        self.last_time=time()
        dd=done-self.last_done
        self.last_done=done
        if dt==0:
            speed=999999999
        else:
            speed=dd/dt
        
        progress=done/self.goal
        bar=int(self.width*progress)
        print('\r'+self.msg, \
              '['+'*'*bar+'_'*(self.width-bar)+']'+ \
              format(progress,'4.0%'), \
              'Total:',smartUnit(self.goal), \
              'Done:',smartUnit(done), \
              'Speed:',smartUnit(speed,is_speed=True)+'/s', \
              end='',flush=True)

    def complete(self):
        self.active=False
        self.__class__.occupied=False
        print('\r'+self.msg,'['+'#'*self.width+'] Complete! Total:', \
              smartUnit(self.goal),' '*22)

class Jdt:
    '''
    msg [****____] 50% Total: 44 Done: 22
    '''
    occupied=False
    
    def __init__(self,goal,msg='',width=32, UPP = 1):
        if self.__class__.occupied:
            raise _CannotDisplayMultiJdts
        self.__class__.occupied=True
        self.active=True
        self.width=width
        self.goal=goal
        self.msg=msg
        self.done = 0
        self.UPP = UPP
        self.UPP_count = 0
        # updates per print

    def update(self,done):
        if not self.active:
            raise _JdtAlreadyClosedError
        self.done = done
        self.UPP_count += 1
        if self.UPP_count == self.UPP:
            self.UPP_count = 0
        else:
            return
        progress=done/self.goal
        bar=int(self.width*progress)
        print('\r'+self.msg, \
              '['+'*'*bar+'_'*(self.width-bar)+']'+ \
              format(progress,'4.0%'), \
              'Total:',self.goal, \
              'Done:',done, \
              end='',flush=True)
    
    def acc(self):
        self.update(self.done + 1)
    
    def complete(self):
        self.active=False
        self.__class__.occupied=False
        print('\r'+self.msg,'['+'#'*self.width+'] Complete! Total:', \
              self.goal,' '*22)

if __name__=='__main__':
    from time import sleep
    j=CommJdt(10240000)
    for i in range(0,10240000,32345):
        j.update(i)
        sleep(0.01)
    j.complete()
    input('Enter..')
