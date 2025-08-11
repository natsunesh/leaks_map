import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch, MagicMock, call
from src.recommendations import print_recommendations_for_breaches
from typing import List, Dict

class TestRecommendations(unittest.TestCase):

    @patch('src.recommendations.generate_recommendations')
    def test_print_recommendations_for_breaches(self, mock_generate_recommendations):
        """
        Test printing recommendations for breaches.
        """
        mock_generate_recommendations.side_effect = [
            ['Recommendation 1'],
            ['Recommendation 2']
        ]

        breaches: List[Dict[str, str]] = [
            {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
            {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
        ]

        print_recommendations_for_breaches(breaches, 'Russian')

        mock_generate_recommendations.assert_has_calls([
            call('Service1', 'Russian'),
            call('Service2', 'Russian')
        ])

if __name__ == '__main__':
    unittest.main()
