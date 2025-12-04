import apis.browser as br

open_page_dec= {
    "name": "open_page_api",
    "description": "Opens web page on a browser",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "url": {"type": "STRING", "description": "What URL to open. Example: Youtube.com, Amazon.com, Wikipedia.org"},
            "open_location": {"type": "STRING", "description": "Where to open it. Example: tab, new window, same window. Enter 'tab' if no value is given."},
        },
        "required": ["url", "open_location"]
    }
}

search_page_dec = {
    "name": "search_page_api",
    "description": "Search web page on a browser",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "website": {"type": "STRING", "description": "The website to search on. Example: Youtube.com, youtube, Spotify.com"},
            "query": {"type": "STRING", "description": "The search query. Example: 'cat videos, 'Star Wars'. Do not use quotes"},
        },
        "required": ["website", "query"]
    }
}

def open_page_api(url, open_location):
    """Opens url on a browser"""
    try:
        br.open_page(url, open_location)
        return {"status": "success", "message": f"Successfully opened {url}."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def search_page_api(url, query):
    """Search web page on a browser"""
    try:
        br.query_page(url, query)
        return {"status": "success", "message": f"Successfully searched query from {url}."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}