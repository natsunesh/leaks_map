import httpx
from tenacity import retry, wait_exponential, stop_after_attempt
from cryptography.fernet import Fernet
from typing import Dict, Any
import structlog

# Логгер
logger = structlog.get_logger("api_client")

# Клиент для асинхронных HTTP-запросов
client = httpx.AsyncClient(verify=True, timeout=10.0)

# Функция для выполнения запроса с повторными попытками
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
async def fetch_data(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Выполняет HTTP GET-запрос с повторными попытками.
    """
    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error("HTTP error occurred", error=e)
        raise
    except Exception as e:
        logger.error("An error occurred", error=e)
        raise

# Функция для шифрования данных перед отправкой
def encrypt_data(data: str, key: bytes) -> str:
    """
    Шифрует данные с использованием ключа Fernet.
    """
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

# Функция для дешифрования данных после получения
def decrypt_data(encrypted_data: str, key: bytes) -> str:
    """
    Дешифрует данные с использованием ключа Fernet.
    """
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return decrypted_data.decode()

# Основная функция для взаимодействия с API
async def get_leaks_data(api_key: str, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Получает данные об утечках с внешнего API.
    """
    encrypted_api_key = encrypt_data(api_key, b"encryption_key")
    headers = {"Authorization": f"Bearer {encrypted_api_key}"}
    url = f"https://api.example.com/{endpoint}"

    logger.info("Sending request to API", url=url, params=params)
    data = await fetch_data(url, params=params)
    logger.info("Received data from API", data=data)

    return data
