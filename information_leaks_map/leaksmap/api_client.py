import requests
import aiohttp
import asyncio
from .utils import validate_email
import logging
from typing import List, Dict, Optional, Union
import re
import os
import sys
# Add parent directory to path for cache import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from cache.cache_manager import CacheManager

# Configure logging level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LeakCheckAPIClient:
    """
    Клиент для работы с публичным API LeakCheck.
    """

    BASE_URL = "https://leakcheck.io/api/public"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key must be provided")
        # Use environment variable if available, otherwise use provided key
        env_key = os.getenv("API_KEY")
        self.api_key = env_key if env_key else api_key
        if not self.api_key:
            raise ValueError("API key must be provided either as parameter or environment variable")
        self.cache_manager = CacheManager()

    def _validate_email(self, email: str) -> bool:
        """
        Простая проверка формата email.
        """
        return validate_email(email)

    async def get_breach_info_by_email(self, email: str, timeout: Optional[float] = 10.0) -> Optional[List[Dict[str, Optional[str]]]]:
        """
        Асинхронный метод для выполнения запроса к API LeakCheck.
        """
        # Validate email before making request
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

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.BASE_URL, params=params, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if data.get("success", False):
                        results = data.get("sources", [])
                        standardized_results = []
                        for source in results:
                            name = source.get("name")
                            date = source.get("date")
                            location = source.get("location", "Unknown")
                            data_type = source.get("data_type", "Unknown")
                            standardized_results.append({
                                "service_name": name or "Unknown",
                                "breach_date": date or "Unknown",
                                "location": location,
                                "data_type": data_type,
                                "description": f"Data breach detected at {name}" if name else "Data breach detected",
                                "source": "LeakCheck"
                            })
                        self.cache_manager.set(self.BASE_URL, params, standardized_results)
                        return standardized_results
                    else:
                        logger.info(f"No breaches found for email {email}")
                        return []
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.error(f"Error fetching data for email {email}: {str(e)}")
                return []
            except Exception as e:
                logger.error(f"Unexpected error fetching data for email {email}: {str(e)}", exc_info=True)
                return []

    def get_breach_info_by_username(self, username: str, timeout: Optional[float] = 10.0) -> Union[List[Dict[str, Optional[str]]], None]:
        """
        Retrieve a list of breaches for the given username using the public LeakCheck API.
        """
        username = username.strip()
        if not username:
            logger.error("Username must be provided")
            return []

        params = {
            "key": self.api_key,
            "check": username,
        }

        response = None
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.error(f"Timeout expired for username {username} when accessing LeakCheck API")
            raise TimeoutError(f"Timeout expired for username {username} when accessing LeakCheck API")
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for username {username} when accessing LeakCheck API")
            raise ConnectionError(f"Connection error for username {username} when accessing LeakCheck API")
        except requests.exceptions.HTTPError as err:
            if response and response.status_code == 404:
                logger.error(f"Resource not found for username {username}")
                raise ValueError(f"Resource not found for username {username}")
            elif response and response.status_code == 429:
                logger.error(f"Rate limit exceeded for username {username}")
                raise ValueError(f"Rate limit exceeded for username {username}")
            elif response and response.status_code == 500:
                logger.error(f"Internal server error for username {username}")
                raise ValueError(f"Internal server error for username {username}")
            else:
                logger.error(f"HTTP error for username {username}: {err}")
                raise ValueError(f"HTTP error for username {username}: {err}")
        except requests.exceptions.RequestException as err:
            logger.error(f"Unexpected error for username {username}: {err}", exc_info=True)
            raise ValueError(f"Unexpected error for username {username}: {err}")

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

        results = []
        for source in sources:
            name = source.get("name")
            date = source.get("date")

            results.append({
                "service_name": name or "Unknown",
                "breach_date": date or "Unknown",
                "description": f"Data breach detected at {name}" if name else "Data breach detected"
            })

        return results

