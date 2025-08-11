import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch, MagicMock
from src.api_client import LeakCheckAPIClient
from typing import List, Dict

class TestLeakCheckAPIClient(unittest.TestCase):

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_caching(self, mock_get):
        """Test the caching mechanism for API responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        # Check if the data is cached
        cached_data = api_client.cache_manager.get(api_client.BASE_URL, {'key': 'test_key', 'check': 'test@example.com'})
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 2)
        self.assertEqual(cached_data[0]['service_name'], 'Service1')
        self.assertEqual(cached_data[1]['service_name'], 'Service2')

    @patch('src.api_client.requests.get')
    def test_get_breach_info(self, mock_get):
        """Test retrieving breach information for a given email."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'data': [
                {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
                {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
            ]
        }
        mock_get.return_value = mock_response

        api_client = LeakCheckAPIClient(api_key='test_key')
        breaches = api_client.get_breach_info('test@example.com')

        self.assertEqual(len(breaches), 2)
        self.assertEqual(breaches[0]['service_name'], 'Service1')
        self.assertEqual(breaches[
