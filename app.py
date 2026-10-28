import streamlit as st
import yagmail

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

    # 2. Build and execute the email sequence using yagmail
    try:
        # Initialize the yagmail client with your secret credentials
        yag = yagmail.SMTP(user=email_sender, password=app_password)
        
        # Send the contents directly
        yag.send(
            to=email_receiver,
            subject=subject,
            contents=body
        )

        st.success('Email sent successfully! 🚀')
    except Exception as e:
        st.error(f"Erreur lors de l’envoi de l’e-mail : {e}")
