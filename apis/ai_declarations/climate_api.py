import apis.api_definitions.climate as climate

climate_power_dec = {
    "name": "set_climate_power",
    "description": "Turns on or off the climate (AC) controls.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "power_mode" : {"type": "STRING", "description": "Whether to turn on or off. Ex: On, Off"}
        },
        "required": ["power_mode"]
    }
}

set_temp_dec = {
    "name": "set_temp",
    "description": "Sets the temperature on the climate (AC) controls.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "temp": {"type": "INTEGER", "description": "The temperature in degrees Fahrenheit."},
        },
        "required": ["temp"]
    }
}

set_climate_mode_dec = {
    "name": "set_climate_mode",
    "description": "Sets the mode of the climate (AC) controls.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "op_mode": {"type": "STRING", "description": "The mode of the climate (AC). Ex: Heat, Cool, Auto, Fan"},
        },
        "required": ["op_mode"]
    }
}

swing_mode_dec = {
    "name": "set_swing_mode",
    "description": "Sets the mode of the climate (AC) controls.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "swing_mode": {"type": "STRING", "description": "Turns swing speed on or off. Example: On, Off"},
        },
        "required": ["swing_mode"]
    }
}

fan_speed_dec = {
    "name": "set_fan_speed",
    "description": "Sets the speed of the climate (AC) controls.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "fan_speed": {"type": "STRING", "description": "The speed to set the fan speed. Ex: Auto, Full, High, Medium, Low, Silent."},
        },
        "required": ["fan_speed"]
    }
}

def set_climate_power(power_mode : str):
    try:
        if power_mode.lower() == "on":
            power = True
        else:
            power = False
        climate.power_on_off(power)
        return {"status": "success", "message": f"Turned {power_mode} climate controls."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def set_temp(temp : int):
    try:
        climate.set_temperature(temp)
        return {"status": "success", "message": f"Setting temperature to {temp} degrees."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def set_climate_mode(op_mode : str):
    modes = ["cool", "fan", "auto", "heat"]
    if op_mode.lower() not in modes:
        return {"status": "error", "message": f"Mode '{op_mode}' not supported."}
    try:
        climate.set_mode(op_mode)
        return {"status": "success", "message": f"Setting mode to {op_mode}."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def set_swing_mode(swing_mode : str):
    if swing_mode.lower() == "on":
        swing_mode = True
    else:
        swing_mode = False
    try:
        climate.swing_mode(swing_mode)
        return {"status": "success", "message": f"Setting swing mode to {swing_mode}."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def set_fan_speed(fan_speed : str):
    speeds = ["auto", "full", "high", "medium", "low", "silent"]
    if fan_speed.lower() not in speeds:
        return {"status": "error", "message": f"Fan speed not supported."}
    fan_speed = fan_speed.lower()
    fan_speed = fan_speed.capitalize()
    try:
        climate.fan_speed(fan_speed)
        return {"status": "success", "message": f"Fan speed set to {fan_speed}."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}