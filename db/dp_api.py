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

insert_web_search_url_dec = {
    "name": "insert_web_search_url",
    "description": "Inserts a website's search url query path by website name",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "website": {"type": "STRING", "description": "Name of the website."},
            "search_url": {"type": "STRING", "description": "URL search path. Example: 'https://www.youtube.com/results?search_query='"},
        },
        "required": ["website", "search_url"]
    }
}

get_user_preferences_dec = {
    "name": "get_user_preferences",
    "description": "Gets user preferences from database",
    "parameters": {
    }
}

def insert_app(app_name, app_path):
    """Insert app path into table"""
    try:
        result = db.insert_app_path(app_name, app_path)
        return {"status": "success", "message": f"Successfully inserted path to {app_name}.", "preferences": result}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def insert_web_search_url(website, search_url):
    """Insert website's search url path into table"""
    try:
        db.insert_url_search(website, search_url)
        return {"status": "success", "message": f"Successfully inserted path to {website}."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}