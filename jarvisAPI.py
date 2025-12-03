
# -- Declares the functions for Jarvis to recognize --
double_num = {
            "name": "double_num",
            "description": "Doubles a number using the given input",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "number": {
                        "type": "INTEGER",
                        "description": "The input variable to be doubled."
                    }
                },
                "required": ["number"]
            }
        }


# -- Defines the functions for Jarvis to use --
def double_num_func(num: int):
    """Doubles the input number"""
    result = num*2
    return {"status": "success", "message": f"Successfully doubled '{result}'.", "num": result}