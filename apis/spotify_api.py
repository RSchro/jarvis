import time
import apis.spotify as spot
import apis.browser as br
import jarvisAPI as jpi

spotify_tools = ["play_pause_dec", "skip_dec", "previous_track_dec", "spotify_play_song_dec"]

play_pause_dec = {
    "name": "play_pause",
    "description": "Plays or pauses media"
}

skip_dec = {
    "name": "skip_track",
    "description": "Skip tracks"
}

previous_track_dec = {
    "name": "previous_track",
    "description": "Previous track"
}

spotify_play_song_dec = {
    "name": "spotify_play_song",
    "description": "Plays a song via Spotify application",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "song": {"type": "STRING", "description": "The song name the user requests."},
        }
    }
}

spotify_play_artist_dec = {
    "name": "spotify_play_artist",
    "description": "Plays an artist via Spotify application",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "artist": {"type": "STRING", "description": "The artist name the user requests."},
        }
    }
}

def play_pause():
    """Plays or pauses media"""
    try:
        spot.play_pause()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def skip_track():
    """Skip tracks"""
    try:
        spot.skip()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def previous_track():
    """Previous track"""
    try:
        spot.previous()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def spotify_play_song(song):
    """Play a song on spotify application"""
    try:
        jpi.open_application("spotify")
        time.sleep(3)
        br.swap_to_application("spotify")
        time.sleep(0.2)
        spot.play_song(song)
        return {"status": "success", "message": f"Playing {song}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def spotify_play_artist(artist):
    """Plays an artist on spotify application"""
    try:
        spot.play_pause()
        time.sleep(0.2)
        br.swap_to_application("spotify")
        time.sleep(0.2)
        spot.play_artist(artist)
        return {"status": "success", "message": f"Now playing: {artist} on Spotify"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}