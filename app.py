import streamlit as st
import resend

st.set_page_config(page_title="Bulk Email Sandbox", page_icon="👥")

st.title("👥 Streamlit Bulk Email Sandbox (BCC Mode)")
st.caption("Practice sending single messages to hidden bulk lists securely.")

try:
    # 1. Pull the API key safely from Streamlit Secrets
    resend.api_key = st.secrets["RESEND_API_KEY"]
    
    # 2. Input fields on screen
    # Enter multiple emails separated by commas (e.g., test1@gmail.com, test2@yahoo.com)
    bulk_input = st.text_area(
        "Enter Bulk Target Emails (separated by commas):", 
        value=st.secrets["EMAIL_TO"]
    )
    
    subject = st.text_input("Subject Line:", value="Secure Bulk Practice Alert")
    body = st.text_area("Email Content:", value="This message was fired out to a hidden bulk list via the Resend API framework.")

    if st.button("🚀 Fire Bulk Campaign", use_container_width=True):
        if not bulk_input:
            st.warning("Please specify at least one recipient address.")
        else:
            with st.spinner("Processing hidden packaging loop..."):
                try:
                    # 3. Parse out clean individual emails from the raw comma text string
                    # This strips away unexpected white spaces automatically
                    parsed_recipients = [email.strip() for email in bulk_input.split(",") if email.strip()]

                    # 4. Define the email details using Resend's secure BCC array layout
                    params = {
                        "from": "onboarding@resend.dev",
                        # We direct the public "to" line to a generic string mask so it stays anonymous
                        "to": "undisclosed-recipients@srinivasta.dev",
                        # The secret list array passes through the bcc gateway safely hidden
                        "bcc": parsed_recipients,
                        "subject": subject,
                        "text": body,
                    }

                    # 5. Fire the payload over web port 443 (Firewall-safe)
                    email = resend.Emails.send(params)
                    
                    st.success(f"Bulk campaign cleanly transmitted! Message ID: {email['id']} 🎉")
                    st.info(f"Delivered securely to {len(parsed_recipients)} hidden inbox locations.")

                except Exception as api_error:
                    st.error(f"API Transmission Failed: {api_error}")

except KeyError:
    st.error("Credential Error: Streamlit Secrets are missing or named incorrectly.")
    st.info("Ensure you have defined RESEND_API_KEY and EMAIL_TO inside your Streamlit Cloud Advanced Settings.")
