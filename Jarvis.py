from google import genai  # Imports the main Gemini AI library
from google.genai import types
from google.genai.types import ModelContent, Part, UserContent
import os  # Imports the 'os' module for system interactions
from dotenv import load_dotenv  # Imports a function to load environment variables from a .env file
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

# -- CUSTOM APIs --
import jarvisAPI as jpi
import db.dp_api as dbapi
import apis.browser_api as br
import apis.spotify_api as spt
import apis.emails_api as e
import apis.atv_api as atv
import apis.locks_api as lock
from apis.ansicolors import ANSIColors as ansi


# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
GEMINI_API = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API = os.getenv("ELEVENLABS_API_KEY")
MODEL = "gemini-2.5-flash"
VOICE_ID = 'iF0kaX7XTQPFLTjMlJL4'
USE_VOICE = False
MAX_OUTPUT_TOKENS = 500
SYSTEM_INSTRUCTIONS="""Your name is Jarvis, which stands for Just A Rather Very Intelligent System. 
            You are an Ai designed to help me with day to day task. Also keep replies short when plausible.
                You have access to tools for searching, code execution, and file system actions.
                1.  For information or questions, use `Google Search`.
                2.  For math or running python code, use `code_execution`.
                3.  If the user asks to create a directory or folder, you must use the `create_folder` function.
                4.  If the user asks to create a file with content, you must use the `create_file` function.
                5.  If the user asks to add to, append, or edit an existing file, you must use the `edit_file` function.
                Prioritize the most appropriate tool for the user's specific request."""

client = genai.Client(api_key=GEMINI_API)  # Creates a client instance for the Gemini API
tools = types.Tool(function_declarations=[jpi.welcome_home_dec, jpi.create_folder_dec, jpi.create_file_dec, jpi.edit_file_dec, jpi.open_application_dec, jpi.close_app_dec,
                                          jpi.get_weather_dec, jpi.get_local_time_dec, dbapi.insert_app_path_dec, dbapi.insert_web_search_url_dec, br.open_page_dec, br.search_page_dec,
                                          br.scroll_dec, spt.play_pause_dec, spt.skip_dec, spt.previous_track_dec, spt.spotify_play_song_dec, spt.spotify_play_artist_dec,
                                          dbapi.get_user_preferences_dec, e.count_emails_dec, e.print_emails_dec, e.delete_emails_dec, e.retrieve_email_dec, atv.atv_on_off_dec,
                                          atv.launch_atv_app_dec, atv.apple_remote_command_dec, lock.lock_unlock_door_dec, lock.get_lock_info_dec])

# Check if the key was loaded successfully
if not GEMINI_API:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

print(f"===> {ansi.BOLD}{ansi.CYAN}BOOTING JARVIS...{ansi.ENDC}")

history = [
    types.Content(
        role="user", parts=[types.Part(text="Occasionally call me Mr. Schroeder or sir, upon your preference. Only welcome me home if I tell you I've returned.")]
    )
]

config = types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTIONS, tools=[tools], max_output_tokens=MAX_OUTPUT_TOKENS)

