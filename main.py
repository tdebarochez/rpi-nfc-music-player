from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import subprocess
import time
import json

with open('playlists.json', 'r') as f:
    playlists = json.load(f)

def getPlaylist(x):
    # return {
    #     '4b0101000408049e017581': 'Chill Bump'
    # }.get(x, 'not-found')
    return playlists.get(x, 'not-found')

print("Load ", playlists)

pn532 = Pn532_i2c()
pn532.SAMconfigure()

print("Waiting for nfc card presentation...")

while True:
  card_data = pn532.read_mifare().get_data()
  nfc_card_id = bytes(card_data).hex()
  playlist = getPlaylist(nfc_card_id)
  if playlist == 'not-found':
    print("No playlist found for " + nfc_card_id)
  else:
    subprocess.call(['mpc', 'stop']);
    subprocess.call(['mpc', 'clear']);
    subprocess.call(['mpc', 'load', playlist]);
    subprocess.call(['mpc', 'play']);
    time.sleep(3)
