import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch, MagicMock, call
from src.visualizer_breaches import visualize_breaches_with_info
from typing import List, Dict

class TestVisualizerBreaches(unittest.TestCase):

    @patch('visualizer_breaches.nx.Graph')
    def test_visualize_breaches_with_info(self, MockGraph):
        """
        Test visualizing breaches with information.
        """
        mock_graph = MockGraph()
        breaches: List[Dict[str, str]] = [
            {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
            {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
        ]

        visualize_breaches_with_info(breaches)

        mock_graph.add_node.assert_any_call('Service1', label='Service1\n2023-01-01\nDescription1')
        mock_graph.add_node.assert_any_call('Service2', label='Service2\n2023-02-01\nDescription2')
        mock_graph.add_edge.assert_has_calls([
            call('Service1', 'Service2')
        ])

if __name__ == '__main__':
    unittest.main()
