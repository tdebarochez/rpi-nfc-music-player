from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import subprocess
import time
import json

with open('playlists.json', 'r') as f:
    playlists = json.load(f)

with open('urls.json', 'r') as f:
    urls = json.load(f)

def getPlaylist(x):
    return playlists.get(x, 'not-found')

def getUrl(x):
    return urls.get(x, 'not-found')

print("Load ", playlists, urls)

pn532 = Pn532_i2c()
pn532.SAMconfigure()

print("Waiting for nfc card presentation...")

while True:
  card_data = pn532.read_mifare().get_data()
  nfc_card_id = bytes(card_data).hex()
  playlist = getPlaylist(nfc_card_id)

  if playlist == 'not-found':
+    url = getUrl(nfc_card_id)
+    if url == 'not-found':
+      print("No playlist or url found for " + nfc_card_id)
+    else:
+      subprocess.call(['chromium-browser', '--disable-component-update', '--window-size=320,480', '--start-fullscreen', '--kiosk', '--noerrdialogs', '--disable-translate', '--no-first-run', '--fast', '--fast-start', '--disable-infobars', '--disable-features=TranslateUI', '--force-device-scale-factor=0.65', url])
+      time.sleep(3)
  else:
    subprocess.call(['mpc', 'stop']);
    subprocess.call(['mpc', 'clear']);
    subprocess.call(['mpc', 'load', playlist]);
    subprocess.call(['mpc', 'play']);
    time.sleep(3)
