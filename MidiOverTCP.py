'''
 -> LAN -> `Midi from TCP` as midi device ->  
'''
IP = '10'
PORT = 2350
VIRTUAL_DEVICE_NAME = 'Midi from TCP'
PAGE_SIZE = 4096

from time import sleep
import socket
import rtmidi

class Receiver:
    def __init__(self) -> None:
        self.midiOut = rtmidi.MidiOut()
        self.midiOut.open_virtual_port(VIRTUAL_DEVICE_NAME)

    def noteOn(self, pitch, velocity):
        # channel = 0
        self.midiOut.send_message([0x90, pitch, velocity])

    def noteOff(self, pitch):
        # channel = 0
        self.midiOut.send_message([0x80, pitch, 0])

    def pitchBend(self, x):
        # channel = 0
        self.midiOut.send_message([0xe0, x % 128, x // 128])

    def sendControllerChange(self, controller_number, value):
        # channel = 0
        self.midiOut.send_message([
            0xb0, controller_number, value, 
        ])

def receive():
    receiver = Receiver()
    print(f'''Opened virtual MIDI device "{
        VIRTUAL_DEVICE_NAME
    }".''')
    s = socket.socket()
    print(f'Connecting to {(IP, PORT)}...')
    s.connect((IP, PORT))
    s.settimeout(1)
    print('Established.')
    page = ''
    cursor = 0
    message = []
    try:
        while True:
            if cursor == len(page):
                try:
                    page = s.recv(PAGE_SIZE)
                except socket.timeout:
                    continue
                else:
                    cursor = 0
            else:
                message.append(page[cursor])
                cursor += 1
                if len(message) == 3:
                    receiver.midiOut.send_message(message)
                    print([hex(x) for x in message])
    except KeyboardInterrupt:
        print('Bye.')

def main():
    receive()

PORT_I = 0
def send():
    midiIn = rtmidi.MidiIn()
    ports = midiIn.get_ports()
    print('Available:')
    print(*enumerate(ports), sep='\n')
    print()
    print('Selected:')
    print(PORT_I)
    print(ports[PORT_I])
    print('Connecting...')
    midiIn.open_port(PORT_I)
    print('Success.')
    s = socket.socket()
    s.bind(('lcoalhost', PORT))
    s.listen(1)
    print('Server listening...')
    c, addr = s.accept()
    print('Incoming connection from', addr)
    midiIn.set_callback(onMidiIn, c)
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        midiIn.cancel_callback()
        midiIn.close_port()
        print('Bye.')

def onMidiIn(msg_dt, c):
    msg, _ = msg_dt
    assert len(msg) == 3
    c.send(bytes(msg))

main()
