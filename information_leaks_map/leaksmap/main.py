import signal
import sys
import logging
from structlog import get_logger, BoundLogger
from django.core.management import execute_from_command_line

# Логгер для main.py
logger = BoundLogger(get_logger())

def graceful_shutdown(signum, frame):
    """Обработка сигналов для graceful shutdown."""
    logger.info("Received signal to shut down gracefully.")
    sys.exit(0)

def main():
    """Точка входа для запуска Django приложения."""
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)
    logger.info("Starting the application.")
    execute_from_command_line()

if __name__ == "__main__":
    main()
