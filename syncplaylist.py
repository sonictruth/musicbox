from mpd import MPDClient
from os import listdir
from os.path import isfile, isdir, join
import urllib.parse

host = 'localhost'
mediadir = '/home/pi/Music'

client = MPDClient()
client.connect(host, 6600)

playlistNames = [f for f in listdir(mediadir) if isdir(join(mediadir, f))]

for playlistName in playlistNames:
    client.playlistclear(playlistName)
    client.rm(playlistName)
    currentDir = mediadir + '/' + playlistName
    prefix = 'local:track:'
    print(prefix)
    files = [f for f in listdir(currentDir) if isfile(join(currentDir, f))]
    for file in files:
        item = prefix + urllib.parse.quote(playlistName + '/' + file, safe='/')
        print(item)
        client.playlistadd(playlistName, item)
