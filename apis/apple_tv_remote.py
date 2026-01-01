from dotenv import load_dotenv
from typing import Tuple
import subprocess
import os

load_dotenv()

remote_id = str(os.getenv("ATV_REMOTE_ID"))     # personal home remote id
base_remote_command = ['atvremote', '--id', remote_id]  # commonly used command for controlling Apple TV
app_dict = {} # dictionary to start apps installed on device

# Assigns virtual environment directory to use 'atvremote' command
venv_name = '../.venv/Scripts'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PATH = os.path.join(BASE_DIR, venv_name)

# returns list of applications installed on device
def get_app_list() -> Tuple[str, str]:
    command = base_remote_command + ['app_list']
    process = subprocess.Popen(command, cwd=VENV_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    return stdout, stderr

# fills 'app_dict' with applications retrieved from get_app_list
def add_app_dict():
    apps = get_app_list()[0].split(',')
    for app in apps:
        key = app.split(':')[1].strip()
        key = key.split('(')[0].strip()
        val = app.split('(')[1].strip()[:-1]
        app_dict[key] = val

# Checks if on/off then sends respective command
def turn_on_off():
    command = base_remote_command + ['power_state']
    process = subprocess.Popen(command, cwd=VENV_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    power = "turn_on"
    if 'on' in stdout.lower():
        power = "turn_off"

    command = base_remote_command + [power]
    subprocess.Popen(command, cwd=VENV_PATH)

# finds application url from app_dict and launches
def launch_app(app_name):
    if not bool(app_dict):
        add_app_dict()

    for app in app_dict:
        if app.lower() == app_name.lower():
            app_url = app_dict[app]

    command = base_remote_command + [f'launch_app={app_url}']
    subprocess.Popen(command, cwd=VENV_PATH)

# used for generic commands i.e up, down, select, etc.
def remote_command(command: str):
    full_command = base_remote_command + [command]
    subprocess.Popen(full_command, cwd=VENV_PATH)