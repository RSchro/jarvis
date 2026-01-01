import apis.locks as lock

lock_unlock_door_dec = {
    "name": "lock_unlock_door",
    "description": "Locks or unlocks a door",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "lock_state": { "type": "STRING", "description": "'Lock' or 'Unlock'" },
            "location": { "type": "STRING", "description": "Where the lock is located, case-sensitive. Example: Main House, Guest House, Office."},
            "lock_name": { "type": "STRING", "description": "The name of the lock. Example: 'Front Door', 'Back Door'"}
        },
        "required": ["lock_state", "location", "lock_name"]
    }
}

get_lock_info_dec = {
    "name": "get_lock_info",
    "description": "Gets information about a lock. Returns a dictionary.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "location" : { "type" : "STRING", "description" : "Where the lock is located, case-sensitive. Example: Main House, Guest House, Office."},
            "lock_name": { "type": "STRING", "description" : "The name of the lock. Example: 'Front Door', 'Back Door'"},
            "locked": {"type": "STRING", "description" : "True if door is locked. False if unlocked."},
            "online": {"type": "STRING", "description" : "True if door is online and connected. False if not connected."},
            "battery_level": {"type": "STRING", "description" : "The battery level of the lock. Example: 0.915 for 91.5%."},
        },
        "required": ["location", "lock_name"]
    }
}

def lock_unlock_door(lock_state : str, location: str, lock_name: str):
    try:
        device_id = lock.fetch_device(location, lock_name).device_id

        if lock_state.lower() == "unlock":
            lock.unlock_door(device_id)
        elif lock_state.lower() == "lock":
            lock.lock_door(device_id)
        return {"status": "success", "message": f"Door {lock_state}ed"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def get_lock_info(location : str, lock_name: str) -> dict | None:
    try:
        device = lock.get_device_info(location, lock_name)
        if not device:
            return {"status": "error", "message": "Could not retrieve device information."}
        return {"locked": str(device["locked"]), "online": str(device["online"]), "battery_level": str(device["battery_level"])}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}