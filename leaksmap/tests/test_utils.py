import pytest
from leaksmap.utils.validation import sanitize_input, validate_input, InputDataModel

# Тест для функции санитизации данных
def test_sanitize_input():
    data = {"email": "test@example.com", "url": "http://example.com", "additional_fields": {"key": "value"}}
    sanitized_data = sanitize_input(data)
    assert sanitized_data == {"email": "test@example.com", "url": "http://example.com", "additional_fields": {"key": "value"}}

# Тест для функции валидации данных
def test_validate_input():
    data = {"email": "test@example.com", "url": "http://example.com", "additional_fields": {"key": "value"}}
    validated_data = validate_input(data)
    assert isinstance(validated_data, InputDataModel)

# Тест для валидации некорректных данных
def test_validate_input_invalid():
    data = {"email": "invalid-email", "url": "invalid-url", "additional_fields": {"key": "value"}}
    with pytest.raises(ValueError):
        validate_input(data)
