import apis.emails as email

count_emails_dec = {
    "name": "count_emails",
    "description": "Counts user's new emails in their inbox. Returns 'count'",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "count": { "type": "INTEGER", "description": "The amount of unread emails"},
        }
    }
}

print_emails_dec = {
    "name": "print_emails",
    "description": "Prints the user's emails to the console.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "limit": {"type": "INTEGER", "description": "The maximum number of emails to print."},
        }
    }
}

delete_emails_dec = {
    "name": "delete_mail",
    "description": "Deletes the user's using given subject and sender.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "subject": {"type": "STRING", "description": "The subject of the email. Example: 'Your receipt from Apple'"},
            "sender": {"type": "STRING", "description": "The sender of the email. Example: 'Apple' or 'Google'"},
        }
    }
}

def count_emails():
    try:
        count = email.count_new_mail()
        return {"status": "success", "message": f"Emails counted", "emails": str(count)}
    except Exception as e:
        print(str(e))
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def print_emails(limit=5):
    try:
        email.get_new_mail(limit)
        return {"status": "success", "message": f"Emails printed to console"}
    except Exception as e:
        print(str(e))
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def delete_mail(subject, sender):
    return email.delete_mail(subject, sender)
