import sys
import subprocess
import os
import requests
from dotenv import load_dotenv

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
            app_command = app_map.get(application_name.lower(), application_name)
            command, shell_mode = f"start {app_command}", True
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

def get_weather(location):
    """Obtains current weather from given location"""
    try:
        lat, lon = get_lat_lon(location)
        unit = "imperial"
        BASE_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={unit}&appid={str(os.getenv('OPENWEATHER_API_KEY'))}"
        response = requests.get(BASE_URL).json()
        high = response["main"]["temp_max"]
        low = response["main"]["temp_min"]
        curr_temp = response["main"]["temp"]
        print(f"High: {high}, Low: {low}, Current Temp: {curr_temp}")
        return {"status": "success", "message": f"Successfully obtained weather from '{location}'.", "high": str(high), "low": str(low), "curr_temp": str(curr_temp)}
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