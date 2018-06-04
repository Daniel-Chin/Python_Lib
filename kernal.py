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
                result = eval(__command + '\r')
                if result is not None:
                    print(result)
                del result
            except SyntaxError:
                exec(__command + '\r')
        except:
            import traceback
            traceback.print_exc()
            del traceback

if __name__ == '__main__':
    kernal = Kernal({})
    next(kernal)
    while True:
        kernal.send(input('>> '))
