

import re
from typing import List, Dict, Optional

def validate_email(email: str) -> bool:
    """
    Validate the format of an email address using a regular expression.

    :param email: The email address to validate.
    :return: True if the email is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_user_email() -> str:
    """
    Prompt the user to enter an email address and validate its format.

    :return: A valid email address entered by the user.
    """
    while True:
        email = input('Введите email для проверки: ').strip()

        if validate_email(email):
            return email
        else:
            print("Email некорректный, попробуйте вновь.")
