#
# Author: dextor@gmail.com
# Script to control a headless Raspbery PI running mpd using a GPIO Keypad
# Can tell the current song using TTS
#
from pad4pi import rpi_gpio
from mpd import MPDClient
from multiprocessing import Process
from threading import Thread
import os
import time

client = MPDClient()
host = 'localhost'

KEYPAD = [
    [1, 2],
    [3, 4],
]

# BCM Pins
ROW_PINS = [26, 20]
COL_PINS = [19, 16]


def handleKey(key):
    connect()
    if(key == 1):
        song = client.currentsong()
        if(song):
            time.sleep(1)
            say('This song is {0} by {1} from {2}. Enjoy!'.format(
                song['title'], song['artist'], song['date']))
        else:
            say('Nothig')
    if(key == 2):
        client.pause()
        out = client.status()
        say(out['state'])
    if(key == 3):
        say('Next.')
        client.next()
    if(key == 4):
        say('Play.')
        client.play()


def say(message):
    print(message)
    client.volume(-10)
    os.system('echo "{0}" | festival --tts'.format(message))
    client.volume(10)


def execute(command):
    out = check_output(command)
    return out.decode('utf-8').strip()


def connect():
    connected = False
    status = None
    try:
        client.status()
        connected = True
    except:
        print('Not connected')

    while connected == False:
        try:
            print('Connecting', host)
            client.timeout = None
            client.idletimeout = None
            client.connect(host, 6600)
            connected = True
        except:
            time.sleep(1)


def checkchanges():
    idleclient = MPDClient()
    idleclient.connect(host, 6600)
    while True:
        result = idleclient.idle('player')
        status = idleclient.status()
        if(status['state'] == 'play'):
            song = client.currentsong()
            say(song['artist'])


connect()
client.stop()
say('MusicBox is Ready.')
client.play()
#t1 = Thread(target=checkchanges)
#t1.setDaemon(True)
#t1.start()

try:
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(
        keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

    keypad.registerKeyPressHandler(handleKey)

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('Goodbye')
finally:
    keypad.cleanup()
    client.close()
