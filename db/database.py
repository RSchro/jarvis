from sqlite3 import connect
from os.path import isfile
import os.path

import subprocess

db_name = "jarvis.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, db_name)
BUILD_PATH = "build.sql"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()

# Builds the database
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)

# Fetches build.sql to create database
def scriptexec(path):
    with open(path, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

def insert_app_path(app_name, app_path):
    """Insert app path into table"""
    cxn = connect(DB_PATH, check_same_thread=False)
    cur = cxn.cursor()

    cur.execute("INSERT INTO application_paths VALUES (?, ?)", (app_name.lower(), app_path))

    cxn.commit()
    cxn.close()

def lookup_app_path(app_name):
    """Lookup path to an application by name"""
    cxn = connect(DB_PATH, check_same_thread=False)
    cur = cxn.cursor()

    try:
        cur.execute("SELECT app_path FROM application_paths WHERE app_name = ?", (app_name.lower(),))

        result = cur.fetchone()[0]
        cxn.close()
        return result
    except:
        cxn.close()
        return None

def change_app_path(app_name, app_path):
    """Change path to an application by name"""
    cxn = connect(DB_PATH, check_same_thread=False)
    cur = cxn.cursor()

    cur.execute("UPDATE application_paths SET app_path = ? WHERE app_name = ?", (app_path, app_name.lower()))
    cxn.commit()
    cxn.close()

def delete_app_path(app_name):
    """Deletes an app and its path"""
    cxn = connect(DB_PATH, check_same_thread=False)
    cur = cxn.cursor()

    cur.execute("DELETE FROM application_paths WHERE app_name = ?", (app_name.lower(),))
    cxn.commit()
    cxn.close()

# Formats website names for database
def format_website_name(website):
    formatted_name = website.partition(".")[0]
    formatted_name = formatted_name.replace(" ", "").lower()
    return formatted_name

# Inserts new website and its query url
def insert_url_search(url_name, url_search):
    """Insert url search string into table"""
    cxn = connect(DB_PATH, check_same_thread=False)
    cur = cxn.cursor()

    formatted = format_website_name(url_name)

    cur.execute("INSERT INTO web_search_urls VALUES (?, ?)", (formatted, url_search))

    cxn.commit()
    cxn.close()

# Lookup search url by website
def lookup_url_search(url_name):
    """Lookup url search string by name"""
    cxn = connect(DB_PATH, check_same_thread=False)
    cur = cxn.cursor()

    formatted = format_website_name(url_name)

    cur.execute("SELECT url_search FROM web_search_urls WHERE url_name = ?", (formatted,))

    result = cur.fetchone()[0]

    cxn.close()
    return result

# Remove website search url
def remove_url_search(url_name):
    """Remove url search string from table"""
    cxn = connect(DB_PATH, check_same_thread=False)
    cur = cxn.cursor()

    formatted = format_website_name(url_name)
    cur.execute("DELETE FROM web_search_urls WHERE url_name = ?", (formatted,))

    cxn.commit()
    cxn.close()