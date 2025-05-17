import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

# Print current email settings
print("Current email settings:")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else ''}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# Try to send a test email
try:
    print("\nSending test email...")
    send_mail(
        subject="Test Email",
        message="This is a test email from EduMore360.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["test@example.com"],
        fail_silently=False,
    )
    print("Test email sent successfully!")
except Exception as e:
    print(f"Error sending test email: {e}")
