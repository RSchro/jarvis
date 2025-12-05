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