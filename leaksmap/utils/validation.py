from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError
from typing import List, Dict, Any

# Модель для валидации входных данных
class InputDataModel(BaseModel):
    email: EmailStr
    url: HttpUrl
    additional_fields: Dict[str, Any] = {}

# Функция для санитизации входных данных
def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Санитизирует входные данные, удаляя потенциально опасные символы.
    """
    sanitized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Удаление потенциально опасных символов
            sanitized_value = value.replace("<", "").replace(">", "").replace("'", "").replace('"', "")
            sanitized_data[key] = sanitized_value
        else:
            sanitized_data[key] = value
    return sanitized_data

# Функция для валидации входных данных
def validate_input(data: Dict[str, Any]) -> InputDataModel:
    """
    Валидирует входные данные с использованием Pydantic модели.
    """
    try:
        validated_data = InputDataModel(**data)
        return validated_data
    except ValidationError as e:
        raise ValueError(f"Ошибка валидации: {e}")
