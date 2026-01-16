import pytest
import httpx
from leaksmap.api_client import fetch_data, encrypt_data, decrypt_data
from unittest.mock import patch

# Тест для функции шифрования данных
def test_encrypt_data():
    key = b"encryption_key"
    data = "sensitive_data"
    encrypted = encrypt_data(data, key)
    assert encrypted is not None
    assert encrypted != data

# Тест для функции дешифрования данных
def test_decrypt_data():
    key = b"encryption_key"
    data = "sensitive_data"
    encrypted = encrypt_data(data, key)
    decrypted = decrypt_data(encrypted, key)
    assert decrypted == data

# Тест для функции fetch_data с имитацией успешного ответа
@patch("leaksmap.api_client.client.get")
def test_fetch_data_success(mock_get):
    mock_get.return_value = MockResponse(status_code=200, json={"key": "value"})
    url = "https://api.example.com/test"
    params = {"param": "value"}
    data = fetch_data(url, params)
    assert data == {"key": "value"}

# Тест для функции fetch_data с имитацией ошибки 404
@patch("leaksmap.api_client.client.get")
def test_fetch_data_404(mock_get):
    mock_get.return_value = MockResponse(status_code=404)
    url = "https://api.example.com/test"
    params = {"param": "value"}
    with pytest.raises(httpx.HTTPStatusError):
        fetch_data(url, params)

# Вспомогательный класс для имитации ответа
class MockResponse:
    def __init__(self, status_code, json=None):
        self.status_code = status_code
        self.json_data = json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(f"Error {self.status_code}")

    def json(self):
        return self.json_data
