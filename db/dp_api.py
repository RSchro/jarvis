import db.database as db

insert_app_path_dec= {
    "name": "insert_app_path",
    "description": "Inserts an application path and its name into database",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "app_name": {"type": "STRING", "description": "The name of the application."},
            "app_path": {"type": "STRING", "description": "The path from the root to the application executable."},
        },
        "required": ["app_name", "app_path"]
    }
}

def insert_app(app_name, app_path):
    """Insert app path into table"""
    try:
        db.insert_app_path(app_name, app_path)
        return {"status": "success", "message": f"Successfully inserted path to {app_name}."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}