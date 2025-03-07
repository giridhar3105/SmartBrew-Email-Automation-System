import streamlit as st
from email_extractor import fetch_sent_emails
from email_sender import send_bulk_email
import pandas as pd

# ---- Page Configuration ----
st.set_page_config(page_title="SmartBrew Email Automation System", page_icon="📧", layout="wide")

# ---- Custom Styles ----
st.markdown("""
    <style>
    /* Center the title & logo */
    .center-text { text-align: center; }

    /* Style buttons */
    div.stButton > button {
        background-color: #007BFF; /* Blue */
        color: white;
        border-radius: 8px;
        padding: 10px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #0056b3; /* Darker Blue */
    }

    /* Improve input field appearance */
    input, textarea {
        border-radius: 8px !important;
        border: 1px solid #ccc !important;
        padding: 10px !important;
    }

    /* Align radio buttons */
    div.stRadio > label { display: inline-block; padding-right: 10px; }
    </style>
""", unsafe_allow_html=True)

# ---- Display Logo ----
st.image("smartbrew_solutionss_logo.jpeg", width=200)
st.markdown("<h1 class='center-text' style='color: white;'>SmartBrew Email Automation System</h1>", unsafe_allow_html=True)

# ---- Toggle Mode ----
mode = st.radio("Select Mode", ["📥 Gmail Sent Email Extractor", "📤 Bulk Email Sender"], horizontal=True)

# ---- Gmail Sent Email Extractor Mode ----
if mode == "📥 Gmail Sent Email Extractor":
    st.subheader("📧 Extract Sent Emails from Gmail")

    # User Credentials
    email = st.text_input("Enter your Gmail", placeholder="your_email@gmail.com")
    app_password = st.text_input("Enter App Password", placeholder="Generated App Password", type="password")

    # Date Range Selection (Side-by-Side)
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")

    # Fetch Emails Button
    if st.button("Fetch Emails"):
        if not email or not app_password:
            st.error("⚠️ Please enter your email and app password.")
        else:
            responded, not_responded = fetch_sent_emails(email, app_password, start_date, end_date)

            all_emails = responded + not_responded
            if all_emails:
                df = pd.DataFrame(all_emails, columns=["Name", "Email", "Status"])
                st.success(f"✅ {len(all_emails)} Emails Extracted")
                st.write(df)

                # Download CSV
                st.download_button("Download CSV", df.to_csv(index=False), "sent_emails.csv", "text/csv")
            else:
                st.error("❌ No emails found!")

# ---- Bulk Email Sender Mode ----
elif mode == "📤 Bulk Email Sender":
    st.subheader("📨 Send Bulk Emails")

    # Email Credentials
    sender_email = st.text_input("Sender Email", placeholder="your_email@gmail.com")
    sender_password = st.text_input("App Password", placeholder="Generated App Password", type="password")

    # Recipient Selection
    recipient_mode = st.radio("Recipient Input Method", ["📧 Single Email", "📂 Upload CSV"], horizontal=True)

    recipients = []
    if recipient_mode == "📧 Single Email":
        recipient_email = st.text_input("Recipient Email", placeholder="example@gmail.com")
        if recipient_email:
            recipients.append({"Name": "Recipient", "Email": recipient_email})
    else:
        uploaded_file = st.file_uploader("Upload CSV (Format: Name, Email)", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            if "Email" in df.columns:
                recipients = df.to_dict(orient="records")
            else:
                st.error("❌ CSV must contain an 'Email' column.")

    # Email Content
    subject = st.text_input("Email Subject", placeholder="Enter subject...")
    message_body = st.text_area("Email Body", placeholder="Write your email message...")

    # File Attachments
    attachment = st.file_uploader("Attach File (Optional)", type=["pdf", "jpg", "png", "docx"])

    # Send Emails Button
    if st.button("🚀 Send Emails"):
        if not sender_email or not sender_password:
            st.error("⚠️ Please enter your email credentials!")
        elif not recipients:
            st.error("⚠️ No recipient email addresses found!")
        else:
            send_bulk_email(sender_email, sender_password, recipients, subject, message_body, attachment)
