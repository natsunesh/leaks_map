import structlog
from typing import Dict, Any
from leaksmap.utils.validation import sanitize_input, validate_input

# Логгер
logger = structlog.get_logger("utils")

# Функция для санитизации и валидации входных данных
def process_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Обрабатывает входные данные: санитизирует и валидирует.
    """
    sanitized_data = sanitize_input(data)
    validated_data = validate_input(sanitized_data)
    return validated_data

# Функция для логирования событий
def log_event(event: str, details: Dict[str, Any]) -> None:
    """
    Логирует событие с деталями.
    """
    logger.info(event, **details)
