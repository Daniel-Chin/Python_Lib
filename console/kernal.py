'''
For a clean namespace.
'''
def Kernal(namespace = {}):
    from os import system as cmd
    from pprint import pprint
    from interactive import cls
    
    if namespace:
        for name in namespace:
            if not name.startswith('_'):
                exec(f'{name}=namespace["{name}"]')
        del name
    del namespace
    while True:
        try:
            try:
                __command = yield
            except GeneratorExit:
                return
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
        print(kernal.send(input('>> ')))
        next(kernal)
