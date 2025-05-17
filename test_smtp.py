import smtplib
from email.mime.text import MIMEText
import os
import sys

# Email settings from .env file
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = "skillnetservices@gmail.com"
EMAIL_HOST_PASSWORD = "tdms ckdk tmgo fado"
DEFAULT_FROM_EMAIL = "skillnetservices@gmail.com"

def test_smtp_connection():
    """Test SMTP connection to verify email settings."""
    print(f"Testing SMTP connection to {EMAIL_HOST}:{EMAIL_PORT}...")

    try:
        # Create SMTP connection
        if EMAIL_USE_SSL:
            print("Using SSL connection...")
            server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        else:
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)

        server.set_debuglevel(1)  # Enable verbose debug output

        # Start TLS if required
        if EMAIL_USE_TLS:
            print("Starting TLS...")
            server.starttls()

        # Login to SMTP server
        print(f"Logging in as {EMAIL_HOST_USER}...")
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

        print("SMTP connection successful!")

        # Close connection
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_smtp_connection()
    sys.exit(0 if success else 1)
