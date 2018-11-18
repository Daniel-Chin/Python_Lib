'''
For a clean namespace.
'''
def Kernal(namespace = {}):
    from os import system as cmd
    from pprint import pprint
    def cls():
        cmd('cls')
    
    if namespace:
        for name in namespace:
            if name[0] != '_':
                exec(name + '=namespace[\''+name+'\']')
        del name
    del namespace
    while True:
        try:
            __command = yield
            if __command == 'exit':
                return
            try:
                yield eval([__command + '\r', exec('del __command')][0])
                # Tries to hide `__command` in dir(). 
                # doesn't work tho. 
                # But you have to admit, it's a clever try. 
                continue
            except SyntaxError:
                pass
            exec(__command + '\r')
            yield None
        except:
            import traceback
            traceback.print_exc()
            del traceback
            yield None

if __name__ == '__main__':
    kernal = Kernal({})
    next(kernal)
    while True:
        kernal.send(input('>> '))
