import unittest
import networkx as nx
from unittest.mock import patch, MagicMock, call
from visualizer_breaches import visualize_breaches_with_info
from typing import List, Dict

class TestVisualizerBreaches(unittest.TestCase):

    def test_visualize_breaches_with_info(self):
        """Test visualizing breaches with information."""
        graph = nx.Graph()
        breaches = [
            {'Name': 'Service1', 'Breach Date': '2023-01-01', 'Description': 'Description1'},
            {'Name': 'Service2', 'Breach Date': '2023-02-01', 'Description': 'Description2'}
        ]

        graph = visualize_breaches_with_info(breaches)


        assert 'Service1' in graph.nodes
        assert 'Service2' in graph.nodes
        assert ('Service1', 'Service2') in graph.edges

if __name__ == '__main__':
    unittest.main()
