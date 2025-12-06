import time
import pyautogui as pg
import apis.browser as br

# Play
def play_pause():
    time.sleep(0.5)
    pg.press("playpause")

# Skip
def skip():
    pg.press("nexttrack")

# Previous
def previous():
    pg.press("prevtrack")

# Searches Spotify
def spotify_play_song(query):
    time.sleep(0.5)
    pg.hotkey("ctrl", "k")
    time.sleep(0.2)
    pg.write(query)
    time.sleep(1)
    pg.press("enter")

# Searches and plays an artis on Spotify
def spotify_play_artist(artist):
    time.sleep(0.5)
    pg.hotkey("ctrl", "k")
    time.sleep(0.5)
    pg.write(artist)
    time.sleep(1)
    pg.hotkey("shift", "enter")