import time
import apis.spotify as spot
import apis.browser as br

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
            "query": {"type": "STRING", "description": "The song name the user requests."},
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

def spotify_play_song(query):
    """Play a song on spotify application"""
    try:
        time.sleep(2)
        br.swap_to_application("spotify")
        spot.spotify_play_song(query)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}