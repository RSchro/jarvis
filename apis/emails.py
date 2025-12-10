import imap_tools

from apis.ansicolors import ANSIColors as ansi
from imap_tools import MailBox, OR, AND
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("EMAIL_APP_USER")
password = os.getenv("EMAIL_APP_PSWD")

# Prints unread emails --> sender, subject. Takes in optional limit and mark_seen parameters
def get_new_mail(limit=5, mark_seen=False):
    with MailBox("imap.gmail.com").login(username, password, "Inbox") as mb:
        for msg in mb.fetch(OR(seen=False), limit=limit, reverse=True, mark_seen=mark_seen):
            header_from = str(msg.headers["from"]).partition("<")[0][:-1]
            header_from = header_from.replace('"', '')
            header_from = header_from.replace("'", '')
            header_from = header_from.replace("(", "")
            print(f"{ansi.BOLD}{ansi.GREEN}From:{ansi.ENDC} {ansi.BOLD}{header_from}{ansi.ENDC} {msg.from_}")
            print(f"{ansi.BOLD}{ansi.GREEN}Subject:{ansi.ENDC} {msg.subject}\n")

# Counts unread emails
def count_new_mail():
    count = 0
    with MailBox("imap.gmail.com").login(username, password, "Inbox") as mb:
        for msg in mb.fetch(OR(seen=False), reverse=True, mark_seen=False):
            count += 1
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
