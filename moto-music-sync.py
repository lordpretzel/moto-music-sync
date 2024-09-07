#!/usr/bin/env -S nix develop . --command python

"""
Sync music from Apple music playlist to Android device with adb
"""

__author__ = 'Boris Glavic'

import subprocess
import os
from tqdm import tqdm

MUSICDIR=os.path.expanduser("~/Music/iTunes/iTunes Media/Music/")
ANDROID_MUSIC_DIR="/storage/self/primary/Music/Music/"
ADB="adb"


def get_albums():
  scriptpath = os.path.expanduser('~/scripts/apple-scripts/syncMotoPlaylist.scpt')
  output = subprocess.check_output(['osascript', scriptpath])
  
  # Decode the output bytes to string
  result = output.decode('utf-8')
  return list(result.split('@ ')[0:-1])

def android_has_album(album):
  checker = ['/opt/homebrew/bin/adb', 'shell', 'ls', f'\"/storage/self/primary/Music/music/{album}\"', '1>/dev/null', '2>/dev/null','&&','echo',"1",'||','echo',"0"]
  output = subprocess.check_output(checker).decode('utf-8').strip()
  #print(output)
  return output == "1"
  
def sync_albums(albums):
  talbums = tqdm(albums)
  for a in talbums:
    talbums.set_description(f"syning {a}")
    print(f"check for album <{a}> ...")
    if not android_has_album(a):
      print(f"\t\t...does not exist, copy to {ANDROID_MUSIC_DIR}/{a}")
      copy_cmd = [ "adb", "push", f"{MUSICDIR}/{a}/", f"{ANDROID_MUSIC_DIR}/{a}" ]
      process = subprocess.run(copy_cmd, capture_output=True)
      if process.returncode:
        print(f"failed for album {a}, with {process.returncode} and\nSTDOUT:\n{process.stdout}\n\nSTDERR:\n{process.stderr}")
        
def main():
  album_paths = get_albums()
  sync_albums(album_paths)

if __name__ == '__main__':
  main()
