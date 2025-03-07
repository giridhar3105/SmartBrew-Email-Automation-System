import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import SMTP_SERVER, SMTP_PORT

def send_email(sender_email, sender_password, recipient, subject, body, attachment=None):
    """
    Sends an email using SMTP with optional attachment.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient["Email"]
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Add attachment if provided
        if attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={attachment.name}")
            msg.attach(part)

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient["Email"], msg.as_string())
        server.quit()

        return f"✅ Email sent to {recipient['Email']}"
    
    except Exception as e:
        return f"❌ Error sending email to {recipient['Email']}: {e}"

def send_bulk_email(sender_email, sender_password, recipients, subject, body, attachment=None):
    """
    Sends bulk emails.
    """
    for recipient in recipients:
        result = send_email(sender_email, sender_password, recipient, subject, body, attachment)
        print(result)
