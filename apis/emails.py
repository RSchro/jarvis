import imap_tools

from apis.ansicolors import ANSIColors as ansi
from imap_tools import MailBox, OR, AND
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("EMAIL_APP_USER")
password = os.getenv("EMAIL_APP_PSWD")

recent_mail_ids = []

# Prints unread emails --> sender, subject. Takes in optional limit and mark_seen parameters
def print_new_mail(limit=5, mark_seen=False):
    with MailBox("imap.gmail.com").login(username, password, "Inbox") as mb:
        for msg in mb.fetch(OR(seen=False), limit=limit, reverse=True, mark_seen=mark_seen):
            header_from = parse_headers(msg.headers)
            print(f"{ansi.BOLD}{ansi.GREEN}From:{ansi.ENDC} {ansi.BOLD}{header_from}{ansi.ENDC} {msg.from_}")
            print(f"{ansi.BOLD}{ansi.GREEN}Subject:{ansi.ENDC} {msg.subject}\n")

# Parses headers and returns a tidy name of the sender
def parse_headers(header: dict) -> str:
    replace_chars = ['"', "'", "("]
    formatted = str(header["from"]).partition("<")[0][:-1]
    for char in replace_chars:
        if char in formatted:
            formatted = formatted.replace(char, '')
    return formatted

# Counts unread emails
def count_new_mail():
    count = 0
    with MailBox("imap.gmail.com").login(username, password, "Inbox") as mb:
        for msg in mb.fetch(OR(seen=False), reverse=True, mark_seen=False):
            count += 1
            recent_mail_ids.append(msg.uid)
    return count

# Moves unwanted emails to trash folder
def delete_mail(subject, sender):
    trash_folder = "[Gmail]/Trash"
    msg_uid = ""
    try:
        with MailBox("imap.gmail.com").login(username, password, "Inbox") as mb:
            for msg in mb.fetch(AND(subject=subject, from_=sender), limit=1):
                msg_uid = msg.uid
            mb.move(msg_uid, trash_folder, chunks=1)
            return {"status": "success", "message": f"Email moved to trash."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

# Returns a dictionary with sender, subject, and text of an email by uid
def retrieve_mail(msg_uid: str) -> dict:
    email_dict = {}

    with MailBox("imap.gmail.com").login(username, password, "Inbox") as mb:
        for msg in mb.fetch(AND(uid=msg_uid), mark_seen=False):
            email_dict.update({"from": msg.from_})
            email_dict.update({"subject": msg.subject})
            email_dict.update({"text": msg.text})

    return email_dict

count_new_mail()