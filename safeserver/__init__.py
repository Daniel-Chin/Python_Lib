from safe_http import main as safeMain, BaseHandler
import os
from os import path
from io import StringIO

def main():
    safeMain(Handler, log_dir = path.join(path.dirname(__file__), 'logs'))

class Handler(BaseHandler):
    def __init__(self, request, *args, **kw):
        super().__init__(request, *args, **kw)
        assert request.command == 'GET'
        if request.target == '/':
            self.file = StringIO()
            [f'<a href="/{x}">{x}</a><br />' for x in os.listdir() if path.isfile(x)]
            self.content_length

    def do(self):
        
