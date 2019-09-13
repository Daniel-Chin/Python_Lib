'''
Really tries to be safe against injection attacks.  
Intentionally uses single thread only.  
Only answers GET. Does not abide by request http header fields.  
Does not defend against DoS.  
'''
from socket import socket, timeout, gethostname, gethostbyname
from local_ip import getLocalIP
import logging
import os
from interactive import inputUntilValid
from time import asctime
import traceback
from io import StringIO

ESCAPE = '<log>\n'
ACCEPT_TIMEOUT = .005
HANDLE_TIMEOUT = .1
LISTEN = 1
TOP_SPEED = [2 * 1024 * 1024, '2 MB']
PAGE = int(ACCEPT_TIMEOUT * TOP_SPEED[0])

options = {
    'max_connections': (1, '"" if not x else int(x)', 'x == "" or x > 0'), 
    'port': (80, '"" if not x else int(x)', 'x == "" or x > 0'), 
}

def main(Handler, log_dir = None, **kw):
    '''
    `Handler` is a class that has the following methods:  
        __init__(self, request, sock, addr, time_out):  
            `log()` to write logs.  
        do(self):  
            Return 'wait', 'done', or 'close'.  
            Risk of spinlock: The main loop try-wait on do(). Do not do nothing and return 'wait'.  
        unlink(self):  
            called to release files.  
    '''
    initLog(log_dir)
    try:
        log('socket read is maxed at', PAGE // 1024, 'KB, allowing', TOP_SPEED[1], '/ s under ACCEPT_TIMEOUT =', ACCEPT_TIMEOUT, 's.')
        loadOptions(kw)
        serverSock = socket()
        serverSock.bind(('', options['port']))
        serverSock.listen(LISTEN)
        local_ip = getLocalIP
        if not local_ip:
            local_ip = [gethostname()]
            local_ip.append(gethostbyname(local_ip[0]))
        log('listening at', local_ip, '...')
        try:
            loop(serverSock, Handler)
        finally:
            force(serverSock.close)
        log('Exiting main().')
    except Exception as e:
        tempIO = StringIO()
        traceback.print_exc(file = tempIO)
        tempIO.seek(0)
        log(tempIO.read(), level = logging.ERROR)
        raise e

def initLog(log_dir):
    log_dir = log_dir or os.getcwd()
    log_filename = os.path.join(log_dir, asctime().replace(':', '_') + '.log')
    print('Log file will be at', log_filename)
    if inputUntilValid('Is that OK?', 'yn') != 'y':
        raise Exception('User chose to abort.')
    logging.basicConfig(format='%(asctime)s %(message)s', 
                    filename = log_filename)
    logging.root.setLevel(logging.NOTSET)

def log(*args, sep = ' ', end = '\n', flush = False, level = logging.INFO):
    text = sep.join([str(x) for x in args]) + end
    print(text, flush = flush, end = '')
    logging.log(level, text + ESCAPE)

def loadOptions(kw):
    print('Loading options...')
    for key, (default, legalize, validator) in [*options.items()]:
        try:
            options[key] = kw[key]
        except KeyError:
            print(f'`{key}` not provided. ENTER to default `{key} = {default}`.')
            options[key] = inputUntilValid('Otherwise, input value: ', lambda x: eval(validator), legalize = lambda x: eval(legalize))
            if options[key] == '':
                options[key] = default
    log('Launching with options: {', *[f'\n\t{k}\t: {v}' for k, v in options.items()], '\n}')

class Client:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.buffer = b''
        self.handler = None

def loop(serverSock, Handler):
    log('Starting main loop.')
    clients = []
    try:
        while True:
            # Single thread, try_wait logic
            if len(clients) < options['max_connections']:
                if all([x.handler is None for x in clients]):
                    serverSock.settimeout(5)
                else:
                    serverSock.settimeout(ACCEPT_TIMEOUT)
                try:
                    sock, addr = serverSock.accept()
                    assert ESCAPE not in addr
                    log(addr, 'Accepted. ')
                    clients.append(Client(sock, addr))
                    log('Now we have', len(clients), 'clients. ')
                    sock.settimeout(HANDLE_TIMEOUT)
                except timeout:
                    pass
            for i, client in [*reversed(enumerate(clients))]:
                if client.handler is None:
                    try:
                        recved = client.sock.recv(PAGE)
                        assert recved != b''
                    except Exception as e:
                        log(client.addr, 'Shutdown with exception', sanitize(str(e)))
                        unlink(clients, i)
                        continue
                    client.buffer += recved
                    splited = client.buffer.split(b'\r\n\r\n', 1)
                    if len(splited > 1):
                        byte_request, client.buffer = splited
                        request = Request(byte_request)
                        if request.valid:
                            log('Handling request from', client.addr, ':', sanitize(str(request)))
                            client.handler = Handler(request, client.sock, client.addr, HANDLE_TIMEOUT)
                        else:
                            unlink(clients, i)
                            continue
                result = client.handler.do()
                if result == 'done':
                    client.handler = None
                elif result == 'close':
                    log('Handler of', addr, 'demanded shutdown.')
                    unlink(clients, i)
                    continue
                elif result == 'wait':
                    pass
    finally:
        while clients:
            unlink(clients, 0)

def force(function):
    try:
        function()
    except Exception as e:
        log('`force` ignoring', e)

class Request:
    def __init__(self, segment):
        self.valid = False
        try:
            lines = segment.decode().split('\r\n')
        except UnicodeDecodeError:
            log('Request does not decode into str.')
            return
        try:
            parsing = lines.pop(0)
            (
                self.command, 
                self.target, 
                self.http_version, 
            ) = parsing.split(' ')
            if self.command != 'GET':
                parsing = sanitize(parsing, 'Escaped sequence found in request! ')
                log('Ignoring non-GET request:', parsing)
                return
            self.header_fields = {}
            for parsing in lines:
                kw, value = parsing.split(':', 1)
                self.header_fields[kw.strip(' ')] = value.strip(' ')
        except Exception as e:
            parsing = sanitize(parsing, 'Escaped sequence found in request! ')
            log('Request has bad line:', parsing, level = logging.ERROR)
            return
        self.valid = True
    
    def __str__(self):
        return self.command + ' ' + self.target

def sanitize(x, message):
    while ESCAPE in x:
        log(message + 'Sign of an attack!', level = logging.ERROR)
        x = x.replace(ESCAPE, '')
    return x

def unlink(clients, i):
    addr = clients[i].addr
    log('Closing', addr)
    force(clients[i].sock.close)
    clients[i].unlink()
    clients.pop(i)
    log(addr, 'Closed. ')

class BaseHandler:
    log = log
    
    def __init__(self, request, sock, addr, time_out):
        self.request = request
        self.sock = sock
        self.addr = addr
        self.time_out = time_out
    
    def do(self):
        '''
        Override this method
        '''
        data = b"What a shame! The programmer didn't override do()."
        self.respondHead(len(data))
        self.sock.send(data)
        return 'close'

    def respondHead(self, content_length, content_type = 'text/html'):
        response = f'''HTTP/1.1 200 OK\r
Content-Length: {content_length}\r
Content-Type: {content_type}\r\n\r\n'''
        self.sock.send(response.encode())

if __name__ == '__main__':
    main(print)
