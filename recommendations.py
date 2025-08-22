from typing import List, Dict

def generate_recommendations(service: str, language: str) -> List[str]:
    """
    Generate recommendations for a given service based on the language.

    :param service: The name of the service.
    :param language: The language for the recommendations (e.g., "Russian" or "English").
    :return: A list of recommendations.
    """
    recommendations = {
        "Russian": {
            "General": [
                "Измените пароль для всех учетных записей.",
                "Включите двухфакторную аутентификацию.",
                "Используйте уникальные пароли для каждого сервиса."
            ],
            "Evony.com": [
                "Измените пароль для Evony.com.",
                "Проверьте, не используете ли вы этот пароль для других сервисов."
            ],
            "Unknown": [
                "Измените пароль для этого сервиса.",
                "Проверьте, не используете ли вы этот пароль для других сервисов."
            ]
        },
        "English": {
            "General": [
                "Change your password for all accounts.",
                "Enable two-factor authentication.",
                "Use unique passwords for each service."
            ],
            "Evony.com": [
                "Change your password for Evony.com.",
                "Check if you use this password for other services."
            ],
            "Unknown": [
                "Change your password for this service.",
                "Check if you use this password for other services."
            ]
        }
    }

    if service in recommendations[language]:
        return recommendations[language][service]
    else:
        return recommendations[language]["General"]

def print_recommendations_for_breaches(breaches: List[Dict[str, str]], language: str) -> None:
    """
    Print recommendations for a list of breaches.

    :param breaches: List of dictionaries with breach information.
    :param language: The language for the recommendations (e.g., "Russian" or "English").
    """
    for breach in breaches:
        service = breach.get("service", "Unknown")
        recs = generate_recommendations(service, language)
        print(f"Recommendations for {service}:")
        for rec in recs:
            print(f"- {rec}")
        print()
