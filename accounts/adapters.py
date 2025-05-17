from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to send HTML emails
    """
    def send_mail(self, template_prefix, email, context):
        """
        Send a multi-part email with both text and HTML versions
        """
        subject = render_to_string(f'{template_prefix}_subject.txt', context)
        # Remove newlines from subject to comply with RFC2822
        subject = " ".join(subject.splitlines()).strip()
        
        # Render text version
        text_body = render_to_string(f'{template_prefix}_message.txt', context)
        
        # Create email message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        
        # Attach HTML version if template exists
        try:
            html_body = render_to_string(f'{template_prefix}_message.html', context)
            msg.attach_alternative(html_body, "text/html")
        except:
            pass  # If HTML template doesn't exist, just send text version
        
        # Send the email
        msg.send()
