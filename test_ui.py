import sys
import os



import unittest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication
from ui import LeakMapGUI
from typing import List, Dict

class TestLeakMapGUI(unittest.TestCase):

    def setUp(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication([])

    @patch('ui.LeakCheckAPIClient')
    def test_check_leaks(self, MockAPIClient):
        """
        Test checking for leaks in the GUI.
        """
        mock_api_client = MockAPIClient.return_value
        mock_api_client.get_breach_info.return_value = [
            {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
            {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
        ]

        gui = LeakMapGUI()
        gui.email_input.setText('test@example.com')
        gui.check_leaks()

        print(mock_api_client.mock_calls)  # Debugging mock calls
        self.assertIn('Found 2 breaches for test@example.com.', gui.result_text.toPlainText())

    @patch('ui.LeakCheckAPIClient')
    def test_export_report(self, MockAPIClient):
        """
        Test exporting a report in the GUI.
        """
        mock_api_client = MockAPIClient.return_value
        mock_api_client.get_breach_info.return_value = [
            {'service_name': 'Service1', 'breach_date': '2023-01-01', 'description': 'Description1'},
            {'service_name': 'Service2', 'breach_date': '2023-02-01', 'description': 'Description2'}
        ]

        gui = LeakMapGUI()
        gui.email_input.setText('test@example.com')
        gui.export_report()

        with open('test@example.com_report.txt', 'r') as report_file:
            content = report_file.read()
            self.assertIn('Service: Service1', content)
            self.assertIn('Service: Service2', content)

if __name__ == '__main__':
    unittest.main()
