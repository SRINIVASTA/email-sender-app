import streamlit as st
import smtplib
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

# --- APPLICATION HEADER ---
st.set_page_config(page_title="Bulk Email Sender", page_icon="✉️")
st.title("✉️ Streamlit Email Mass Sender with Attachments")
st.markdown("Easily send secure bulk emails with attachments through Gmail using Streamlit Secrets.")
st.divider()

# UI Inputs
email_receiver_input = st.text_input('To (Recipient Email - separate multiple with commas)')
subject = st.text_input('Subject')
body = st.text_area('Body')

# File Uploader for multiple documents
uploaded_files = st.file_uploader("Attach documents", accept_multiple_files=True)

if st.button("Send Email"):
    try:
        email_sender = st.secrets["gmail"]["username"]
        app_password = st.secrets["gmail"]["app_password"]
    except KeyError:
        st.error("Missing credentials! Please configure Streamlit Secrets.")
        st.stop()

    if not email_receiver_input:
        st.error("Please enter at least one recipient email address.")
        st.stop()

    try:
        # 1. Clean and convert the input string into a proper Python list
        recipient_list = [email.strip() for email in email_receiver_input.split(",") if email.strip()]

        # 2. Establish connection to Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, app_password)

        # 3. Loop through each recipient and send individually
        for receiver in recipient_list:
            # Change to MIMEMultipart to support attachments
            msg = MIMEMultipart()
            msg['From'] = email_sender
            msg['To'] = receiver
            msg['Subject'] = subject

            # Attach the text body
            msg.attach(MIMEText(body, 'plain'))

            # 4. Process and attach each uploaded file
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    # Create the attachment object
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(uploaded_file.read())
                    encode_base64(part)
                    
                    # Add headers for the file name
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{uploaded_file.name}"'
                    )
                    msg.attach(part)
                    
                    # Reset file pointer for the next recipient loop iteration
                    uploaded_file.seek(0)

            # Send the email
            server.sendmail(email_sender, receiver, msg.as_string())
            
            # Anti-spam delay: sleep for 1 second if sending to multiple people
            if len(recipient_list) > 1:
                time.sleep(1)

        server.quit()
        st.success(f'Email(s) sent successfully to {len(recipient_list)} recipient(s) with {len(uploaded_files) if uploaded_files else 0} file(s)! 🚀')
        
    except Exception as e:
        st.error(f"Erreur lors de l’envoi de l’e-mail : {e}")
