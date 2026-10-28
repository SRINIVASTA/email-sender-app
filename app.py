import streamlit as st
import smtplib
import time
from email.mime.text import MIMEText

# UI Inputs
email_receiver_input = st.text_input('To (Recipient Email - separate multiple with commas)')
subject = st.text_input('Subject')
body = st.text_area('Body')

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
        # This turns "one@gmail.com, two@gmail.com" into ["one@gmail.com", "two@gmail.com"]
        recipient_list = [email.strip() for email in email_receiver_input.split(",") if email.strip()]

        # 2. Establish connection to Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, app_password)

        # 3. Loop through each recipient and send individually
        for receiver in recipient_list:
            msg = MIMEText(body)
            msg['From'] = email_sender
            msg['To'] = receiver
            msg['Subject'] = subject

            server.sendmail(email_sender, receiver, msg.as_string())
            
            # Anti-spam delay: sleep for 1 second if sending to multiple people
            if len(recipient_list) > 1:
                time.sleep(1)

        server.quit()
        st.success(f'Email(s) sent successfully to {len(recipient_list)} recipient(s)! 🚀')
        
    except Exception as e:
        st.error(f"Erreur lors de l’envoi de l’e-mail : {e}")
