from typing import List, Dict

BASE_RECOMMENDATIONS = {
    "Russian": [
        "Смените пароль в {service_name} и, если этот пароль использовался на других сайтах, смените его и там.",
        "Включите двухфакторную аутентификацию, если это возможно.",
        "Проверьте недавние действия в вашем аккаунте {service_name} на наличие подозрительной активности.",
        "Остерегайтесь фишинговых сообщений: не переходите по непроверенным ссылкам по email/SMS, даже если они выглядят как от этого сервиса.",
        "Заведите уникальные и сложные пароли для каждого сервиса.",
        "Используйте уникальные пароли для каждого аккаунта, чтобы минимизировать риск утечки данных.",
        "Регулярно обновляйте пароли и используйте сложные комбинации символов, включая буквы, цифры и специальные символы.",
        "Будьте осторожны с публичными Wi-Fi сетями: избегайте ввода конфиденциальной информации, если вы не используете VPN.",
        "Настройте уведомления о входе в ваш аккаунт, чтобы получать оповещения о любых необычных или несанкционированных попытках входа.",
        "Регулярно проверяйте историю входа в ваш аккаунт и отключайте доступ с неизвестных устройств."
    ],
    "English": [
        "Change your password in {service_name} and, if this password was used on other websites, change it there as well.",
        "Enable two-factor authentication if possible.",
        "Check your recent account activity in {service_name} for any suspicious activity.",
        "Be cautious of phishing messages: do not click on unverified links via email/SMS, even if they appear to be from this service.",
        "Create unique and complex passwords for each service.",
        "Use unique passwords for each account to minimize the risk of data breaches.",
        "Regularly update your passwords and use complex combinations of characters, including letters, numbers, and special symbols.",
        "Be careful with public Wi-Fi networks: avoid entering confidential information if you are not using a VPN.",
        "Set up login notifications to receive alerts about any unusual or unauthorized login attempts.",
        "Regularly check your account login history and disable access from unknown devices."
    ],
    "Spanish": [
        "Cambie su contraseña en {service_name} y, si esta contraseña se utilizó en otros sitios web, cámbiela allí también.",
        "Habilite la autenticación de dos factores si es posible.",
        "Revise la actividad reciente de su cuenta en {service_name} para detectar cualquier actividad sospechosa.",
        "Tenga cuidado con los mensajes de phishing: no haga clic en enlaces no verificados a través de correo electrónico/SMS, incluso si parecen ser de este servicio.",
        "Cree contraseñas únicas y complejas para cada servicio.",
        "Use contraseñas únicas para cada cuenta para minimizar el riesgo de violaciones de datos.",
        "Actualice regularmente sus contraseñas y use combinaciones complejas de caracteres, incluidas letras, números y símbolos especiales.",
        "Tenga cuidado con las redes Wi-Fi públicas: evite ingresar información confidencial si no está utilizando una VPN.",
        "Configure notificaciones de inicio de sesión para recibir alertas sobre cualquier intento de inicio de sesión inusual o no autorizado.",
        "Revise regularmente el historial de inicio de sesión de su cuenta y desactive el acceso desde dispositivos desconocidos."
    ]
}

