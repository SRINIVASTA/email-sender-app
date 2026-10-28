# Streamlit Email Mass Sender (Refactored with `yagmail`)

This Streamlit application allows you to securely send bulk or individual emails using **yagmail**, a highly intuitive wrapper around `smtplib`. It includes automated rate-limiting to prevent spam flags and incorporates a real-time progress bar interface.

## Features
- **Simplified Mail Handling**: Replaces complex `MIMEText` and connection logic with simple `yagmail.SMTP` handlers.
- **Dynamic Recipient Processing**: Converts comma-separated text input into a clean list of individual emails.
- **Secure Authentication**: Leverages Streamlit Secrets (`.streamlit/secrets.toml`) to prevent hardcoding sensitive Gmail credentials.
- **Visual Progress Tracking**: Real-time progress updates natively inside the Streamlit user interface.
- **Anti-Spam Safety**: Inserts an intentional delay between dispatches when handling multiple targets.

---

## ⚙️ Application Workflow

```mermaid
graph TD
    A([Start App]) --> B[Input: Recipient, Subject, Body]
    B --> C{Click 'Send Email'}
    C -->|No| B
    C -->|Yes| D[Load Streamlit Secrets]
    D --> E{Credentials Exist?}
    E -->|No| F[Display Error & Stop]
    E -->|Yes| G[Parse Recipient List]
    G --> H[Initialize yagmail.SMTP Client]
    H --> I[Start Broadcast Loop]
    I --> J[Send Email to Recipient]
    J --> K[Update UI Progress Bar]
    K --> L{More Recipients?}
    L -->|Yes| M[Delay 1 Second]
    M --> I
    L -->|No| N[Display Success Message]
    N --> O([End Application])
```

---

## 🛠️ Refactored Python Code (`app.py`)

```python
import streamlit as st
import yagmail
import time

# UI Setup
st.title("✉️ Bulk Email Sender")

email_receiver_input = st.text_input('To (Recipient Email - separate multiple with commas)')
subject = st.text_input('Subject')
body = st.text_area('Body')

if st.button("Send Email", type="primary"):
    # 1. Fetch credentials securely from secrets
    try:
        email_sender = st.secrets["gmail"]["username"]
        app_password = st.secrets["gmail"]["app_password"]
    except KeyError:
        st.error("Missing credentials! Please configure Streamlit Secrets.")
        st.stop()

    # 2. Check for empty recipient input
    if not email_receiver_input.strip():
        st.error("Please enter at least one recipient email address.")
        st.stop()

    try:
        # 3. Clean and isolate individual emails
        recipient_list = [email.strip() for email in email_receiver_input.split(",") if email.strip()]
        total_recipients = len(recipient_list)

        # 4. Initialize UI tracking states
        progress_bar = st.progress(0.0)
        status_text = st.empty()

        # 5. Connect and broadcast via yagmail context manager
        # Context management auto-closes the SMTP session elegantly
        with yagmail.SMTP(user=email_sender, password=app_password) as yag:
            for idx, receiver in enumerate(recipient_list):
                status_text.text(f"Sending to {receiver} ({idx + 1}/{total_recipients})...")
                
                # yagmail processes strings, lists, dicts, and attachments intuitively
                yag.send(
                    to=receiver,
                    subject=subject,
                    contents=body
                )
                
                # Update visual progress tracker
                progress_bar.progress((idx + 1) / total_recipients)
                
                # Anti-spam throttling
                if total_recipients > 1 and idx < total_recipients - 1:
                    time.sleep(1)

        status_text.empty()
        st.success(f'Email(s) sent successfully to {total_recipients} recipient(s)! 🚀')
        
    except Exception as e:
        st.error(f"Error encountered while dispatching email: {e}")
```

---

## 🔒 Configuration & Authentication

### 1. Requirements (`requirements.txt`)
Ensure you have the target libraries available inside your working environment:
```text
streamlit
yagmail
```

### 2. Google Account App Passwords
Gmail blocks standard password authentication from unverified third-party integrations. You must provision an **App Password**:
1. Head to your [Google Account Console](https://google.com).
2. Turn on **2-Step Verification** under the Security tab.
3. Search for or navigate to **App passwords**.
4. Generate a custom app name (e.g., `Streamlit Mailer App`) and click **Create**.
5. Save the generated 16-character string securely.

### 3. Streamlit Secrets Setup (`.streamlit/secrets.toml`)
Create a local secrets file at the root level of your project directory structure:
```text
your_project/
│
├── .streamlit/
│   └── secrets.toml  <-- Create this file
└── app.py
```

Populate `.streamlit/secrets.toml` explicitly using this block structure:
```toml
[gmail]
username = "your_actual_email@gmail.com"
app_password = "abcd efgh ijkl mnop"  # The 16-character string without spaces
```

> ⚠️ **Security Warning:** Add `.streamlit/secrets.toml` directly into your `.gitignore` file immediately to avoid leaking credentials onto public version control systems.
