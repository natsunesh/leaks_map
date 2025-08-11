import sys
import os



import unittest
from parser import parse_data
from typing import List, Dict, Any

class TestParser(unittest.TestCase):

    def test_parse_data(self):
        """
        Test parsing raw data into a standardized format.
        """
        mock_data: List[Dict[str, Any]] = [
            {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
            {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
        ]

        data = parse_data(mock_data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['service'], 'Service1')
        self.assertEqual(data[1]['service'], 'Service2')

if __name__ == '__main__':
    unittest.main()
