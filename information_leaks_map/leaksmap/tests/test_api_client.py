import pytest
import asyncio
import sys
sys.path.append('e:/проекты/Карта информационных утечек/information_leaks_map')
from leaksmap.api_client import LeakCheckAPIClient, HaveIBeenPwnedAPIClient

@pytest.mark.anyio
async def test_leakcheck_api_client():
    """Тест LeakCheckAPIClient."""
    api_key = "test_api_key"
    client = LeakCheckAPIClient(api_key)

    # Проверка валидации email
    assert client._validate_email("test@example.com") == True
    assert client._validate_email("invalid_email") == False

    # Проверка асинхронного запроса
    breaches = await client.get_breach_info_by_email("test@example.com")
    assert isinstance(breaches, list)
    assert all(isinstance(breach, dict) for breach in breaches)

import unittest.mock as mock

@pytest.mark.anyio
async def test_haveibeenpwned_api_client():
    """Тест HaveIBeenPwnedAPIClient."""
    api_key = "test_api_key"
    client = HaveIBeenPwnedAPIClient(api_key)

    # Мокирование ответа API
    with mock.patch("httpx.AsyncClient.get", return_value=mock.Mock(json=lambda: [])):
        breaches = await client.get_breach_info_by_email("test@example.com")
        assert isinstance(breaches, list)
        assert all(isinstance(breach, dict) for breach in breaches)

if __name__ == "__main__":
    pytest.main()
