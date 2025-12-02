from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import logging
import os
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

def notify_user_email(email: str, message: str, subject: str = 'Information Leak Notification') -> bool:
    """
    Send a notification email to the user.

    Args:
        email (str): The recipient's email address.
        message (str): The message to send.
        subject (str): Email subject.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
        if not from_email:
            logger.warning("DEFAULT_FROM_EMAIL is not configured in settings")
            return False
        
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"Email notification sent to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email notification to {email}: {e}")
        return False

def notify_user_telegram(telegram_id: str, message: str) -> bool:
    """
    Send a notification via Telegram to the user.

    Args:
        telegram_id (str): The user's Telegram chat ID.
        message (str): The message to send.

    Returns:
        bool: True if the notification was sent successfully, False otherwise.
    """
    try:
        telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not telegram_bot_token:
            logger.warning("TELEGRAM_BOT_TOKEN is not configured")
            return False
        
        # Use python-telegram-bot if available, otherwise use requests
        try:
            from telegram import Bot
            import asyncio
            # python-telegram-bot v20+ requires async
            async def send_telegram_message():
                bot = Bot(token=telegram_bot_token)
                await bot.send_message(chat_id=telegram_id, text=message)
            
            # Run async function
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is already running, create a new one
                    asyncio.run(send_telegram_message())
                else:
                    loop.run_until_complete(send_telegram_message())
            except RuntimeError:
                # No event loop, create a new one
                asyncio.run(send_telegram_message())
            
            logger.info(f"Telegram notification sent to {telegram_id}")
            return True
        except ImportError:
            # Fallback to requests if python-telegram-bot is not available
            import requests
            url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
            payload = {
                'chat_id': telegram_id,
                'text': message
            }
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Telegram notification sent to {telegram_id}")
            return True
    except Exception as e:
        logger.error(f"Failed to send Telegram notification to {telegram_id}: {e}")
        return False

def notify_user_push(user: User, message: str, title: str = 'Information Leak Alert') -> bool:
    """
    Send a push notification to the user.
    
    Note: This is a placeholder implementation. In production, you would integrate
    with a push notification service like Firebase Cloud Messaging (FCM) or OneSignal.

    Args:
        user (User): The user to send the notification to.
        message (str): The message to send.
        title (str): Notification title.

    Returns:
        bool: True if the notification was sent successfully, False otherwise.
    """
    try:
        # Check if user has push notification preferences enabled
        if hasattr(user, 'userprofile'):
            prefs = user.userprofile.notification_preferences
            if not prefs.get('push_enabled', True):
                logger.info(f"Push notifications disabled for user {user.username}")
                return False
        
        # Placeholder for push notification implementation
        # In production, integrate with FCM, OneSignal, or similar service
        logger.info(f"Push notification would be sent to {user.username}: {title} - {message}")
        
        # Example implementation with a service would look like:
        # push_service.send_notification(user.device_token, title, message)
        
        return True
    except Exception as e:
        logger.error(f"Failed to send push notification to {user.username}: {e}")
        return False

def notify_user(user: User, message: str, subject: str = 'Information Leak Notification', 
                breach_details: Optional[List[Dict[str, Any]]] = None) -> Dict[str, bool]:
    """
    Send notifications to user through all enabled channels (Email, Telegram, Push).

    Args:
        user (User): The user to notify.
        message (str): The message to send.
        subject (str): Notification subject/title.
        breach_details (Optional[List[Dict]]): List of breach details for detailed notifications.

    Returns:
        Dict[str, bool]: Dictionary with notification results for each channel.
    """
    results = {
        'email': False,
        'telegram': False,
        'push': False
    }
    
    # Get user preferences
    notification_prefs = {}
    if hasattr(user, 'userprofile'):
        notification_prefs = user.userprofile.notification_preferences
    
    # Prepare detailed message if breach details provided
    detailed_message = message
    if breach_details:
        detailed_message += "\n\nОбнаруженные утечки:\n"
        for breach in breach_details[:5]:  # Limit to 5 breaches in notification
            service = breach.get('service_name', 'Unknown')
            date = breach.get('breach_date', 'Unknown')
            detailed_message += f"- {service} (дата: {date})\n"
        if len(breach_details) > 5:
            detailed_message += f"\n... и еще {len(breach_details) - 5} утечек."
    
    # Send email notification
    if notification_prefs.get('email_enabled', True):
        if user.email:
            results['email'] = notify_user_email(user.email, detailed_message, subject)
    
    # Send Telegram notification
    if notification_prefs.get('telegram_enabled', False):
        if hasattr(user, 'userprofile') and user.userprofile.telegram_id:
            results['telegram'] = notify_user_telegram(user.userprofile.telegram_id, detailed_message)
    
    # Send push notification
    if notification_prefs.get('push_enabled', True):
        results['push'] = notify_user_push(user, detailed_message, subject)
    
    return results
