from .entries import entries
from local_ip import getLocalIP

def main():
    ips = getLocalIP()
    ips = [x for x in ips if not x.startswith('192.')]
    for ip in ips:
        try:
            print('Known IP:', ip, entries[ip])
        except KeyError:
            print('unknown IP:', ip)
    input('Enter...')

main()