SPECIAL_RECOMMENDATIONS = {
    "VK": {
        "Russian": [
            "Проверьте сохранённые устройства и завершите неизвестные сеансы.",
            "Отключите лишние приложения с доступом к вашему аккаунту."
        ],
        "English": [
            "Check saved devices and end unknown sessions.",
            "Disable unnecessary applications with access to your account."
        ]
    },
    "Mail.ru": {
        "Russian": [
            "Проверьте, не настроена ли переадресация писем без вашего ведома.",
            "Убедитесь, что резервные почты и телефоны актуальны."
        ],
        "English": [
            "Check if email forwarding is set up without your knowledge.",
            "Ensure that backup emails and phones are up-to-date."
        ]
    },
    "Facebook": {
        "Russian": [
            "Проверьте, какие приложения имеют доступ к вашему аккаунту, и отключите ненужные.",
            "Настройте приватность профиля, чтобы ограничить доступ к вашей информации."
        ],
        "English": [
            "Check which applications have access to your account and disable unnecessary ones.",
            "Set up profile privacy to limit access to your information."
        ]
    },
    "Instagram": {
        "Russian": [
            "Проверьте, какие приложения имеют доступ к вашему аккаунту, и отключите ненужные.",
            "Настройте приватность профиля, чтобы ограничить доступ к вашей информации."
        ],
        "English": [
            "Check which applications have access to your account and disable unnecessary ones.",
            "Set up profile privacy to limit access to your information."
        ]
    },
    "Twitter": {
        "Russian": [
            "Проверьте, какие приложения имеют доступ к вашему аккаунту, и отключите ненужные.",
            "Настройте приватность профиля, чтобы ограничить доступ к вашей информации."
        ],
        "English": [
            "Check which applications have access to your account and disable unnecessary ones.",
            "Set up profile privacy to limit access to your information."
        ]
    }
}

base_recommendations = BASE_RECOMMENDATIONS
special = SPECIAL_RECOMMENDATIONS

def generate_recommendations(service_name: str, language: str) -> List[str]:
    """
    Generates a list of recommendations for user actions for
    a specific service where a breach occurred.

    :param service_name: Name of the service (e.g., "LinkedIn").
    :param language: Language of the recommendations ("Russian" or "English").
    :return: List of recommendations.
    """
    if not service_name:
        return ["Invalid service name provided."]

    recommendations = base_recommendations[language].copy()
    if service_name in special:
        recommendations.extend(special[service_name][language])

    if not recommendations:
        return ["No recommendations available for this service."]

    recommendations = [rec.replace("{service_name}", service_name) for rec in recommendations]

    return recommendations

def print_recommendations_for_breaches(breaches: List[Dict[str, str]], language: str) -> None:
    """
    For each unique service from the list of breaches
    calls generate_recommendations and prints the recommendations.

    :param breaches: List of breaches.
    :param language: Language of the recommendations ("Russian" or "English").
    """
    if not breaches:
        print("No breaches provided.")
        return

    unique_services = {breach.get('name') for breach in breaches if breach.get('name')}

    for service_name in unique_services:
        print(f'Recommendations for service: {service_name}')
        try:
            resc = generate_recommendations(service_name, language)
            if not resc:
                print("No recommendations available for this service.")
            else:
                for idx, rec in enumerate(resc, 1):
                    print(f'{idx}, {rec}')
                    print()
        except Exception as e:
            print(f"Error generating recommendations for {service_name}: {e}")

def generate_recommendations_dict(breaches: List[Dict[str, str]]) -> Dict[str, Dict[str, List[str]]]:
    """
    Generates dictionaries of recommendations for all breaches in both languages.

    :param breaches: List of breaches.
    :return: Dictionary with recommendations in both languages.
    """
    recommendations_dict = {}
    for language in ["Russian", "English"]:
        recommendations_dict[language] = {}
        for breach in breaches:
            service_name = breach.get("name")
            if service_name:
                recommendations_dict[language][service_name] = generate_recommendations(service_name, language)
    return recommendations_dict

def print_recommendations_for_breaches(breaches: List[Dict[str, str]], language: str) -> None:
    """
    For each unique service from the list of breaches
    calls generate_recommendations and prints the recommendations.

    :param breaches: List of breaches.
    :param language: Language of the recommendations ("Russian" or "English").
    """
    if not breaches:
        print("No breaches provided.")
        return

    unique_services = {breach.get('name') for breach in breaches if breach.get('name')}

    for service_name in unique_services:
        print(f'Recommendations for service: {service_name}')
        try:
            resc = generate_recommendations(service_name, language)
            if not resc:
                print("No recommendations available for this service.")
            else:
                for idx, rec in enumerate(resc, 1):
                    print(f'{idx}, {rec}')
                    print()
        except Exception as e:
            print(f"Error generating recommendations for {service_name}: {e}")
