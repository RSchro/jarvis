import apis.apple_tv_remote as atv

# -- Declares the functions for Jarvis to recognize --
atv_on_off_dec = {
    "name": "atv_on_off",
    "description": "Turns on or off the apple tv.",
    "parameters": {
        "type": "OBJECT",
        "properties": {}
    }
}

launch_atv_app_dec = {
    "name": "launch_atv_app",
    "description": "Launches a specified app on Apple TV with specified name",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "app_name": { "type": "STRING", "description": "The name of the app to launch. Example: 'HBO Max, Disney+, Youtube'"},
        },
        "required": ["app_name"]
    }
}

apple_remote_command_dec = {
    "name": "send_remote_command",
    "description": "Send a remote command to the Apple TV",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "command": {"type": "STRING", "description": "The command to send. Example: play, pause, home, menu, left, right, up, down"},
        },
        "required": ["command"]
    }
}

def atv_on_off():
    """Turns on or off Apple TV"""
    try:
        atv.turn_on_off()
        return {"status": "success", "message": f"Successfully switched on/off Apple TV."}
    except Exception as e:
        print(str(e))
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def launch_atv_app(app_name: str):
    """Launches a specified app on Apple TV"""
    try:
        atv.launch_app(app_name)
        return {"status": "success", "message": f"Launched application '{app_name}' on Apple TV."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def send_remote_command(command: str):
    """Sends a remote command to Apple TV"""
    formatted_command = command.lower().replace(' ', '_')
    try:
        atv.remote_command(formatted_command)
        return {"status": "success", "message": f"Remote command '{formatted_command}' sent."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}