'''
Does requests_futures interrupt the sockets on exit?  
Conclusion: No. There seems no magic.  
'''

from __future__ import annotations

from typing import *
from time import sleep
import concurrent.futures as futures
from requests import Response

from requests_futures.sessions import FuturesSession

with FuturesSession(max_workers=1) as session:
    while True:
        print('starting req...')
        f: futures.Future[Response] = session.get(
            # 'https://www.google.com', 
            'http://localhost', 
            headers = {
                'Host': 'www.google.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.google.com/',
                'Origin': 'https://www.google.com',
                'Connection': 'keep-alive',
                'TE': 'Trailers',
            }, 
        )
        try:
            futures.wait([f])
        except KeyboardInterrupt:
            break
        response = f.result()
        print(response.text[:64])
        sleep(1)

print('session closed.')
