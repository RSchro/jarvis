from typing import Any
from seam import Seam
from dotenv import load_dotenv
import requests

load_dotenv()

# Creates Seam object to find and list locks
seam = Seam()
all_locks = seam.locks.list()

# Unlocks door given an id
def unlock_door(device_id : str):
    seam.locks.unlock_door(device_id = device_id)
    updated_lock = seam.locks.get(device_id = device_id)
    assert updated_lock.properties['locked'] is False

# Locks door given an id
def lock_door(device_id : str):
    seam.locks.lock_door(device_id = device_id)
    updated_lock = seam.locks.get(device_id=device_id)
    assert updated_lock.properties['locked'] is True

# Finds device information using device location and name; example: "Main House", "Front Door"
def fetch_device(device_location : str, device_name : str) -> Any | None:
    for lock in all_locks:
        if lock.location['location_name'] == device_location and lock.properties['name'] == device_name:
            return lock
    return None

def get_device_info(device_location : str, device_name : str) -> dict | None:
    device = fetch_device(device_location , device_name).properties
    return device