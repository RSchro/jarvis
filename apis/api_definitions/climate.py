from dotenv import load_dotenv
import subprocess
import os

load_dotenv()

unit_id = os.getenv("AC_UNIT_IP")
BASE_COMMAND = ['msmart-ng', 'control', unit_id, '--auto']

# Assigns virtual environment directory to use 'msmart-ng' command
venv_name = '../../.venv/Scripts'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PATH = os.path.join(BASE_DIR, venv_name)

# Sets temperature --> Converts F temp to C temp
def set_temperature(temp : int):
    c_temp = round((temp - 32) * (5/9), 1)
    command = BASE_COMMAND + [f'target_temperature={c_temp}']
    subprocess.Popen(command, cwd=VENV_PATH)

# Turns power on/off
def power_on_off(power_mode : bool):
    command = BASE_COMMAND + [f'power_state={power_mode}']
    subprocess.Popen(command, cwd=VENV_PATH)

# Sets operation mode: heat, cool, auto, fan.
def set_mode(operation_mode : str):
    if operation_mode.lower() == "fan":
        operation_mode = "fan_only"
    command = BASE_COMMAND + [f'operational_mode={operation_mode.lower()}']
    subprocess.Popen(command, cwd=VENV_PATH)

# Sets swing mode on/off -- codes subject to midea-msmart
def swing_mode(swing_mode : bool):
    swing_code = '0x0'
    if swing_mode:
        swing_code = '0xC'
    command = BASE_COMMAND + [f'swing_mode={swing_code}']
    subprocess.Popen(command, cwd=VENV_PATH)

# Sets fan speed: full, high, medium, low, auto, or silent
def fan_speed(fan_speed : str):
    command = BASE_COMMAND + [f'fan_speed={fan_speed}']
    subprocess.Popen(command, cwd=VENV_PATH)