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

insert_web_search_dec = {
    "name": "insert_web_search",
    "description": "Inserts a website's url search query path by website name",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "website": {"type": "STRING", "description": "Name of the website."},
            "url_search": {"type": "STRING", "description": "URL search query path. Example: 'https://www.youtube.com/results?search_query='"},
        },
        "required": ["website", "url_search"]
    }
}

def insert_app(app_name, app_path):
    """Insert app path into table"""
    try:
        db.insert_app_path(app_name, app_path)
        return {"status": "success", "message": f"Successfully inserted path to {app_name}."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def insert_web_search(website, url_search):
    """Insert website's url search query path into table"""
    try:
        db.insert_url_search(website, url_search)
        return {"status": "success", "message": f"Successfully inserted path to {website}."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}