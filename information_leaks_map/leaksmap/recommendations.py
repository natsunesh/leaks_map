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
        "Измените пароли регулярно",
        "Включите двухфакторную аутентификацию",
        "Мониторьте свои аккаунты на наличие подозрительной активности",
        "Используйте менеджер паролей",
        "Избегайте повторного использования паролей на разных сайтах"
    ]

    if breaches:
        checklist.append("Проверьте безопасность следующих скомпрометированных сервисов:")
        for breach in breaches:
            service_name = None
            if isinstance(breach, dict):
                service_name = breach.get('service_name') or breach.get('Name')
            elif hasattr(breach, 'service_name'):
                service_name = breach.service_name
            
            if service_name:
                checklist.append(f"- {service_name}")

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
    advice = "Вот рекомендации по безопасности на основе обнаруженных утечек:\n\n"

    if breaches:
        advice += "Вы были затронуты следующими утечками:\n"
        unique_services = set()
        for breach in breaches:
            service_name = None
            if isinstance(breach, dict):
                service_name = breach.get('service_name') or breach.get('Name')
            elif isinstance(breach, Breach):
                service_name = breach.service_name
            
            if service_name:
                unique_services.add(service_name)
        
        for service in sorted(unique_services):
            advice += f"- {service}\n"
        advice += "\n"
    else:
        advice += "Утечек не найдено. Однако важно поддерживать хорошие практики безопасности.\n\n"

    advice += "Общие рекомендации по безопасности:\n"
    advice += "1. Регулярно меняйте пароли\n"
    advice += "2. Включите двухфакторную аутентификацию везде, где это возможно\n"
    advice += "3. Мониторьте свои аккаунты на наличие подозрительной активности\n"
    advice += "4. Используйте менеджер паролей для безопасного хранения\n"
    advice += "5. Избегайте повторного использования паролей на разных сайтах\n"
    advice += "6. Обновляйте программное обеспечение регулярно\n"
    advice += "7. Будьте осторожны с фишинговыми письмами и подозрительными ссылками\n"
    advice += "8. Проверяйте свои финансовые счета на наличие необычных транзакций\n"

    logger.info("Generated security advice")
    return advice
