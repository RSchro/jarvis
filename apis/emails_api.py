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

retrieve_email_dec = {
    "name": "retrieve_email",
    "description": "Retrieves information from the user's email using a list of stored email uids",
    "parameters": {
        "type": "OBJECT",
        "properties": {"email_idx": {"type": "INTEGER", "description": "The index of the email to retrieve (starting at 1). Example: 1 for the first email, 2 for the second."}},
        "required": ["email_idx"]
    }
}

def count_emails():
    try:
        count = email.count_new_mail()
        return {"status": "success", "message": f"Emails counted", "emails": str(count)}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def print_emails(limit=5):
    try:
        email.print_new_mail(limit)
        return {"status": "success", "message": f"Emails printed to console"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def delete_mail(subject, sender):
    return email.delete_mail(subject, sender)

def retrieve_email(email_idx: int) -> dict:
    try:
        mail_uid = email.recent_mail_ids[email_idx]
        info = email.retrieve_mail(mail_uid)
        return {"status": "success", "message": f"Email info retrieved.", "email": info}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}