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

    cur.execute("SELECT app_path FROM application_paths WHERE app_name = ?", (app_name.lower(),))

    result = cur.fetchone()[0]
    cxn.close()
    return result

def change_app_path(app_name, app_path):
    """Change path to an application by name"""
    cxn = connect(DB_PATH, check_same_thread=False)
    cur = cxn.cursor()

    cur.execute("UPDATE application_paths SET app_path = ? WHERE app_name = ?", (app_path, app_name.lower()))
    cxn.commit()
    cxn.close()