class HaveIBeenPwnedAPIClient:
    async def _fetch_data_haveibeenpwned(self, email: str, timeout: Optional[float] = 10.0) -> Optional[List[Dict[str, Optional[str]]]]:
        headers = {
            "hibp-api-key": self.api_key,
            "user-agent": "LeaksMap"
        }

        # Use email as part of cache key since headers contain sensitive data
        cache_key = f"{self.BASE_URL}/breachedaccount/{email}"
        cache_params = {"email": email}  # Use email as params for cache key
        cached_data = self.cache_manager.get(cache_key, cache_params)
        if cached_data:
            return cached_data

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.BASE_URL}/breachedaccount/{email}", headers=headers, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if data:
                        standardized_results = []
                        for breach in data:
                            name = breach.get("Name")
                            date = breach.get("BreachDate")
                            description = breach.get("Description", "No description")
                            data_classes = breach.get("DataClasses", [])
                            data_type = ", ".join(data_classes) if data_classes else "Unknown"

                            standardized_results.append({
                                "service_name": name or "Unknown",
                                "breach_date": date or "Unknown",
                                "location": "Unknown",
                                "data_type": data_type,
                                "description": description,
                                "source": "HaveIBeenPwned"
                            })

                        cache_key = f"{self.BASE_URL}/breachedaccount/{email}"
                        cache_params = {"email": email}
                        self.cache_manager.set(cache_key, cache_params, standardized_results)
                        return standardized_results
                    else:
                        logger.info(f"No breaches found for email {email}")
                        return []
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.error(f"Error fetching data for email {email}: {str(e)}")
                return []
            except Exception as e:
                logger.error(f"Unexpected error fetching data for email {email}: {str(e)}", exc_info=True)
                return []

        """
        Retrieve a list of breaches for the given email using the Have I Been Pwned API.
        """
        email = email.strip()
        if not self._validate_email(email):
            logger.error(f"Invalid email format: {email}")
            return []

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running, we can't use run_until_complete
                # Use asyncio.run which creates a new event loop
                return asyncio.run(self._fetch_data_haveibeenpwned(email, timeout))
            return loop.run_until_complete(self._fetch_data_haveibeenpwned(email, timeout))
        except RuntimeError:
            # No event loop, create a new one
            return asyncio.run(self._fetch_data_haveibeenpwned(email, timeout))
    """
    Клиент для работы с публичным API Have I Been Pwned.
    """

    BASE_URL = "https://haveibeenpwned.com/api/v3"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key must be provided")
        # Use environment variable if available, otherwise use provided key
        env_key = os.getenv("HIBP_API_KEY")
        self.api_key = env_key if env_key else api_key
        if not self.api_key:
            raise ValueError("API key must be provided either as parameter or environment variable")
        self.cache_manager = CacheManager()

    def _validate_email(self, email: str) -> bool:
        """
        Простая проверка формата email.
        """
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(pattern, email) is not None

    async def get_breach_info_hibp(self, email: str, timeout: Optional[float] = 10.0) -> Optional[List[Dict[str, Optional[str]]]]:
        """
        Асинхронный метод для выполнения запроса к API Have I Been Pwned.
        """
        headers = {
            "hibp-api-key": self.api_key,
            "user-agent": "LeaksMap"
        }

        # Use email as part of cache key since headers contain sensitive data
        cache_key = f"{self.BASE_URL}/breachedaccount/{email}"
        cache_params = {"email": email}  # Use email as params for cache key
        cached_data = self.cache_manager.get(cache_key, cache_params)
        if cached_data:
            return cached_data

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.BASE_URL}/breachedaccount/{email}", headers=headers, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if data:
                        standardized_results = []
                        for breach in data:
                            name = breach.get("Name")
                            date = breach.get("BreachDate")
                            description = breach.get("Description", "No description")
                            data_classes = breach.get("DataClasses", [])
                            data_type = ", ".join(data_classes) if data_classes else "Unknown"

                            standardized_results.append({
                                "service_name": name or "Unknown",
                                "breach_date": date or "Unknown",
                                "location": "Unknown",
                                "data_type": data_type,
                                "description": description,
                                "source": "HaveIBeenPwned"
                            })

                        cache_key = f"{self.BASE_URL}/breachedaccount/{email}"
                        cache_params = {"email": email}
                        self.cache_manager.set(cache_key, cache_params, standardized_results)
                        return standardized_results
                    else:
                        logger.info(f"No breaches found for email {email}")
                        return []
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.error(f"Error fetching data for email {email}: {str(e)}")
                return []
            except Exception as e:
                logger.error(f"Unexpected error fetching data for email {email}: {str(e)}", exc_info=True)
                return []
