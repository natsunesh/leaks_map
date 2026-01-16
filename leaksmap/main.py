import asyncio
import signal
import structlog
from leaksmap.api_client import get_leaks_data
from leaksmap.utils import log_event
from leaksmap.utils.secrets import load_encryption_key

# Логгер
logger = structlog.get_logger("main")

# Обработчик сигнала для корректного завершения работы
def handle_shutdown(signum, frame):
    logger.info("Received shutdown signal", signal=signum)
    log_event("Shutdown initiated", details={"signal": signum})
    # Очистка ресурсов, если необходимо
    logger.info("Shutdown complete")
    exit(0)

# Основная функция для запуска приложения
async def main():
    # Загрузка ключа шифрования
    encryption_key = load_encryption_key("password")
    logger.info("Encryption key loaded")

    # Пример вызова API
    api_key = "your_api_key_here"
    endpoint = "leaks"
    params = {"param1": "value1"}
    data = await get_leaks_data(api_key, endpoint, params)
    logger.info("Data received from API", data=data)

    # Логирование события
    log_event("API data retrieved", details={"data": data})

# Регистрация обработчика сигнала
signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

# Запуск основной функции
if __name__ == "__main__":
    asyncio.run(main())
