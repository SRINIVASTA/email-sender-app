import streamlit as st
import smtplib
from email.mime.text import MIMEText

# Taking inputs from the UI (excluding the sender's password)
email_receiver = st.text_input('To (Recipient Email)')
subject = st.text_input('Subject')
body = st.text_area('Body')

if st.button("Send Email"):
    # 1. Fetch credentials securely from Streamlit Cloud Secrets
    try:
        email_sender = st.secrets["gmail"]["username"]
        app_password = st.secrets["gmail"]["app_password"]
    except KeyError:
        st.error("Missing credentials! Please configure Streamlit Secrets.")
        st.stop()

    # 2. Build and execute the email sequence
    try:
        msg = MIMEText(body)
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Log in using secrets
        server.login(email_sender, app_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()

        st.success('Email sent successfully! 🚀')
    except Exception as e:
        st.error(f"Erreur lors de l’envoi de l’e-mail : {e}")
