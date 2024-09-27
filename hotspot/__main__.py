'''
Opens a hotspot on linux.  
Deprecated in favor of linux-wifi-hotspot.  
'''

import os
from contextlib import contextmanager
from subprocess import Popen
from functools import lru_cache
import typing as tp
import re
import uuid
import argparse

import psutil

HOSTAPD = 'hostapd'
DNSMASQ = 'dnsmasq'

@lru_cache(1)
def interface():
    interfaces = psutil.net_if_addrs().keys()
    for name in interfaces:
        if 'wlan' in name:
            return name
    for name in interfaces:
        if 'wlp' in name:
            return name
    raise EnvironmentError('No wireless interface found.')

@lru_cache(1)
def workingDir():
    return os.path.dirname(os.path.realpath(__file__))

def tempFileName(identifier: str):
    return os.path.join(workingDir(), f'temp_{identifier}.conf')

def newSecureTempFile(identifier: str):
    fn = tempFileName(identifier)
    with open(fn, 'w') as f:
        f.write('dummy')
    os.chmod(fn, 0o600)
    return open(fn, 'w')

def writeHostapdConf(
    ssid: str, wpa_passphrase: str, conf: dict = {}, 
):
    DEFAULT = {
        'interface': interface(),
        'ssid': ssid,
        'wpa_passphrase': wpa_passphrase,
        'driver': 'nl80211',
        'hw_mode': 'g',
        'channel': 6,
        'wmm_enabled': 0,
        'auth_algs': 1,
        'wpa': 2,
        'wpa_key_mgmt': 'WPA-PSK',
        'rsn_pairwise': 'CCMP', 
    }
    c = {**DEFAULT, **conf}
    with newSecureTempFile(HOSTAPD) as f:
        for k, v in c.items():
            print(f'{k}={v}', file=f)

def writeDnsmasqConf(conf: dict = {}):
    DEFAULT = {
        'interface': interface(),
        'dhcp-range': '192.168.1.2,192.168.1.20,12h', 
    }
    c = {**DEFAULT, **conf}
    with newSecureTempFile(DNSMASQ) as f:
        for k, v in c.items():
            print(f'{k}={v}', file=f)

@contextmanager
def UnmanageNetwork():
    CONF_FILE = '/etc/NetworkManager/NetworkManager.conf'

    tag_open = '# >>> the following line(s) are automated by ' + os.path.realpath(__file__)
    tag_close = '# <<< end of automation by ' + os.path.realpath(__file__)
    block_content: tp.Dict[bool, str] = {}
    block_content[True] = '\n'.join([
        tag_open, 
        '[keyfile]', 
        'unmanaged-devices=interface-name:' + interface(), 
        tag_close, 
    ])
    block_content[False] = '\n'.join([
        tag_open, 
        '# ', 
        tag_close, 
    ])
    block_pattern = re.compile(rf"{tag_open}.*?{tag_close}", re.DOTALL)

    def setConf(from_old: bool, to_new: bool):
        uuid_ = str(uuid.uuid4())
        with open(CONF_FILE, 'r') as f:
            content = f.read()
        if re.search(block_pattern, content):
            if block_content[from_old] not in content:
                if block_content[not from_old] not in content:
                    raise ValueError('Conf file contains correct tags but its enclosed content is unrecognized.')
                if not from_old:
                    print('Hint: maybe another hotspot instance is running?')
                raise ValueError('Unexpected state of conf file.')
            re.sub(block_pattern, uuid_, content)
            assert not re.search(block_pattern, content), 'Multiple blocks found.'
            content = content.replace(uuid_, block_content[to_new])
        else:
            assert not from_old
            content = '\n'.join([
                content.strip(),
                '', 
                block_content[to_new], 
                '', 
            ])
        with open(CONF_FILE, 'w') as f:
            f.write(content)
    
    setConf(False, True)
    os.system('sudo systemctl restart NetworkManager')
    print('NetworkManager out of the way.')
    try:
        yield
    finally:
        setConf(True, False)
        os.system('sudo systemctl restart NetworkManager')
        print('NetworkManager restored.')

def main(
    ssid: str, wpa_passphrase: str, 
    hostapd_conf: dict = {},
    dnsmasq_conf: dict = {},
):
    if os.geteuid() != 0:
        print('Error: sudo required')
        return
    
    writeHostapdConf(ssid, wpa_passphrase, hostapd_conf)
    writeDnsmasqConf(dnsmasq_conf)
    with UnmanageNetwork():
        with Popen(['hostapd', tempFileName(HOSTAPD)]) as hostapd:
            os.system(f'sudo ip addr add 192.168.1.1/24 dev {interface()}')
            with Popen(['dnsmasq', '-C', tempFileName(DNSMASQ), '-d']) as dnsmasq:
                print('Hotspot running. Press ctrl+C to stop.')
                try:
                    dnsmasq.wait()
                except KeyboardInterrupt:
                    print('Quiting...')
                    dnsmasq.terminate()
                    dnsmasq.wait()
                else:
                    print('unexpected exit by dnsmasq')
            hostapd.terminate()
            hostapd.wait()

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('ssid', type=str)
    parser.add_argument('wpa_passphrase', type=str)
    args = parser.parse_args()
    return args.ssid, args.wpa_passphrase

if __name__ == '__main__':
    main(*parseArgs())
