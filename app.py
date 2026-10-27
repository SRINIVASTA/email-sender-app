import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Email Sandbox", page_icon="✉️")

st.title("✉️ Streamlit Email Sandbox")
st.caption("A minimal playground application to test Python SMTP connections.")

try:
    # 1. Safely pull all credentials from Streamlit Secrets
    sender_email = st.secrets["EMAIL_USER"]
    app_password = st.secrets["EMAIL_PASS"]
    default_recipient = st.secrets["EMAIL_TO"]

    # 2. Input fields (Using the secret as the default value on screen)
    recipient = st.text_input("Send To:", value=default_recipient)
    subject = st.text_input("Subject Line:", value="Hello from Streamlit!")
    body = st.text_area("Email Content:", value="This is a test email sent from my Streamlit practice app.")

    if st.button("🚀 Fire Email", use_container_width=True):
        if not recipient:
            st.warning("Please specify a recipient email address.")
        else:
            with st.spinner("Establishing secure SSL handshake..."):
                try:
                    # 3. Build the structural multi-part email payload
                    message = MIMEMultipart()
                    message["From"] = sender_email
                    message["To"] = recipient
                    message["Subject"] = subject
                    message.attach(MIMEText(body, "plain"))

                    # 4. Connect to Gmail SMTP with a manual, clean handshake sequence
                    # We use standard SMTP but add a timeout to prevent hanging, then upgrade securely.
                    server = smtplib.SMTP("://gmail.com", 587, timeout=15)
                    
                    # Say hello to the server first to establish who we are
                    server.ehlo() 
                    
                    # Upgrade the connection to secure TLS encryption
                    server.starttls() 
                    
                    # Say hello again over the newly encrypted secure channel
                    server.ehlo()
                    
                    # Authenticate and send
                    server.login(sender_email, app_password)
                    server.sendmail(sender_email, recipient, message.as_string())
                    server.quit()

                    st.success(f"Email successfully delivered to {recipient}!")

                except smtplib.SMTPAuthenticationError:
                    st.error("Authentication Error: The 16-character App Password was rejected.")
                    st.info("Verify that spaces were completely removed from the password string in your Secrets and that Google 2-Step Verification is still active.")
                except Exception as exception_message:
                    st.error(f"Network Connection Failed: {exception_message}")

except KeyError:
    st.error("Credential Error: Streamlit Secrets are missing or named incorrectly.")
    st.info("Ensure you have defined EMAIL_USER, EMAIL_PASS, and EMAIL_TO inside your Streamlit Cloud Advanced Settings.")
