import sys
import subprocess
import os
import requests
import fnmatch
from datetime import datetime as dt
from dotenv import load_dotenv
import db.database as db

load_dotenv()

# -- Declares the functions for Jarvis to recognize --
create_folder_dec = {
            "name": "create_folder",
            "description": "Creates a new folder at the specified path relative to the script's root directory.",
            "parameters": {
                "type": "OBJECT",
                "properties": { "folder_path": { "type": "STRING", "description": "The path for the new folder (e.g., 'new_project/assets')."}},
                "required": ["folder_path"]
            }
        }

create_file_dec = {
            "name": "create_file",
            "description": "Creates a new file with specified content at a given path.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "file_path": { "type": "STRING", "description": "The path for the new file (e.g., 'new_project/notes.txt')."},
                    "content": { "type": "STRING", "description": "The content to write into the new file."}
                },
                "required": ["file_path", "content"]
            }
        }

edit_file_dec = {
            "name": "edit_file",
            "description": "Appends content to an existing file at a specified path.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "file_path": { "type": "STRING", "description": "The path of the file to edit (e.g., 'project/notes.txt')."},
                    "content": { "type": "STRING", "description": "The content to append to the file."}
                },
                "required": ["file_path", "content"]
            }
        }

open_application_dec = {
            "name": "open_application",
            "description": "Opens or launches a desktop application on the user's computer.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "application_name": { "type": "STRING", "description": "The name of the application to open (e.g., 'Notepad', 'Calculator', 'Chrome')."}
                },
                "required": ["application_name"]
            }
        }

get_weather_dec = {
    "name": "get_weather",
    "description": "Gets weather using a given location",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "location": {"type": "STRING", "description": "The requested location to obtain weather"},
            "high": {"type": "STRING", "description": "The high weather"},
            "low": {"type": "STRING", "description": "The low weather"},
            "curr_temp": { "type": "string", "description": "The current temp"},
        },
        "required": ["location"]
    }
}

get_local_time_dec = {
    "name": "get_local_time",
    "description": "Gets the local time",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "time": {"type": "STRING", "description": "The requested time"},
        },
        "required": []
    }
}


def create_folder(folder_path):
    """Creates a folder at the specified path and returns a status dictionary."""
    try:
        if not folder_path or not isinstance(folder_path, str): return {"status": "error",
                                                                        "message": "Invalid folder path provided."}
        if os.path.exists(folder_path): return {"status": "skipped",
                                                "message": f"The folder '{folder_path}' already exists."}
        os.makedirs(folder_path)
        return {"status": "success", "message": f"Successfully created the folder at '{folder_path}'."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def create_file(file_path, content):
    """Creates a file at the specified path"""
    try:
        if not file_path or not isinstance(file_path, str): return {"status": "error",
                                                                    "message": "Invalid file path provided."}
        if os.path.exists(file_path): return {"status": "skipped",
                                              "message": f"The file '{file_path}' already exists."}
        with open(file_path, 'w') as f:
            f.write(content)
        return {"status": "success", "message": f"Successfully created the file at '{file_path}'."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred while creating the file: {str(e)}"}

def edit_file( file_path, content):
    try:
        if not file_path or not isinstance(file_path, str): return {"status": "error",
                                                                    "message": "Invalid file path provided."}
        if not os.path.exists(file_path): return {"status": "error",
                                                  "message": f"The file '{file_path}' does not exist. Please create it first."}
        with open(file_path, 'a') as f:
            f.write(f"\n{content}")
        return {"status": "success", "message": f"Successfully appended content to the file at '{file_path}'."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred while editing the file: {str(e)}"}

def open_application(application_name):
    """Opens application requested by the user"""
    print(f">>> [DEBUG] Attempting to open application: '{application_name}'")
    try:
        if not application_name or not isinstance(application_name, str):
            return {"status": "error", "message": "Invalid application name provided."}
        command, shell_mode = [], False
        if sys.platform == "win32":
            app_map = {"calculator": "calc:", "notepad": "notepad", "chrome": "chrome", "google chrome": "chrome",
                       "firefox": "firefox", "explorer": "explorer", "file explorer": "explorer"}
            if application_name in app_map:
                app_command = app_map.get(application_name.lower(), application_name)
                command, shell_mode = f"start {app_command}", True
            else:
                print("Not in app_map")
                result = db.lookup_app_path(application_name)
                if result is not None:
                    print("Looking up application path")
                    command, shell_mode = f'start "" "{result}"', True
                else:
                    desktop_items = get_desktop_items()
                    filtered_items = fnmatch.filter(desktop_items, f"{application_name}*")
                    desk_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                    if application_name.lower() in filtered_items[0].lower():
                        print("Found desktop shortcut")
                        command, shell_mode = f'start {desk_path}\\{filtered_items[0]}', True


        elif sys.platform == "darwin":
            app_map = {"calculator": "Calculator", "chrome": "Google Chrome", "firefox": "Firefox", "finder": "Finder",
                       "textedit": "TextEdit"}
            app_name = app_map.get(application_name.lower(), application_name)
            command = ["open", "-a", app_name]
        else:
            command = [application_name.lower()]
        subprocess.Popen(command, shell=shell_mode)
        return {"status": "success", "message": f"Successfully launched '{application_name}'."}
    except FileNotFoundError:
        return {"status": "error", "message": f"Application '{application_name}' not found."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def get_desktop_items():
    desk_path = ""
    if os.name == 'nt':  # Windows
        desk_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    elif os.name == 'posix':  # macOS or Linux
        desk_path = os.path.expanduser('~/Desktop')
        try:
            desk_path = subprocess.check_output(['xdg-user-dir', 'DESKTOP']).decode().strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    desktop_items = os.listdir(desk_path)
    return desktop_items

def get_weather(location, units = "imperial"):
    """Obtains current weather from given location"""
    try:
        units = units
        formatted_location = location.replace(" ","%20").lower()
        formatted_location = formatted_location.replace(",", "%20")
        forecast_url = f"https://api.tomorrow.io/v4/weather/forecast?location={formatted_location}&timesteps=1d&units={units}&apikey={os.getenv('TOMORROWIO_API_KEY')}"
        realtime_url = f"https://api.tomorrow.io/v4/weather/realtime?location={formatted_location}&units={units}&apikey={os.getenv('TOMORROWIO_API_KEY')}"
        forecast = requests.get(forecast_url).json()
        realtime = requests.get(realtime_url).json()
        high = forecast["timelines"]["daily"][0]["values"]["temperatureMax"]
        low = forecast["timelines"]["daily"][0]["values"]["temperatureMin"]
        current = realtime["data"]["values"]["temperature"]
        return {"status": "success", "message": f"Successfully obtained weather from '{location}'.", "high": str(high),
            "low": str(low), "curr_temp": str(current)}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def get_lat_lon(location):
    """Obtains latitude and longitude from given location"""
    formatted_location=location.replace(" ", "%20")
    BASE_URL = f"http://api.openweathermap.org/geo/1.0/direct?q={formatted_location}&limit=5&appid={os.getenv("OPENWEATHER_API_KEY")}"
    response=requests.get(BASE_URL).json()
    lat = response[0]["lat"]
    lon = response[0]["lon"]
    return lat, lon

def get_local_time():
    """Gets local time"""
    try:
        now = dt.now()
        curr_time = now.time()
        formatted_time = curr_time.strftime('%I:%M %p')
        return {"status": "success", "message": f"Successfully obtained time'.", "time": str(formatted_time)}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"status": "error", "message": f"An error occurred: {str(e)}"}