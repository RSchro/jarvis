import subprocess

command = "start /wait python -W ignore Jarvis.py"
subprocess.call(command, shell=True)