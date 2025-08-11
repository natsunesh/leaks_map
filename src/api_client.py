import requests
from src.utils import validate_email
import logging
from typing import List, Dict, Optional
import re
from cache.cache_manager import CacheManager

logger = logging.getLogger(__name__)
# Configure logging level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class LeakCheckAPIClient:
    """
    Клиент для работы с публичным API LeakCheck.
    """

    BASE_URL = "https://leakcheck.io/api/public"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key must be provided")
        self.api_key = api_key
        self.cache_manager = CacheManager()

    @staticmethod
    def _validate_email(email: str) -> bool:
        """
        Простая проверка формата email.
        """
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(pattern, email) is not None

    # Sample data for testing
    sample_data = [
        {"Name": "Test Breach 1", "BreachDate": "2023-01-01", "Description": "Пароль под угрозой"},
        {"Name": "Test Breach 2", "BreachDate": "2023-02-01", "Description": "пароль и логин под угрозой"}
    ]

    def get_breach_info(self, email: str, timeout: float = 10.0) -> List[Dict[str, Optional[str]]]:
        """
        Retrieve a list of breaches for the given email using the public LeakCheck API.

        :param email: Email address to check.
        :param timeout: Request timeout in seconds.
        :return: List of dictionaries with breach information, or an empty list if no breaches are found or in case of errors.
        """
        email = email.strip()
        if not self._validate_email(email):
            logger.error(f"Invalid email format: {email}")
            return []

        params = {
            "key": self.api_key,
            "check": email,
        }

        cached_data = self.cache_manager.get(self.BASE_URL, params)
        if cached_data:
            return cached_data

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.error(f"Timeout expired for email {email} when accessing LeakCheck API")
            return []
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for email {email} when accessing LeakCheck API")
            return []
        except requests.exceptions.HTTPError as err:
            if response.status_code == 404:
                logger.error(f"Resource not found for email {email}")
            elif response.status_code == 429:
                logger.error(f"Rate limit exceeded for email {email}")
            elif response.status_code == 500:
                logger.error(f"Internal server error for email {email}")
            else:
                logger.error(f"HTTP error {response.status_code} for email {email}: {err}")
            return []
        except requests.exceptions.RequestException as err:
            logger.error(f"Unexpected error for email {email}: {err}", exc_info=True)
            return []

        try:
            data = response.json()
        except ValueError:
            logger.error(f"Invalid JSON response for email {email}")
            return []

        if not data.get("success", False):
            logger.info(f"LeakCheck API returned success=false for email {email}")
            return data.get("data", []) if data.get("data") else []
        else:
            return data.get("data", [])

        if data.get("found", 0) < 1:
            logger.info(f"No breaches found for email {email}")
            return []

        sources = data.get("sources", [])
        if not isinstance(sources, list):
            logger.error(f"Malformed 'sources' data for email {email}")
            return []

        # Стандартизируем формат вывода
        results = []
        for source in sources:
            # Ожидается объект вроде {"name": "Evony.com", "date": "2016-07"}
            name = source.get("name")
            date = source.get("date")

            results.append({
                "service_name": name or "Unknown",
                "breach_date": date or "Unknown",
                "description": f"Data breach detected at {name}" if name else "Data breach detected"
            })

        self.cache_manager.set(self.BASE_URL, params, results)
        return results

    def get_breach_info_by_username(self, username: str, timeout: float = 10.0) -> List[Dict[str, Optional[str]]]:
        """
        Retrieve a list of breaches for the given username using the public LeakCheck API.

        :param username: Username to check.
        :param timeout: Request timeout in seconds.
        :return: List of dictionaries with breach information, or an empty list if no breaches are found or in case of errors.
        """
        username = username.strip()
        if not username:
            logger.error("Username must be provided")
            return []

        params = {
            "key": self.api_key,
            "check": username,
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.error(f"Timeout expired for username {username} when accessing LeakCheck API")
            return []
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for username {username} when accessing LeakCheck API")
            return []
        except requests.exceptions.HTTPError as err:
            if response.status_code == 404:
                logger.error(f"Resource not found for username {username}")
            elif response.status_code == 429:
                logger.error(f"Rate limit exceeded for username {username}")
            elif response.status_code == 500:
                logger.error(f"Internal server error for username {username}")
            else:
                logger.error(f"HTTP error {response.status_code} for username {username}: {err}")
            return []
        except requests.exceptions.RequestException as err:
            logger.error(f"Unexpected error for username {username}: {err}", exc_info=True)
            return []

        try:
            data = response.json()
        except ValueError:
            logger.error(f"Invalid JSON response for username {username}")
            return []

        if not data.get("success", False):
            logger.info(f"LeakCheck API returned success=false for username {username}")
            return []

        if data.get("found", 0) < 1:
            logger.info(f"No breaches found for username {username}")
            return []

        sources = data.get("sources", [])
        if not isinstance(sources, list):
            logger.error(f"Malformed 'sources' data for username {username}")
            return []

        # Стандартизируем формат вывода
        results = []
        for source in sources:
            # Ожидается объект вроде {"name": "Evony.com", "date": "2016-07"}
            name = source.get("name")
            date = source.get("date")

            results.append({
                "service_name": name or "Unknown",
                "breach_date": date or "Unknown",
                "description": f"Data breach detected at {name}" if name else "Data breach detected"
            })

        return results
