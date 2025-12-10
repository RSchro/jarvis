import webbrowser
import pygetwindow as gw
import pyautogui as pg
import db.database as db

def open_page(url: str, open_location: str = "tab"):
    """Opens url on a browser"""
    same_window = ["same", "same window", "this window"]

    # Open window in new window, same window or new tab
    new = 2
    if open_location.lower() == "new window":
        print("Opening new window")
        new = 1
    elif open_location.lower() in same_window:
        print("Opening same window")
        new = 0
    webbrowser.open(f"https://{url}", new=new)

def query_page(website, query):
    """Search web page on a browser"""
    url = db.lookup_url_search(website)

    if url:
        webbrowser.open(f"{url}{query}", new = 0)
    else:
        print("Url search path not found")

# Scrolls page: value is amount of clicks, direction is False (up) or True (down)
def scroll(down = True):
    """Scroll web page on a browser"""
    scroll_val = 1000
    if down:
        scroll_val *= -1
    pg.scroll(scroll_val)


def swap_to_application(application):
    search = gw.getAllTitles()
    found = False
    for item in search:
        if application.lower() in item.lower():
            application = str(item)
            found = True

    if found:
        app = gw.getWindowsWithTitle(application)[0]
        app.restore()
        app.activate()
    print(found)
    return found