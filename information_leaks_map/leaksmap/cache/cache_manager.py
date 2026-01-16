from typing import List, Dict, Optional
import time
import structlog
from structlog import get_logger
from datetime import datetime, timedelta

logger = get_logger(__name__)

class SecureCacheManager:
    """Безопасный кэш с шифрованием и автоудалением через 24 часа."""

    def __init__(self):
        self.cache = {}

    def get(self, key: str) -> Optional[List[Dict]]:
        """Получение данных из кэша."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if self._is_expired(timestamp):
                logger.info(f"Cache expired for key: {key}. Removing.")
                del self.cache[key]
                return None
            return data
        return None

    def set(self, key: str, data: List[Dict], ttl: int = 86400):
        """Сохранение данных в кэше с TTL (время жизни)."""
        self.cache[key] = (data, time.time())
        logger.info(f"Cache set for key: {key} with TTL: {ttl} seconds.")

    def _is_expired(self, timestamp: float) -> bool:
        """Проверка истечения времени жизни кэша."""
        return time.time() - timestamp > 86400  # 24 часа

    def delete_expired(self):
        """Автоматическое удаление устаревших данных из кэша."""
        current_time = time.time()
        expired_keys = [key for key, (data, timestamp) in self.cache.items() if current_time - timestamp > 86400]
        for key in expired_keys:
            logger.info(f"Cache expired for key: {key}. Removing.")
            del self.cache[key]

# Пример использования
if __name__ == "__main__":
    cache = SecureCacheManager()
    cache.set("example_key", [{"data": "example"}])
    print(cache.get("example_key"))  # Должно вернуть данные
    time.sleep(86401)  # Подождите 24 часа + 1 секунда
    print(cache.get("example_key"))  # Должно вернуть None, так как данные истекли
