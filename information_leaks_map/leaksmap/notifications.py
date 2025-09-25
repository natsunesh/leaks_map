from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def notify_user(email: str, message: str) -> bool:
    """
    Send a notification email to the user.

    Args:
        email (str): The recipient's email address.
        message (str): The message to send.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        send_mail(
            subject='Information Leak Notification',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"Notification sent to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send notification to {email}: {e}")
        return False
