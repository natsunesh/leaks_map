import sys
import os



import unittest
from unittest.mock import patch, MagicMock
from api_client import LeakCheckAPIClient
from typing import List, Dict

class TestLeakCheckAPIClient(unittest.TestCase):

    @patch('api_client.requests.get')
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
