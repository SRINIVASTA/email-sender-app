import streamlit as st
import smtplib
import socket
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

    # 2. Input fields
    recipient = st.text_input("Send To:", value=default_recipient)
    subject = st.text_input("Subject Line:", value="Hello from Streamlit!")
    body = st.text_area("Email Content:", value="This is a test email sent from my Streamlit practice app.")

    if st.button("🚀 Fire Email", use_container_width=True):
        if not recipient:
            st.warning("Please specify a recipient email address.")
        else:
            with st.spinner("Initiating network routing..."):
                
                # 3. Build the email payload
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = recipient
                message["Subject"] = subject
                message.attach(MIMEText(body, "plain"))

                server = None
                
                # 4. Smart Network Resolver Block
                try:
                    # Attempt standard DNS connection first
                    st.info("Attempting standard DNS route (smtp.gmail.com)...")
                    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
                except (socket.gaierror, socket.error) as dns_error:
                    # DNS Fail: Fallback directly to Google's raw mail server IP address
                    st.warning(f"DNS Resolution failed ({dns_error}). Switching to hardcoded IPv4 gateway...")
                    try:
                        server = smtplib.SMTP("74.125.195.108", 587, timeout=15)
                    except Exception as fallback_error:
                        st.error(f"Fallback route failed: {fallback_error}")

                # 5. Handshake and Transmission execution loop
                if server:
                    try:
                        server.ehlo() 
                        server.starttls() 
                        server.ehlo()
                        server.login(sender_email, app_password)
                        server.sendmail(sender_email, recipient, message.as_string())
                        server.quit()
                        st.success(f"Email successfully delivered to {recipient}! 🎉")
                    except smtplib.SMTPAuthenticationError:
                        st.error("Authentication Error: The 16-character App Password was rejected.")
                        st.info("Verify that spaces were completely removed from your Streamlit Secrets string.")
                    except Exception as connection_error:
                        st.error(f"SMTP Transmission Failed: {connection_error}")

except KeyError:
    st.error("Credential Error: Streamlit Secrets are missing or named incorrectly.")
    st.info("Ensure you have defined EMAIL_USER, EMAIL_PASS, and EMAIL_TO inside your Streamlit Cloud Advanced Settings.")
