from typing import List

from .models import Breach

def get_security_advice(breaches: List[Breach]) -> str:
    """
    Generate personalized security advice based on the user's breaches.

    :param breaches: List of Breach objects.
    :return: str of security advice.
    """
    security_advice = ""
    
    # Group breaches by service for service-specific advice
    service_breaches = {}
    for breach in breaches:
        service = breach.service_name
        if service not in service_breaches:
            service_breaches[service] = []
        service_breaches[service].append(breach)
    
    # Generate service-specific advice
    service_advice = {}
    for service, service_breach_list in service_breaches.items():
        service_advice[service] = generate_service_security_advice(service_breach_list)
    
    # Combine all advice
    for service, advice in service_advice.items():
        security_advice += advice
    
    return security_advice


def generate_service_security_advice(breaches: List[Breach]) -> str:
    """
    Generate service-specific security advice based on the user's breaches.

    :param breaches: List of Breach objects.
    :return: str of security advice.
    """
    advice = ""
    
    # Generate advice for each breach
    for breach in breaches:
        advice += generate_security_advice_for_breach(breach)
    
    return advice


def generate_security_advice_for_breach(breach: Breach) -> str:
    """
    Generate security advice based on a single breach.

    :param breach: Breach object.
    :return: str of security advice.
    """
    advice = ""
    
    # Generate advice based on breach details
    if breach.service_name:
        advice += f"Change your password for {breach.service_name}\n"
    if breach.data_type:
        advice += f"Check your {breach.data_type} for any suspicious activity\n"
    
    return advice

