from pydantic import BaseModel, EmailStr, Field, ValidationError as PydanticValidationError, validator
import re

class ValidationError(PydanticValidationError):
    """Ошибка валидации данных."""
    pass

class EmailValidation(BaseModel):
    """Валидация email с использованием pydantic."""
    email: EmailStr

    @validator('email')
    def validate_email_format(cls, value):
        """Проверка формата email."""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValidationError(f"Invalid email format: {value}")
        return value

class SanitizedInput(BaseModel):
    """Сантизация входных данных."""
    data: str = Field(..., description="Входные данные для сантизации")

    @validator('data', pre=True, always=True)
    def sanitize_input(cls, value):
        """Удаление потенциально опасных символов."""
        # Пример: удаление HTML-тегов
        clean_value = re.sub(r'<.*?>', '', value)
        return clean_value
