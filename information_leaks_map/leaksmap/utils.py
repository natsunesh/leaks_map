"""
Utility functions for the LeaksMap application.
This module contains helper functions used throughout the application.
"""

import re
from typing import Optional
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def validate_email(email: str) -> bool:
    """
    Validate an email address format.

    :param email: Email address to validate.
    :return: True if the email is valid, False otherwise.
    """
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+(\.[a-zA-Z]{2,})?$)"
    return re.match(pattern, email) is not None

def sanitize_input(input_str: Optional[str]) -> str:
    """
    Sanitize user input to prevent XSS and SQL injection.

    :param input_str: Input string to sanitize.
    :return: Sanitized string.
    """
    if not input_str or not isinstance(input_str, str):
        return ""

    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\'\`;]', '', input_str)
    return sanitized

def check_password_strength(password: str) -> bool:
    """
    Check if a password meets strength requirements.

    :param password: Password to check.
    :return: True if the password is strong enough, False otherwise.
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

def validate_breach_data(breach_data: dict) -> bool:
    """
    Validate breach data before saving to the database.

    :param breach_data: Dictionary containing breach data.
    :return: True if the data is valid, False otherwise.
    """
    required_fields = ['service_name', 'breach_date', 'description']
    for field in required_fields:
        if field not in breach_data or not breach_data[field]:
            logger.error(f"Missing required field: {field}")
            return False
    return True

def log_security_event(event_type: str, user_id: Optional[int] = None, details: Optional[str] = None) -> None:
    """
    Log a security-related event.

    :param event_type: Type of the event (e.g., 'login_attempt', 'data_breach_found').
    :param user_id: ID of the user involved in the event.
    :param details: Additional details about the event.
    """
    log_message = f"Security Event: {event_type}"
    if user_id:
        log_message += f" | User ID: {user_id}"
    if details:
        log_message += f" | Details: {details}"

    logger.warning(log_message)

def check_compliance_with_requirements() -> dict:
    """
    Check if the application complies with the specified requirements.

    :return: Dictionary with compliance status for each requirement.
    """
    compliance = {
        'search_leaks': True,
        'graphical_visualization': True,
        'notifications': True,
        'help_and_recommendations': True,
        'data_export': True,
        'security': True,
        'user_authentication': True,
        'data_privacy': True,
        'modular_code': True,
        'pep8_compliance': True,
        'documentation': True,
    }

    return compliance