# Generates client response and updates chat history -> checks for function call then handles differently
def send_message(user_input: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=history,
        config=config,
    )

    # True if model called a function
    fc = response.candidates[0].content.parts[0].function_call

    if fc:
        args, result = fc.args, {}

        if fc.name == "welcome_home":
            result = jpi.welcome_home()
        elif fc.name == "create_folder":
            result = jpi.create_folder(folder_path=("folder_path"))
        elif fc.name == "create_file":
            result = jpi.create_file(file_path=args.get("file_path"), content=args.get("content"))
        elif fc.name == "edit_file":
            result = jpi.edit_file(file_path=args.get("file_path"), content=args.get("content"))
        elif fc.name == "open_application":
            result = jpi.open_application(application_name=args.get("application_name"))
        elif fc.name == "close_application":
            result = jpi.close_application(application_name=args.get("application_name"))
        elif fc.name == "get_weather":
            location = args.get("location")
            result = jpi.get_weather(location)
        elif fc.name == "get_local_time":
            result = jpi.get_local_time()
        elif fc.name == "insert_app_path":
            app_name = args.get("app_name")
            app_path = args.get("app_path")
            result = dbapi.insert_app(app_name, app_path)
        elif fc.name == "insert_web_search_url":
            website = args.get("website")
            search_url = args.get("search_url")
            result = dbapi.insert_web_search_url(website, search_url)
        elif fc.name == "open_page_api":
            url_name = args.get("url")
            open_location = args.get("open_location")
            result = br.open_page_api(url_name, open_location)
        elif fc.name == "search_page_api":
            website = args.get("website")
            query = args.get("query")
            result = br.search_page_api(website, query)
        elif fc.name == "scroll_api":
            direction = args.get("direction")
            result = br.scroll_api(direction)
        elif fc.name == "play_pause":
            result = spt.play_pause()
        elif fc.name == "skip_track":
            result = spt.skip_track()
        elif fc.name == "previous_track":
            result = spt.previous_track()
        elif fc.name == "spotify_play_song":
            song = args.get("song")
            result = spt.spotify_play_song(song)
        elif fc.name == "spotify_play_artist":
            artist = args.get("artist")
            result = spt.spotify_play_artist(artist)
        elif fc.name == "count_emails":
            result = e.count_emails()
        elif fc.name == "print_emails":
            limit = args.get("limit")
            result = e.print_emails(limit)
        elif fc.name == "delete_mail":
            subject = args.get("subject")
            sender = args.get("sender")
            result = e.delete_mail(subject, sender)
        elif fc.name == "retrieve_email":
            email_idx = args.get("email_idx")
            result = e.retrieve_email(email_idx)
        elif fc.name == "atv_on_off":
            result = atv.atv_on_off()
        elif fc.name == "launch_atv_app":
            app_name = args.get("app_name")
            result = atv.launch_atv_app(app_name)
        elif fc.name == "send_remote_command":
            command = args.get("command")
            result = atv.send_remote_command(command)
        elif fc.name == "lock_unlock_door":
            lock_state = args.get("lock_state")
            location = args.get("location")
            lock_name = args.get("lock_name")
            result = lock.lock_unlock_door(lock_state, location, lock_name)
        elif fc.name == "get_lock_info":
            location = args.get("location")
            lock_name = args.get("lock_name")
            result = lock.get_lock_info(location, lock_name)

        fc_response = types.Part.from_function_response(
            name=fc.name,
            response={"result": result}
        )

        history.append(response.candidates[0].content)
        history.append(types.Content(role="user", parts=[fc_response]))
        final_response = client.models.generate_content(
            model=MODEL,
            contents=history,
            config=config,
        )
        return final_response.text

    return response.text

# Conversation loop --> "exit" to break
def main():
    elevenlabs = ElevenLabs(
        api_key=ELEVENLABS_API
    )
    initial_response = send_message("Reply to this with a greeting of your choice.")
    print(f"{ansi.BOLD}{ansi.BLUE}Jarvis:{ansi.ENDC} {initial_response}")
    while True:
        try:
            user_input = input(f"{ansi.BOLD}{ansi.GREEN}You:{ansi.ENDC} ")

            if user_input.lower() == "exit":
                break

            history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
            response = send_message(user_input)

            print(f"{ansi.BOLD}{ansi.BLUE}Jarvis:{ansi.ENDC} {response}")
            if USE_VOICE:
                audio = elevenlabs.text_to_speech.convert(

                    text=response,
                    voice_id=VOICE_ID,
                    model_id="eleven_flash_v2_5",
                    output_format="mp3_44100_128"
                )
                play(audio)

        except Exception as e:
            # Catch any exceptions and print an error message.
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()