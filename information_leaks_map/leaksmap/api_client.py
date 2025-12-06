import aiohttp
from typing import List, Dict, Optional
import re
import os
import logging
from django.conf import settings  # Для Django settings

# Локальные утилиты (замените на ваши)
def validate_email(email: str) -> bool:
    """Простая валидация email."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

logger = logging.getLogger(__name__)

class SimpleCacheManager:
    """Простой in-memory кэш (замените на redis/memcached)."""
    def __init__(self):
        self.cache = {}
    
    def get(self, url: str, params: dict) -> Optional[List[Dict]]:
        key = f"{url}:{hash(frozenset(params.items()))}"
        return self.cache.get(key)
    
    def set(self, url: str, params: dict, data: List[Dict], ttl: int = 3600):
        key = f"{url}:{hash(frozenset(params.items()))}"
        self.cache[key] = data

class LeakCheckAPIClient:
    """Клиент для LeakCheck API."""
    
    BASE_URL = "https://leakcheck.io/api/public"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or getattr(settings, 'LEAKCHECK_API_KEY', os.getenv('LEAKCHECK_API_KEY'))
        if not self.api_key:
            raise ValueError("LEAKCHECK_API_KEY required")
        self.cache = SimpleCacheManager()
    
    def _validate_email(self, email: str) -> bool:
        return validate_email(email)
    
    async def get_breach_info_by_email(self, email: str, timeout: float = 10.0) -> List[Dict[str, str]]:
        """Асинхронный запрос к LeakCheck API."""
        if not self._validate_email(email):
            logger.error(f"Invalid email: {email}")
            return []
        
        params = {"key": self.api_key, "check": email}
        cache_key = (self.BASE_URL, params)
        cached = self.cache.get(self.BASE_URL, params)
        if cached:
            return cached
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            try:
                async with session.get(self.BASE_URL, params=params) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    
                    if data.get("success"):
                        breaches = self._standardize_leakcheck_data(data.get("sources", []))
                        self.cache.set(self.BASE_URL, params, breaches)
                        return breaches
                    return []
            except Exception as e:
                logger.error(f"LeakCheck API error for {email}: {e}")
                return []
    
    def _standardize_leakcheck_data(self, sources: List[Dict]) -> List[Dict[str, str]]:
        """Стандартизация данных LeakCheck."""
        return [{
            "service_name": s.get("name", "Unknown"),
            "breach_date": s.get("date", "Unknown"),
            "location": s.get("location", "Unknown"),
            "data_type": s.get("data_type", "Unknown"),
            "description": s.get("description", "Breach detected"),
            "source": "LeakCheck"
        } for s in sources]

class HaveIBeenPwnedAPIClient:
    """Клиент для HaveIBeenPwned API."""
    
    BASE_URL = "https://haveibeenpwned.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or getattr(settings, 'HIBP_API_KEY', os.getenv('HIBP_API_KEY'))
        if not self.api_key:
            raise ValueError("HIBP_API_KEY required")
        self.cache = SimpleCacheManager()
    
    async def get_breach_info_by_email(self, email: str, timeout: float = 10.0) -> List[Dict[str, str]]:
        """Асинхронный запрос к HIBP API."""
        if not validate_email(email):
            logger.error(f"Invalid email: {email}")
            return []
        
        url = f"{self.BASE_URL}/breachedaccount/{email}"
        headers = {
            "hibp-api-key": self.api_key,
            "user-agent": "LeaksMap/1.0"
        }
        
        cached = self.cache.get(url, {"email": email})
        if cached:
            return cached
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            try:
                async with session.get(url, headers=headers) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    
                    breaches = self._standardize_hibp_data(data)
                    self.cache.set(url, {"email": email}, breaches)
                    return breaches
            except Exception as e:
                logger.error(f"HIBP API error for {email}: {e}")
                return []
    
    def _standardize_hibp_data(self, breaches: List[Dict]) -> List[Dict[str, str]]:
        """Стандартизация данных HIBP."""
        return [{
            "service_name": b.get("Name", "Unknown"),
            "breach_date": b.get("BreachDate", "Unknown"),
            "location": "Unknown",
            "data_type": ", ".join(b.get("DataClasses", [])) or "Unknown",
            "description": b.get("Description", "Breach detected"),
            "source": "HaveIBeenPwned"
        } for b in breaches]

# Backward compatibility
def get_leakcheck_client(api_key: str):
    """Для совместимости с views.py."""
    return LeakCheckAPIClient(api_key)

def get_hibp_client(api_key: str):
    """Для совместимости с views.py."""
    return HaveIBeenPwnedAPIClient(api_key)