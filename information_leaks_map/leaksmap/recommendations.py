from typing import List, Dict, Union, Any
import logging
from .models import Breach

logger = logging.getLogger(__name__)

def generate_checklist(breaches: List[Dict]) -> List[str]:
    """
    Generate a security checklist based on the breaches found.

    Args:
        breaches (List[Dict]): List of breaches with their details.

    Returns:
        List[str]: A list of security recommendations.
    """
    checklist = [
        "Change your passwords regularly",
        "Enable two-factor authentication",
        "Monitor your accounts for suspicious activity",
        "Use a password manager",
        "Avoid reusing passwords across different sites"
    ]

    if breaches:
        checklist.append("Review the security of the following breached services:")
        for breach in breaches:
            if 'Name' in breach:
                checklist.append(f"- {breach['Name']}")

    logger.info("Generated security checklist")
    return checklist

def get_security_advice(breaches: List[Union[Dict, Breach]]) -> str:
    """
    Provide security advice based on the breaches found.

    Args:
        breaches (List[Dict]): List of breaches with their details.

    Returns:
        str: Security advice as a string.
    """
    advice = "Here are some security recommendations based on the breaches found:\n"

    if breaches:
        advice += "You have been affected by the following breaches:\n"
        for breach in breaches:
            if isinstance(breach, dict) and 'service_name' in breach:
                advice += f"- {breach['service_name']}\n"
            elif isinstance(breach, Breach):
                advice += f"- {breach.service_name}\n"
    else:
        advice += "No breaches found. However, it's still important to maintain good security practices.\n"

    advice += "\nGeneral security advice:\n"
    advice += "1. Change your passwords regularly\n"
    advice += "2. Enable two-factor authentication\n"
    advice += "3. Monitor your accounts for suspicious activity\n"
    advice += "4. Use a password manager\n"
    advice += "5. Avoid reusing passwords across different sites\n"

    logger.info("Generated security advice")
    return advice
