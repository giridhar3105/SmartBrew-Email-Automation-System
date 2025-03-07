import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime

def fetch_sent_emails(email_user, email_pass, start_date, end_date):
    """
    Fetches sent emails from Gmail and classifies them into responded and not responded.
    """
    responded = []
    not_responded = []

    try:
        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass)
        mail.select('"[Gmail]/Sent Mail"')

        # Convert date format to IMAP format
        start_date = start_date.strftime("%d-%b-%Y")
        end_date = end_date.strftime("%d-%b-%Y")

        # Search for emails within date range
        result, data = mail.search(None, f'SINCE {start_date} BEFORE {end_date}')
        email_ids = data[0].split()

        for email_id in email_ids:
            res, msg_data = mail.fetch(email_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Extract recipient's email
            to_email = msg["To"]
            name, email_address = re.match(r'(.*)<(.*)>', to_email).groups() if "<" in to_email else ("Unknown", to_email)

            # Check for reply
            if "Re:" in msg["Subject"]:
                responded.append((name.strip(), email_address.strip(), "Responded"))
            else:
                not_responded.append((name.strip(), email_address.strip(), "Not Responded"))

        mail.logout()
        return responded, not_responded

    except Exception as e:
        print("❌ Error fetching emails:", e)
        return [], []
